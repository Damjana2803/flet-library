from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

@dataclass
class Loan:
    id: Optional[int] = None
    book_id: int = 0
    member_id: int = 0
    loan_date: datetime = None
    due_date: datetime = None
    return_date: datetime = None
    status: str = "active"  # active, returned, overdue, lost
    fine_amount: float = 0.0
    notes: str = ""
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.loan_date is None:
            self.loan_date = datetime.now()
        if self.due_date is None:
            # Default loan period is 14 days
            self.due_date = self.loan_date + timedelta(days=14)
    
    def to_dict(self):
        return {
            'id': self.id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'loan_date': self.loan_date.isoformat() if self.loan_date else None,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'return_date': self.return_date.isoformat() if self.return_date else None,
            'status': self.status,
            'fine_amount': self.fine_amount,
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
            loan_date=datetime.fromisoformat(data['loan_date']) if data.get('loan_date') else None,
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            return_date=datetime.fromisoformat(data['return_date']) if data.get('return_date') else None,
            status=data.get('status', 'active'),
            fine_amount=data.get('fine_amount', 0.0),
            notes=data.get('notes', ''),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )
    
    @property
    def is_overdue(self):
        if self.status == "returned":
            return False
        return datetime.now() > self.due_date
    
    @property
    def days_overdue(self):
        if not self.is_overdue:
            return 0
        return (datetime.now() - self.due_date).days
    
    @property
    def days_remaining(self):
        if self.status == "returned":
            return 0
        remaining = (self.due_date - datetime.now()).days
        return max(0, remaining)
    
    def calculate_fine(self, daily_rate: float = 1.0):
        """Calculate fine based on overdue days"""
        if not self.is_overdue:
            return 0.0
        return self.days_overdue * daily_rate
    
    def return_book(self):
        """Mark book as returned"""
        self.status = "returned"
        self.return_date = datetime.now()
        self.updated_at = datetime.now()
        if self.is_overdue:
            self.fine_amount = self.calculate_fine()

