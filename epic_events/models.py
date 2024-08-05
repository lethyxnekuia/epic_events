from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Float,
    Boolean,
    ForeignKey,
    Text,
    Enum,
)
from enum import Enum as PythonEnum
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
from passlib.hash import bcrypt
from itsdangerous import (
    URLSafeTimedSerializer as Serializer,
    BadSignature,
    SignatureExpired,
)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    company_name = Column(String)
    creation_date = Column(DateTime, default=datetime.utcnow)
    last_contact_date = Column(DateTime)
    commercial_contact_id = Column(Integer, ForeignKey("users.id"))

    # Relations
    commercial_contact = relationship("User", back_populates="clients")
    contracts = relationship("Contract", back_populates="client")


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    total_amount = Column(Float)
    remaining_amount = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_signed = Column(Boolean, default=False)

    # Relations
    client = relationship("Client", back_populates="contracts")
    events = relationship("Event", back_populates="contract")


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contract_id = Column(Integer, ForeignKey("contracts.id"))
    support_contact_id = Column(
        Integer, ForeignKey("users.id")
    )
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    location = Column(String)
    attendees = Column(Integer)
    notes = Column(Text)

    # Relations
    contract = relationship("Contract", back_populates="events")
    support_contact = relationship("User", back_populates="events")


class DepartmentEnum(PythonEnum):
    commercial = "commercial"
    support = "support"
    gestion = "gestion"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    department = Column(Enum(DepartmentEnum), nullable=False)

    # Relations
    events = relationship("Event", back_populates="support_contact")
    clients = relationship("Client", back_populates="commercial_contact")

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    @staticmethod
    def generate_token(secret_key, user_id):
        serializer = Serializer(secret_key)
        token = serializer.dumps({"user_id": user_id})
        return token

    @staticmethod
    def verify_token(token, secret_key):
        serializer = Serializer(secret_key)
        try:
            data = serializer.loads(token)
            return data.get("user_id")
        except (BadSignature, SignatureExpired):
            return None
