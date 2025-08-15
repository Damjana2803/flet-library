from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Member:
    id: Optional[int] = None
    first_name: str = ""
    last_name: str = ""
    email: str = ""
    phone: str = ""
    address: str = ""
    membership_number: str = ""
    membership_type: str = "regular"  # regular, student, senior
    membership_status: str = "active"  # active, suspended, expired
    membership_start_date: datetime = None
    membership_end_date: datetime = None
    max_loans: int = 5
    current_loans: int = 0
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.membership_start_date is None:
            self.membership_start_date = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'membership_number': self.membership_number,
            'membership_type': self.membership_type,
            'membership_status': self.membership_status,
            'membership_start_date': self.membership_start_date.isoformat() if self.membership_start_date else None,
            'membership_end_date': self.membership_end_date.isoformat() if self.membership_end_date else None,
            'max_loans': self.max_loans,
            'current_loans': self.current_loans,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            email=data.get('email', ''),
            phone=data.get('phone', ''),
            address=data.get('address', ''),
            membership_number=data.get('membership_number', ''),
            membership_type=data.get('membership_type', 'regular'),
            membership_status=data.get('membership_status', 'active'),
            membership_start_date=datetime.fromisoformat(data['membership_start_date']) if data.get('membership_start_date') else None,
            membership_end_date=datetime.fromisoformat(data['membership_end_date']) if data.get('membership_end_date') else None,
            max_loans=data.get('max_loans', 5),
            current_loans=data.get('current_loans', 0),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def can_borrow(self):
        return (self.membership_status == "active" and 
                self.current_loans < self.max_loans)

