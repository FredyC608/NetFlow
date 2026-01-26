import os
import time

from celery import Celery
import netflow_crypto  # The C++ module

# Phase 2 Imports
from database import SessionLocal # Import Session factory
from models import RawDocument, Transaction


#Phase 3 Imports
import csv
import io 
from datetime import datetime

# 1. Configuration
BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://broker:6379/0")
BACKEND_URL = os.getenv("CELERY_RESULT_BACKEND", "redis://broker:6379/0")

celery_app = Celery(
    "netflow_worker",
    broker=BROKER_URL,
    backend=BACKEND_URL
)

# 2. The Real Task Logic
@celery_app.task(name="proc_csv_task")
def proc_csv_task(doc_id: int, file_path: str, key: str):
    """
    1. Read encrypted file from shared volume.
    2. Decrypt using C++ module (in memory).
    3. (Future) Pass decrypted bytes to OCR.
    """

    db = SessionLocal()

    try:
        # Step A: Validate file exists
        if not os.path.exists(file_path):
            return {"status": "error", "message": "File not found"}

        # Step B: Read Encrypted Bytes
        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        # Step C: C++ Decryption (CPU Intensive)
        # This runs inside the Worker Container
        print(f"Decrypting {file_path} using C++ extension...")
        start_time = time.time()
        
        # Call the C++ function
        decrypted_bytes = netflow_crypto.decrypt(encrypted_data, key)
        decrypted_bytes = netflow_crypto.decrypt(decrypted_bytes, key)
        #Phase 3: 

        #Create the CSV Reader
        decrypted_str = decrypted_bytes.decode('utf-8')
        csv_file = io.StringIO(decrypted_str)
        reader = csv.DictReader(csv_file)


        #Parse and Object Creation
        transactions = []
        for row in reader: 

            transaction_entry = Transaction(
                user_id = 1,
                document_id = doc_id,
                date = datetime.strptime(row['date'], '%Y-%m-%d'),
                amount = float(row['amount']),
                currency = row.get('currency', 'USD'),
                description = row['description'],
                category = row.get('category', 'Uncategorized')
            )

            transactions.append(transaction_entry)
            
        #Bulk Inserting 
        if transactions: 
            db.bulk_save_objects(transactions)
            

        doc = db.query(RawDocument).filter(RawDocument.id == doc_id).first()

        if doc:
            doc.processed = True
            db.commit()
        
        duration = time.time() - start_time

        # Step D: (Temporary) Return stats
        # In the next phase, we will pass 'decrypted_bytes' to Tesseract
        return {
            "status": "success",
            "original_file": file_path,
            "document_id": doc_id,
            "decryption_time_sec": duration,
            "decrypted_size": len(decrypted_bytes),
            # WARNING: Don't return the full text in Redis if it's huge. 
            # Just return a snippet or store it in DB.
            "transactions_inserted": len(transactions),
            "preview": decrypted_str, 
            "transactions" : f"{transactions}"
        }

    except Exception as e:
        db.rollback()
        return {"status": "failure", "error": str(e), "file" : decrypted_str}
    finally: 
        db.close()