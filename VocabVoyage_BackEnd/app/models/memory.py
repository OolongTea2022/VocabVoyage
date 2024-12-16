from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.models.base import Base


class Memory(Base):
    __tablename__ = "memory"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="记忆记录ID")
    user_id = Column(Integer, ForeignKey("user.id"), comment="用户id")
    word_id = Column(Integer, ForeignKey("word.id"), comment="单词ID")
    last_memory_time = Column(Date, comment="上次记忆时间")
    proficiency = Column(Integer, default=0, comment="熟练度: 0 ~ 100")

    user = relationship("User", back_populates="memories")
    word = relationship("Word", back_populates="memories")
