from configs.base import Base
from sqlalchemy import Column, Integer, String


class Users(Base):
    __tablename__ = "users"

    uid = Column(Integer, primary_key=True)
    uname = Column(String(25), nullable=False)
    uemail = Column(String(50), nullable=False)
    upwd = Column(String, nullable=False)

    def __repr__(self) -> str:
        return f"User [Name: {self.uname}, email: {self.uemail}]"


#Base.metadata.create_all()
