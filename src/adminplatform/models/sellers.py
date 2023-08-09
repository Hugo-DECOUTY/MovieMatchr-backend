import uuid
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import VARCHAR

from adminplatform.init_base import Base


class DBSellers(Base):
    __tablename__ = "sellers"

    id = Column(VARCHAR(36), primary_key=True, index=True, default=str(uuid.uuid4))
    email = Column(VARCHAR(255))
    firstname = Column(VARCHAR(255))
    lastname = Column(VARCHAR(255))
    phone = Column(VARCHAR(255), nullable=True)
