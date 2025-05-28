"""
Offer model
"""
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.core.database import BaseModel


class Offer(BaseModel):
    """Offer model matching the PRD schema"""
    __tablename__ = "offers"
    
    # Foreign keys
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    buyer_id = Column(String, ForeignKey("users.id"), nullable=True, index=True)
    
    # Event information
    event_name = Column(String(255), nullable=False, index=True)
    event_type = Column(String(50), nullable=False, index=True)
    venue_name = Column(String(255), nullable=False, index=True)
    venue_address = Column(Text, nullable=True)
    event_date = Column(DateTime, nullable=False, index=True)
    event_description = Column(Text, nullable=True)
    
    # Ticket information
    ticket_count = Column(Integer, nullable=False)
    seat_details = Column(Text, nullable=True)
    ticket_type = Column(String(100), nullable=True)
    
    # Pricing
    original_price = Column(Numeric(10, 2), nullable=True)
    selling_price = Column(Numeric(10, 2), nullable=False, index=True)
    
    # Additional information
    additional_notes = Column(Text, nullable=True)
    
    # Sale status
    is_sold = Column(Boolean, default=False, nullable=False, index=True)
    sold_at = Column(DateTime, nullable=True)
    
    # Relationships
    seller = relationship("User", back_populates="offers", foreign_keys=[user_id])
    buyer = relationship("User", back_populates="purchases", foreign_keys=[buyer_id])
    
    def __str__(self) -> str:
        return f"{self.event_name} at {self.venue_name}"
    
    def __repr__(self) -> str:
        return f"<Offer(event='{self.event_name}', venue='{self.venue_name}', price={self.selling_price})>" 