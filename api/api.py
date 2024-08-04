import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, inspect, ForeignKey, Integer
from sqlalchemy.orm import DeclarativeBase, relationship

import json
from utils import scalar_result_to_dict_list

## Definitions
DB_NAME = 'db.sqlite3'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, DB_NAME)

app = Flask(__name__)
## Definitions end


## App configs
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
## App configs end


## Models
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class GermanNouns(Base):
    __tablename__ = 'german_nouns'
    ID: Mapped[int] = mapped_column(primary_key=True)
    Word: Mapped[str] = mapped_column(String(30))
    Translation: Mapped[str] = mapped_column(String(30))
    Example: Mapped[str] = mapped_column(String(400))
    ExampleTranslation: Mapped[str] = mapped_column(String(400))

    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != '_sa_instance_state' }

class TelegramUser(Base):
    __tablename__ = 'telegram_user'
    ID: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)

    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != '_sa_instance_state' }

class WordSeen(db.Model):
    __tablename__ = 'words_seen'
    ID: Mapped[int] = mapped_column(primary_key=True)
    user: Mapped[ForeignKey] = mapped_column(ForeignKey(TelegramUser.ID))
    word: Mapped[ForeignKey] = mapped_column(ForeignKey(GermanNouns.ID))
    
    def to_dict(self):
        return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key != '_sa_instance_state' }

with app.app_context():
    db.create_all()
    
# Model utils
def get_create_user(username):
    user = TelegramUser(username=username)
    db.session.add(user)
    db.session.commit()
    return user

def get_user_seen_words(user_id):
    return db.session.query(WordSeen).filter_by(user=user_id).all()

def user_seen_word(user_id, word_id):
    word_seen = WordSeen(user=user_id, word=word_id)
    db.session.add(word_seen)
    db.session.commit()
    return True
## Models end

## Routes
@app.route("/get_word/<username>")
def get_word(username):
    try:
        # get user if exists, create if not
        user = db.session.query(TelegramUser).filter_by(username=username).first()
        if not user:
            user = get_create_user(username)
        
        # filter out words sent to user, get first word which is not sent
        seen_words = db.session.query(WordSeen).filter_by(user=user.ID).all()
        if len(seen_words) > 0:
            seen_word_ids = [seen.to_dict()['ID'] for seen in seen_words]
            word = db.session.query(GermanNouns).filter(GermanNouns.ID not in seen_word_ids).first()
        else:
            word = db.session.query(GermanNouns).first()
        
        # add word to sent words for the user
        # TODO: Uncomment this
        # user_seen_word(user.ID, word.ID)
        
        return word.to_dict()
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
    
# test
@app.route("/test")
def test_db():
    try:
        nouns = db.session.query(GermanNouns).all() #db.session.execute(db.select(GermanNouns)).scalars()
        response = scalar_result_to_dict_list(nouns)
        return response
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
        
@app.route("/test_word/<username>")
def test_user(username):
    try:
        user = db.session.query(TelegramUser).filter_by(username=username).first()
        if not user:
            user = get_create_user(username)
        seen_words = db.session.query(WordSeen).filter_by(user=user.ID).all()
        if len(seen_words) > 0:
            seen_word_ids = [seen.to_dict()['ID'] for seen in seen_words]
            word = db.session.query(GermanNouns).filter(GermanNouns.ID not in seen_word_ids).first()
        else:
            word = db.session.query(GermanNouns).first()
        
        # user_seen_word(user.ID, word.ID)
        
        return word.to_dict()
    except Exception as e:
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

## Routes end




if __name__ == '__main__':
    app.run(debug=True)