"""
User model
"""
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import BaseModel


class User(BaseModel):
    """User model matching the PRD schema"""
    __tablename__ = "users"
    
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=True)
    
    # Relationships
    offers = relationship("Offer", back_populates="seller", foreign_keys="Offer.user_id")
    purchases = relationship("Offer", back_populates="buyer", foreign_keys="Offer.buyer_id")
    
    def __str__(self) -> str:
        return self.username
    
    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>" 