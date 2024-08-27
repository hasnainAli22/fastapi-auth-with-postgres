from app.database import Base
from sqlalchemy import Column, String, Integer, TIMESTAMP, Boolean, text, DateTime
from sqlalchemy.sql import func


class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE')
    created = Column(TIMESTAMP(timezone=True), server_default=text('now()'))

class User(Base):
    __tablename__ = 'users'  # Table name in the database

    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"