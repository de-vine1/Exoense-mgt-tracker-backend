from sqlalchemy import Column, Numeric, UUID, ForeignKey
import uuid
from app.infrastructure.database.base import Base

class WalletModel(Base):
    __tablename__ = "wallets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    balance = Column(Numeric(precision=18, scale=2), default=0.0)
