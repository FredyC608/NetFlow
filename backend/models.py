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
    # NEW: Link to alerts so we can show "My Notifications"
    alerts = relationship("Alert", back_populates="owner")

class RawDocument(Base):
    __tablename__ = "raw_documents"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    processed = Column(Boolean, default=False)

    # Relationships
    owner = relationship("User", back_populates="documents")
    transactions = relationship("Transaction", back_populates="source_document")

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    domain = Column(String)
    logo_url = Column(String, nullable=True)
    scraping_rules = Column(JSON, nullable=True)

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
    description = Column(String)
    category = Column(String, index=True)

    # Relationships
    owner = relationship("User", back_populates="transactions")
    vendor = relationship("Vendor", back_populates="transactions")
    source_document = relationship("RawDocument", back_populates="transactions")
    # NEW: Link to alerts. If this specific transaction (e.g., Netflix) triggered an alert
    alerts = relationship("Alert", back_populates="related_transaction")

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    
    # Who is this for?
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # What triggered it? (Optional - some alerts might be general)
    transaction_id = Column(Integer, ForeignKey("transactions.id"), nullable=True)

    # The Logic
    type = Column(String, index=True)  # e.g., "arbitrage", "inflation", "duplicate"
    severity = Column(String)          # e.g., "low", "medium", "critical"
    message = Column(String)           # e.g., "Netflix price increased by $2.00"
    
    # Status
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    owner = relationship("User", back_populates="alerts")
    related_transaction = relationship("Transaction", back_populates="alerts")
