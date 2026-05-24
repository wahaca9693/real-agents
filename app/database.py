"""
Real Agents - Database Configuration
إعداد قاعدة البيانات
"""

from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, Float
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from datetime import datetime
import os

Base = declarative_base()


class User(Base):
    """نموذج المستخدم"""
    __tablename__ = "users"
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    login_count = Column(Integer, default=0)


class VerificationCode(Base):
    """رمز التحقق"""
    __tablename__ = "verification_codes"
    
    id = Column(String(50), primary_key=True)
    email = Column(String(255), nullable=False, index=True)
    code = Column(String(10), nullable=False)
    action = Column(String(50), default="register")  # register, reset_password
    attempts = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
    is_used = Column(Boolean, default=False)


class RefreshToken(Base):
    """Refresh Token"""
    __tablename__ = "refresh_tokens"
    
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), nullable=False, index=True)
    token_hash = Column(String(255), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_revoked = Column(Boolean, default=False)


class Task(Base):
    """المهام"""
    __tablename__ = "tasks"
    
    id = Column(String(50), primary_key=True)
    user_id = Column(String(50), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(String(50), default="development")
    priority = Column(Integer, default=1)
    status = Column(String(20), default="pending")  # pending, in_progress, completed, failed
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)


# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "sqlite+aiosqlite:///./workspace/real_agents.db"
)


# Engine and Session
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True
)

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db():
    """إنشاء قاعدة البيانات والجداول"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    """الحصول على session"""
    async with async_session_maker() as session:
        yield session