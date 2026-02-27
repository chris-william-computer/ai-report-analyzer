from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.settings import settings

engine = create_engine(settings.DATABASE_URL)
"""
    SQLAlchemy database engine instance configured with the application's database URL.
    
    This engine serves as the central connection factory for the application's database
    interactions. It manages connection pooling, SQL statement execution, and database
    communication protocols. The engine is initialized with the database URL from the
    application settings and handles all low-level database operations while maintaining
    efficient connection reuse through built-in pooling mechanisms.
"""

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
"""
SQLAlchemy session factory configured for transactional database operations.

This session factory creates database sessions that are bound to the application's
configured database engine. It's configured with autocommit=False and autoflush=False
to provide explicit control over transaction boundaries and database synchronization.
Each session created from this factory maintains its own transaction state and can
be used for multiple related database operations before committing or rolling back
the entire transaction.

The session factory ensures proper isolation between concurrent database operations
and provides a clean interface for ORM operations while maintaining optimal performance
through connection pooling and resource management.
"""

Base = declarative_base()
"""
SQLAlchemy declarative base class for model definition inheritance.

This base class serves as the foundation for all database models in the application.
Models that inherit from this base class automatically gain SQLAlchemy ORM capabilities
including table creation, query interfaces, and relationship management. The declarative
base handles the mapping between Python classes and database tables, providing a clean
object-oriented interface for database interactions.

All application-specific database models should inherit from this Base class to ensure
proper integration with the SQLAlchemy ORM system and automatic table registration
during application startup.
"""


def get_db():
    """
    Generator function that provides database sessions for dependency injection.

    This generator creates a new database session from the SessionLocal factory and yields
    it to the caller, ensuring proper session lifecycle management through context handling.
    The function implements a try-finally pattern to guarantee that database sessions are
    always closed after use, preventing connection leaks and resource exhaustion. This
    pattern is commonly used in FastAPI applications for dependency injection of database
    sessions into route handlers.

    The yielded session supports full SQLAlchemy ORM functionality including querying,
    object persistence, and transaction management. The automatic cleanup ensures that
    connections are returned to the pool efficiently, maintaining optimal database
    connection utilization across the application.

    Yields:
        Session: A SQLAlchemy database session instance configured for transactional
                operations. The session includes methods for querying, adding, updating,
                and deleting database records with proper transaction isolation.

    Example:
        # In a FastAPI route handler using dependency injection
        from fastapi import Depends
        
        def my_route(db: Session = Depends(get_db)):
            user = db.query(User).filter(User.id == 1).first()
            return user
            
        # Manual usage (though dependency injection is preferred)
        for db_session in get_db():
            users = db_session.query(User).all()
            break  # Important: exit generator to trigger cleanup
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()