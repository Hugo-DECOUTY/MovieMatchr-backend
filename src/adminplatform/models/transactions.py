import uuid
from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.mysql import VARCHAR, INTEGER

from adminplatform.init_base import Base


class DBTransactions(Base):
    __tablename__ = "transactions"

    id = Column(VARCHAR(36), primary_key=True, index=True, default=str(uuid.uuid4))
    recording_id = Column(VARCHAR(36), nullable=False)
    type_of_action = Column(INTEGER, nullable=False)
    date_of_action = Column(INTEGER, nullable=False)
    licence_id_action = Column(VARCHAR(36), ForeignKey("licences.id"), nullable=False)
    complementary_id = Column(VARCHAR(36), nullable=False)
    email_action = Column(VARCHAR(255), nullable=False)
    email_complementary = Column(VARCHAR(255), nullable=False)
