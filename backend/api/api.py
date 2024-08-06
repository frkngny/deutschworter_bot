from flask import Blueprint, request, make_response, jsonify
from . import db
from .models import TelegramUser, GermanWords, WordSeen, UserConfiguration
from sqlalchemy import text
import random

api = Blueprint('api', __name__)

## Model utils
def check_get_create_user(username):
    user = TelegramUser.query.filter_by(username=username).first()
    if not user:
        user = TelegramUser(username=username)
        db.session.add(user)
        db.session.commit()
        
        user_config = UserConfiguration(user_id = user.ID)
        db.session.add(user_config)
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
    
    def word_id(item):
        return item.ID   
    
    if len(seen_words) > 0:
        seen_word_ids = [seen.to_dict()['word_id'] for seen in seen_words]
        words = GermanWords.query.filter(GermanWords.ID.notin_(seen_word_ids)).all()
        
        min_word = min(words, key=word_id)
        max_word = max(words, key=word_id)
        random_number = random.randint(min_word.ID, max_word.ID)
        
        word = words[random_number]
    else:
        word = GermanWords.query.first()
    return word
## Model utils end


## Routes
@api.route('/user', methods=['POST'])
def user():
    if request.method == 'POST':
        data = request.form
        if 'username' not in data:
            no_username_text = "username is not provided or not in correct syntax"
            return make_response(jsonify(error=no_username_text), 400)
        
        username = data['username']
        _ = check_get_create_user(username)
        
        text = "User with username %s is created" % username
        return make_response(jsonify(response=text), 200)

@api.route('/user/configure', methods=['POST'])
def user_configure():
    if request.method == 'POST':
        data = request.form
        if 'username' not in data:
            no_username_text = "username is not provided or not in correct syntax"
            return make_response(jsonify(error=no_username_text), 400)
        username = data['username']
        user = check_get_create_user(username)
        
        user_config = UserConfiguration.query.filter_by(user_id=user.ID).first()
        commit = False
        if not user_config:
            user_config = UserConfiguration(user_id = user.ID)
            db.session.add(user_config)
            commit = True
        if 'lang' in data:
            user_config.preferred_language = data['lang']
            commit = True
        if 'time' in data:
            user_config.notification_time = data['time']
            commit = True
        if commit:
            db.session.commit()
        
        text = "User configuration is updated"
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

@api.route("/reset_words", methods=['POST'])
def reset_words():
    if request.method == 'POST':
        data = request.form
        if 'username' not in data:
            no_username_text = "username is not provided or not in correct syntax"
            return make_response(jsonify(error=no_username_text), 400)
        
        username = data['username']
        user = TelegramUser.query.filter_by(username=username).first()
        if not user:
            no_user_text = "There is no user with this username"
            return make_response(jsonify(error=no_user_text), 400)
        
        WordSeen.query.filter_by(user_id=user.ID).delete()
        db.session.commit()
        return make_response(jsonify(response="Success"), 200)
## Routes end