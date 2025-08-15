from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Reservation:
    id: Optional[int] = None
    book_id: int = 0
    member_id: int = 0
    reservation_date: datetime = None
    expiry_date: datetime = None
    status: str = "active"  # active, fulfilled, expired, cancelled
    priority: int = 1
    notes: str = ""
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.reservation_date is None:
            self.reservation_date = datetime.now()
        if self.expiry_date is None:
            # Default reservation expiry is 7 days
            self.expiry_date = self.reservation_date + timedelta(days=7)
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'reservation_date': self.reservation_date.isoformat() if self.reservation_date else None,
            'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
            'status': self.status,
            'priority': self.priority,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            book_id=data.get('book_id', 0),
            member_id=data.get('member_id', 0),
            reservation_date=datetime.fromisoformat(data['reservation_date']) if data.get('reservation_date') else None,
            expiry_date=datetime.fromisoformat(data['expiry_date']) if data.get('expiry_date') else None,
            status=data.get('status', 'active'),
            priority=data.get('priority', 1),
            notes=data.get('notes', ''),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    @property
    def is_expired(self):
        if self.status != "active":
            return False
        return datetime.now() > self.expiry_date
    
    @property
    def days_until_expiry(self):
        if self.status != "active":
            return 0
        remaining = (self.expiry_date - datetime.now()).days
        return max(0, remaining)
    
    def fulfill(self):
        """Mark reservation as fulfilled"""
        self.status = "fulfilled"
        self.updated_at = datetime.now()
    
    def cancel(self):
        """Cancel the reservation"""
        self.status = "cancelled"
        self.updated_at = datetime.now()
    
    def expire(self):
        """Mark reservation as expired"""
        self.status = "expired"
        self.updated_at = datetime.now()

