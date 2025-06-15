from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from db.database import Base


class TbITBlog(Base):
    __tablename__ = "Tb_IT_Blog"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    desc = Column(String, nullable=False)
