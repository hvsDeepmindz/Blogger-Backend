from sqlalchemy import Column, Integer, String, ForeignKey
from db.database import Base


class TbITMedia(Base):
    __tablename__ = "Tb_IT_Media"
    id = Column(Integer, primary_key=True, index=True)
    blog_id = Column(Integer, ForeignKey("Tb_IT_Blog.id"), nullable=False)
    img = Column(String, nullable=False)
