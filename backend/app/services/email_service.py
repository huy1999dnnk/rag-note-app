import boto3
from botocore.exceptions import ClientError
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class EmailService:
    """Service for sending emails using AWS SES."""

    def __init__(self):
        self.ses_client = boto3.client(
            'ses',
            region_name=settings.AWS_REGION,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )

    def send_email(self, recipient_email: str, subject: str, body_text: str, body_html: str = None) -> None:
        """Send an email using AWS SES."""
        try:
            message = {
                'Subject': {
                    'Data': subject,
                    'Charset': 'UTF-8'
                },
                'Body': {
                    'Text': {
                        'Data': body_text,
                        'Charset': 'UTF-8'
                    }
                }
            }
            
            # Add HTML version if provided
            if body_html:
                message['Body']['Html'] = {
                    'Data': body_html,
                    'Charset': 'UTF-8'
                }
                
            response = self.ses_client.send_email(
                Source=settings.EMAIL_SENDER,
                Destination={
                    'ToAddresses': [recipient_email],
                },
                Message=message
            )
            logger.info(f"Email sent! Message ID: {response['MessageId']}")
        except ClientError as e:
            logger.error(f"Failed to send email: {e.response['Error']['Message']}")