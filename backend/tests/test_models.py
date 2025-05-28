"""
Tests for database models
"""
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from app.core.database import Base, get_db
from app.models.user import User
from app.models.offer import Offer


@pytest.fixture
def test_db():
    """Create a test database"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


class TestUserModel:
    """Test cases for User model"""
    
    def test_create_user(self, test_db):
        """Test creating a user with all required fields"""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            full_name="Test User",
            phone_number="+1234567890"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        assert user.id is not None
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.password_hash == "hashed_password"
        assert user.full_name == "Test User"
        assert user.phone_number == "+1234567890"
        assert user.created_at is not None
        assert user.updated_at is not None
    
    def test_create_user_without_phone(self, test_db):
        """Test creating a user without phone number (optional field)"""
        user = User(
            username="testuser2",
            email="test2@example.com",
            password_hash="hashed_password",
            full_name="Test User 2"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        assert user.id is not None
        assert user.phone_number is None
    
    def test_username_unique_constraint(self, test_db):
        """Test that username must be unique"""
        user1 = User(
            username="duplicate",
            email="test1@example.com",
            password_hash="hashed_password",
            full_name="Test User 1"
        )
        test_db.add(user1)
        test_db.commit()
        
        user2 = User(
            username="duplicate",
            email="test2@example.com",
            password_hash="hashed_password",
            full_name="Test User 2"
        )
        test_db.add(user2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_email_unique_constraint(self, test_db):
        """Test that email must be unique"""
        user1 = User(
            username="user1",
            email="duplicate@example.com",
            password_hash="hashed_password",
            full_name="Test User 1"
        )
        test_db.add(user1)
        test_db.commit()
        
        user2 = User(
            username="user2",
            email="duplicate@example.com",
            password_hash="hashed_password",
            full_name="Test User 2"
        )
        test_db.add(user2)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_user_string_representation(self, test_db):
        """Test user string representation"""
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashed_password",
            full_name="Test User"
        )
        assert str(user) == "testuser"


class TestOfferModel:
    """Test cases for Offer model"""
    
    def test_create_offer(self, test_db):
        """Test creating an offer with all required fields"""
        # First create a user
        user = User(
            username="seller",
            email="seller@example.com",
            password_hash="hashed_password",
            full_name="Seller User"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Create offer
        offer = Offer(
            user_id=user.id,
            event_name="Taylor Swift Concert",
            event_type="Concert",
            venue_name="Madison Square Garden",
            venue_address="4 Pennsylvania Plaza, New York, NY 10001",
            event_date=datetime(2024, 12, 31, 20, 0),
            event_description="Amazing concert!",
            ticket_count=2,
            seat_details="Section 101, Row A, Seats 1-2",
            ticket_type="General Admission",
            original_price=150.00,
            selling_price=120.00,
            additional_notes="Great seats!"
        )
        test_db.add(offer)
        test_db.commit()
        test_db.refresh(offer)
        
        assert offer.id is not None
        assert offer.user_id == user.id
        assert offer.event_name == "Taylor Swift Concert"
        assert offer.event_type == "Concert"
        assert offer.venue_name == "Madison Square Garden"
        assert offer.is_sold is False
        assert offer.buyer_id is None
        assert offer.sold_at is None
        assert offer.created_at is not None
        assert offer.updated_at is not None
    
    def test_create_minimal_offer(self, test_db):
        """Test creating an offer with only required fields"""
        # First create a user
        user = User(
            username="seller2",
            email="seller2@example.com",
            password_hash="hashed_password",
            full_name="Seller User 2"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Create minimal offer
        offer = Offer(
            user_id=user.id,
            event_name="Concert",
            event_type="Concert",
            venue_name="Venue",
            event_date=datetime(2024, 12, 31, 20, 0),
            ticket_count=1,
            selling_price=50.00
        )
        test_db.add(offer)
        test_db.commit()
        test_db.refresh(offer)
        
        assert offer.id is not None
        assert offer.venue_address is None
        assert offer.event_description is None
        assert offer.seat_details is None
        assert offer.ticket_type is None
        assert offer.original_price is None
        assert offer.additional_notes is None
    
    def test_offer_user_relationship(self, test_db):
        """Test the relationship between offer and user"""
        # Create user
        user = User(
            username="seller3",
            email="seller3@example.com",
            password_hash="hashed_password",
            full_name="Seller User 3"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        # Create offer
        offer = Offer(
            user_id=user.id,
            event_name="Test Event",
            event_type="Concert",
            venue_name="Test Venue",
            event_date=datetime(2024, 12, 31, 20, 0),
            ticket_count=1,
            selling_price=50.00
        )
        test_db.add(offer)
        test_db.commit()
        test_db.refresh(offer)
        
        # Test relationship
        assert offer.seller.username == "seller3"
        assert offer.seller.email == "seller3@example.com"
    
    def test_mark_offer_as_sold(self, test_db):
        """Test marking an offer as sold"""
        # Create seller
        seller = User(
            username="seller4",
            email="seller4@example.com",
            password_hash="hashed_password",
            full_name="Seller User 4"
        )
        test_db.add(seller)
        test_db.commit()
        test_db.refresh(seller)
        
        # Create buyer
        buyer = User(
            username="buyer1",
            email="buyer1@example.com",
            password_hash="hashed_password",
            full_name="Buyer User 1"
        )
        test_db.add(buyer)
        test_db.commit()
        test_db.refresh(buyer)
        
        # Create offer
        offer = Offer(
            user_id=seller.id,
            event_name="Test Event",
            event_type="Concert",
            venue_name="Test Venue",
            event_date=datetime(2024, 12, 31, 20, 0),
            ticket_count=1,
            selling_price=50.00
        )
        test_db.add(offer)
        test_db.commit()
        test_db.refresh(offer)
        
        # Mark as sold
        offer.is_sold = True
        offer.buyer_id = buyer.id
        offer.sold_at = datetime.utcnow()
        test_db.commit()
        test_db.refresh(offer)
        
        assert offer.is_sold is True
        assert offer.buyer_id == buyer.id
        assert offer.sold_at is not None
        assert offer.buyer.username == "buyer1"
    
    def test_foreign_key_constraint(self, test_db):
        """Test foreign key constraint for user_id"""
        offer = Offer(
            user_id="non-existent-id",
            event_name="Test Event",
            event_type="Concert",
            venue_name="Test Venue",
            event_date=datetime(2024, 12, 31, 20, 0),
            ticket_count=1,
            selling_price=50.00
        )
        test_db.add(offer)
        
        with pytest.raises(IntegrityError):
            test_db.commit()
    
    def test_offer_string_representation(self, test_db):
        """Test offer string representation"""
        # Create user first
        user = User(
            username="seller5",
            email="seller5@example.com",
            password_hash="hashed_password",
            full_name="Seller User 5"
        )
        test_db.add(user)
        test_db.commit()
        test_db.refresh(user)
        
        offer = Offer(
            user_id=user.id,
            event_name="Test Concert",
            event_type="Concert",
            venue_name="Test Venue",
            event_date=datetime(2024, 12, 31, 20, 0),
            ticket_count=1,
            selling_price=50.00
        )
        assert str(offer) == "Test Concert at Test Venue"


class TestDatabaseConnection:
    """Test database connection and session management"""
    
    def test_database_session_creation(self):
        """Test that database session can be created"""
        db = next(get_db())
        assert db is not None
        db.close() 