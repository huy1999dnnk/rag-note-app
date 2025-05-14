import json
import threading
import time
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.document_embedding import DocumentEmbedding, EmbeddingSource
from app.models.note import Note
from app.services.openai_client import OpenAiClient
from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
import logging

logger = logging.getLogger(__name__)


class VectorService:
    _debounce_timers = {}

    def __init__(self):
        self.openAiClient = OpenAiClient()

    def extract_plain_text_from_json(self, json_content):
        """
        Extract plain text from a structured JSON document with nested children.
        Handles any level of nesting in the document tree.
        """
        # Convert string to JSON if needed
        if isinstance(json_content, str):
            try:
                json_content = json.loads(json_content)
            except json.JSONDecodeError:
                return ""

        # Helper function to recursively extract text from nodes
        def extract_text_from_node(node):
            texts = []

            if not node:
                return texts

            if "type" in node and node["type"] == "table":
                table_texts = []
                if "content" in node and isinstance(node["content"], dict):
                    table_content = node["content"]

                    # Process rows
                    if "rows" in table_content and isinstance(
                        table_content["rows"], list
                    ):
                        for row in table_content["rows"]:
                            row_texts = []

                            # Process cells in the row
                            if "cells" in row and isinstance(row["cells"], list):
                                for cell in row["cells"]:
                                    cell_text = []

                                    # Extract text from cell content
                                    if "content" in cell and isinstance(
                                        cell["content"], list
                                    ):
                                        for content_item in cell["content"]:
                                            cell_text.extend(
                                                extract_text_from_node(content_item)
                                            )

                                    row_texts.append(" ".join(cell_text))

                            # Join cells with tabs to maintain table structure
                            if row_texts:
                                table_texts.append(" | ".join(row_texts))

                # Join rows with newlines
                if table_texts:
                    texts.append("\n" + "\n".join(table_texts) + "\n")

            # Handle text nodes directly
            elif "type" in node and node["type"] == "text" and "text" in node:
                texts.append(node["text"])

            # Process standard content array
            elif "content" in node:
                if isinstance(node["content"], list):
                    for item in node["content"]:
                        texts.extend(extract_text_from_node(item))

            # Process children array recursively
            if "children" in node and isinstance(node["children"], list):
                for child in node["children"]:
                    child_texts = extract_text_from_node(child)
                    if child_texts:
                        texts.extend(child_texts)

            return texts

        # Process all top-level nodes
        all_texts = []
        if isinstance(json_content, list):
            for node in json_content:
                all_texts.extend(extract_text_from_node(node))
        elif isinstance(json_content, dict):
            all_texts.extend(extract_text_from_node(json_content))

        # Join all text pieces with spaces
        result = " ".join(all_texts).strip()

        # Clean up spaces but preserve newlines
        # First collapse multiple spaces within lines
        result = re.sub(r" +", " ", result)
        # Then collapse multiple newlines to single newlines
        result = re.sub(r"\n+", "\n", result)

        return result

    def chunk_text(self, text, chunk_size=800, overlap=100):
        """
        Use LangChain's RecursiveCharacterTextSplitter to split text into chunks.
        chunk_size: maximum number of characters in a chunk
        overlap: number of characters to overlap between chunks
        """
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            length_function=len,
        )
        # Split the text into Document objects
        documents = splitter.create_documents([text])
        # Return just the page_content of each Document as chunks
        return [doc.page_content for doc in documents]

    def index_pdf_content(
        self, note_id: str, pdf_content: str, filename: str, db: Session
    ):

        # Format content with PDF source info
        pdf_content = f"[PDF Content from: {filename}]\n\n{pdf_content}"

        # Chunk the content
        chunks = self.chunk_text(pdf_content)
        CHUNK_SIZE = 50  # Adjust this based on the rate limit of your API

        # Create embeddings for PDF chunks
        for i in range(0, len(chunks), CHUNK_SIZE):
            batch = chunks[i : i + CHUNK_SIZE]

            # Ensure that the batch does not exceed the number of chunks
            if len(batch) == 0:
                continue  # Skip empty batches if any

            # Process each chunk in the batch
            for idx, chunk in enumerate(batch):
                embedding = self.openAiClient.embedding_text(chunk)
                doc_emb = DocumentEmbedding(
                    note_id=note_id,
                    chunk_index=idx + i,  # Adjust index for continuity
                    content=chunk,
                    embedding=embedding,
                    source_type=EmbeddingSource.PDF_ATTACHMENT,
                    source_file=filename,
                )
                db.add(doc_emb)

            db.commit()

    def index_note(self, note: Note, db: Session):
        # Remove old embeddings
        db.query(DocumentEmbedding).filter(
            DocumentEmbedding.note_id == note.id,
            DocumentEmbedding.source_type == EmbeddingSource.NOTE_TEXT,
        ).delete()

        plain_text = self.extract_plain_text_from_json(note.content)
        chunks = self.chunk_text(plain_text)
        # Define the maximum chunk size to avoid rate limit issues
        CHUNK_SIZE = 50  # Adjust this based on the rate limit of your API

        # Process in batches
        for i in range(0, len(chunks), CHUNK_SIZE):
            batch = chunks[i : i + CHUNK_SIZE]

            # Ensure that the batch does not exceed the number of chunks
            if len(batch) == 0:
                continue  # Skip empty batches if any

            # Process each chunk in the batch
            for idx, chunk in enumerate(batch):
                embedding = self.openAiClient.embedding_text(chunk)
                doc_emb = DocumentEmbedding(
                    note_id=note.id,
                    chunk_index=idx + i,  # Adjust index for continuity
                    content=chunk,
                    embedding=embedding,
                    source_type=EmbeddingSource.NOTE_TEXT,
                )
                db.add(doc_emb)

            db.commit()

    def debounce_index_note(self, note: Note, db_factory, wait_seconds=2):
        """
        Debounce embedding for a note. Only the last update within wait_seconds will trigger embedding.
        db_factory: a callable that returns a new Session (e.g., SessionLocal)
        """
        note_id = note.id

        def run():
            time.sleep(wait_seconds)
            db = db_factory()
            try:
                # Re-fetch the latest note content from DB
                latest_note = db.query(Note).filter(Note.id == note.id).first()
                if latest_note:
                    self.index_note(latest_note, db)
            finally:
                db.close()
            VectorService._debounce_timers.pop(note_id, None)

        # Cancel previous timer if exists
        if note_id in VectorService._debounce_timers:
            VectorService._debounce_timers[note_id].cancel()
        timer = threading.Timer(wait_seconds, run)
        VectorService._debounce_timers[note_id] = timer
        timer.start()

    def enrich_chunk_with_note_info(self, chunk_content, note_title, note_id):
        """
        Enriches a chunk with note information without changing its data type.
        Returns a formatted string containing the original content plus source info.
        """
        # Format: Add a header with note title and ID at the top of each chunk
        enriched_content = f"[Source: {note_title} (ID: {note_id})]\n\n{chunk_content}"
        return enriched_content

    def search_similar_chunks(self, query: str, db: Session, top_k):
        """
        Search for similar chunks in the database.
        """
        try:
            raw_embedding = self.openAiClient.embedding_text(query)
            stmt = (
                select(
                    DocumentEmbedding.content,
                    Note.id.label("note_id"),
                    Note.title.label("note_title"),
                )
                .join(Note, DocumentEmbedding.note_id == Note.id)
                .order_by(DocumentEmbedding.embedding.cosine_distance(raw_embedding))
                .limit(top_k)
            )

            results = db.execute(stmt).mappings().all()

            enriched_contents = []
            for row in results:
                # Convert UUID to string and add note info to content
                enriched_content = self.enrich_chunk_with_note_info(
                    row.content, row.note_title, str(row.note_id)
                )
                enriched_contents.append(enriched_content)

            return enriched_contents
        except Exception as e:
            # Handle the error gracefully
            logger.exception(f"Error in search_similar_chunks: {e}")
            return []
