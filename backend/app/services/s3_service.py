import boto3
import os

class S3Service: #creates one s3 connection
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = boto3.client(
                's3',
                aws_access_key_id=os.getenv("RAG_AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("RAG_AWS_SECRET_ACCESS_KEY"),
                region_name='us-east-1'
            )
        return cls._instance
    
    def upload_pdf(self, file_content: bytes, filename: str):
        """Upload PDF to S3, return the S3 key"""
        bucket = os.getenv("RAG_AWS_S3_BUCKET_NAME")

        try:
            self.client.put_object(
                Bucket=bucket,
                Key=filename,
                Body=file_content
            )
            return filename # returns s3 key
        except Exception as e:
            raise Exception(f"S3 upload failed: {str(e)}")