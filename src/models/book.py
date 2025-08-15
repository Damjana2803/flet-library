from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    id: Optional[int] = None
    title: str = ""
    author: str = ""
    isbn: str = ""
    category: str = ""
    publication_year: int = 0
    publisher: str = ""
    description: str = ""
    total_copies: int = 1
    available_copies: int = 1
    location: str = ""
    status: str = "available"  # available, unavailable, maintenance
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'category': self.category,
            'publication_year': self.publication_year,
            'publisher': self.publisher,
            'description': self.description,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'location': self.location,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get('id'),
            title=data.get('title', ''),
            author=data.get('author', ''),
            isbn=data.get('isbn', ''),
            category=data.get('category', ''),
            publication_year=data.get('publication_year', 0),
            publisher=data.get('publisher', ''),
            description=data.get('description', ''),
            total_copies=data.get('total_copies', 1),
            available_copies=data.get('available_copies', 1),
            location=data.get('location', ''),
            status=data.get('status', 'available'),
            created_at=datetime.fromisoformat(data['created_at']) if data.get('created_at') else None,
            updated_at=datetime.fromisoformat(data['updated_at']) if data.get('updated_at') else None
        )

