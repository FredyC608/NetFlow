from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    documents = relationship("RawDocument", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")

class RawDocument(Base):
    __tablename__ = "raw_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)  # Path in MinIO/S3 or Encrypted Blob
    upload_date = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)

    # Relationships
    owner = relationship("User", back_populates="documents")
    transactions = relationship("Transaction", back_populates="source_document")

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    domain = Column(String)  # e.g., "netflix.com"
    logo_url = Column(String, nullable=True)
    scraping_rules = Column(JSON, nullable=True)  # Stores {"selector": "#price", "url": "/login"}

    # Relationships
    transactions = relationship("Transaction", back_populates="vendor")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=True)
    document_id = Column(Integer, ForeignKey("raw_documents.id"), nullable=True)
    
    date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    description = Column(String)  # The raw text from bank statement
    category = Column(String, index=True) # "Food", "Utilities"

    # Relationships
    owner = relationship("User", back_populates="transactions")
    vendor = relationship("Vendor", back_populates="transactions")
    source_document = relationship("RawDocument", back_populates="transactions")