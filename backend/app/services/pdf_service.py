import io
import PyPDF2
import logging

logger = logging.getLogger(__name__)


class PDFService:
    @staticmethod
    def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
        """Extract text from PDF bytes"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_file)

            text_content = []
            # Process each page
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text() or ""
                if text.strip():
                    text_content.append(f"[Page {page_num + 1}]\n{text}")

            # Join all pages with separators
            return "\n\n".join(text_content)
        except Exception as e:
            logger.error(f"Error extracting PDF text: {e}")
            return ""
