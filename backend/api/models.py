from . import db

from sqlalchemy import String, inspect, ForeignKey, Integer, Column, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class TelegramUser(db.Model):
    ID: int = Column(Integer, primary_key=True)
    username: str = Column(String(100), unique=True, nullable=False)
    
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != '_sa_instance_state' }

class GermanWords(db.Model):
    ID: int = Column(Integer, primary_key=True)
    Word: str = Column(String(50), nullable=False, unique=True)
    Translation: str = Column(String(50))
    Sentence: str = Column(String(400))
    SentenceTranslation: str = Column(String(400))
    Type: str = Column(String(20))

    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != '_sa_instance_state' }

class WordSeen(db.Model):
    ID: int = Column(Integer, primary_key=True)
    user_id: int = Column(ForeignKey(TelegramUser.ID))
    word_id: int = Column(ForeignKey(GermanWords.ID))
    seen_at: DateTime = Column(DateTime, default=func.now())
    
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != '_sa_instance_state' }
