from flask import Blueprint, request, make_response, jsonify
from . import db
from .models import TelegramUser, GermanWords, WordSeen
from sqlalchemy import text

api = Blueprint('api', __name__)

## Model utils
def check_get_create_user(username):
    user = TelegramUser.query.filter_by(username=username).first()
    if not user:
        user = TelegramUser(username=username)
        db.session.add(user)
        db.session.commit()
    return user

def get_user_seen_words(user_id):
    return WordSeen.query.filter_by(user=user_id).all()

def user_seen_word(user, word):
    word_seen = WordSeen(user_id=user.ID, word_id=word.ID)
    db.session.add(word_seen)
    db.session.commit()
    return True

def get_word_for_user(user):
    # filter out words sent to user, get first word which is not sent
    seen_words = WordSeen.query.filter_by(user_id=user.ID).all()
    
    if len(seen_words) > 0:
        seen_word_ids = [seen.to_dict()['word_id'] for seen in seen_words]
        word = GermanWords.query.filter(GermanWords.ID.notin_(seen_word_ids)).first()
        print(word)
    else:
        word = GermanWords.query.first()
    return word
## Model utils end


## Routes
@api.route('/user', methods=['GET'])
def user():
    if request.method == 'GET':
        data = request.form
        if 'username' not in data:
            no_username_text = "username is not provided or not in correct syntax"
            return make_response(jsonify(error=no_username_text), 400)
        
        username = data['username']
        _ = check_get_create_user(username)
        
        text = "User with username %s is created" % username
        return make_response(jsonify(response=text), 200) 

@api.route("/get_word", methods=['GET'])
def get_word():
    if request.method == 'GET':
        data = request.form
        if 'username' not in data:
            no_username_text = "username is not provided or not in correct syntax"
            return make_response(jsonify(error=no_username_text), 400)
        
        username = data['username']
        try:
            # get user if exists, create if not
            user = check_get_create_user(username)

            # get word for the specific user, None if no word
            word = get_word_for_user(user)
            
            if not word:
                no_word_text = "We are sorry! There is no word left :/ We are frequently adding more words."
                return make_response(jsonify(error=no_word_text))
            # add word to sent words for the user
            # TODO: Uncomment this
            user_seen_word(user, word)
            
            return make_response(word.to_dict(), 200)
        except Exception as e:
            text = f"Error: {str(e)}"
            return make_response(jsonify(error=text), 500)
## Routes end