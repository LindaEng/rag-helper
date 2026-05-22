from dotenv import load_dotenv
import boto3
import os

load_dotenv()

class S3Service: #creates one s3 connection
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            key = os.getenv("RAG_AWS_ACCESS_KEY_ID")
            secret = os.getenv("RAG_AWS_SECRET_ACCESS_KEY")
            bucket = os.getenv("RAG_AWS_S3_BUCKET_NAME")
            
            print(f"DEBUG - Key: {key}")
            print(f"DEBUG - Secret: {secret}")
            print(f"DEBUG - Bucket: {bucket}")
            
            cls._instance.client = boto3.client(
                's3',
                aws_access_key_id=key,
                aws_secret_access_key=secret,
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

s3_service = S3Service()