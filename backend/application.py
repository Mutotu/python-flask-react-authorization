import os
from flask import Flask, request
from flask_cors import CORS
import sqlalchemy
app = Flask(__name__)
CORS(app)
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
import jwt
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
import models
models.db.init_app(app)

def root():
  return 'ok'
app.route('/', methods=["GET"])(root)

@app.route('/users', methods=["POST"])
def create_user():
  # notice that in models the paswotd is not there in to_json func because of 
  hashed_pw = bcrypt.generate_password_hash(request.json["password"]).decode("utf-8")
  try:
      user = models.User(
        email=request.json["email"],
        # password=request.json["password"]
        password=hashed_pw
      )
      models.db.session.add(user)
      models.db.session.commit()
      encrypted_id = jwt.encode({"user_id":user.id}, os.environ.get("JWT_SECRET"), algorithm="HS256")
      return {"user":user.to_json(),
              "user_id":encrypted_id}
  except sqlalchemy.exc.IntegrityError:
    # Remeber to inluce 400 so that fronten knows it
    return {"message": 'Email must be unique'}, 400
  ######login
@app.route('/users/login', methods=["POST"])
def login():
  user = models.User.query.filter_by(email=request.json["email"]).first()
  if not user:
    return {
      'message': "User not found"
    }, 404
  # if user.password == request.json['password']:
  #with encruption
  if bcrypt.check_password_hash(user.password, request.json["password"]):
    encrypted_id = jwt.encode({"user_id":user.id}, os.environ.get("JWT_SECRET"), algorithm="HS256")
    return {
      "user": user.to_json(),
      "user_id": encrypted_id
    }
  else:
    return {
      "message": "Login failed"
    }, 401
      
# app.route('/users/login', methods=["POST"])(login())
    # try:
    #     user = models.User.query.filter_by(email=request.json["email"]).first()
    #     print(user)
    #     if not user:
    #         print('ok')
    #         return {"message": "User not found"},401

    #     # elif user.password == request.json["password"]:
    #     elif bcrypt.check_password_hash(user.password, request.json["password"]):
    #         encrypted_id = jwt.encode(
    #             {"user_id": user.id}, os.environ.get("JWT_SECRET"), algorithm="HS256"
    #         )
    #         return {"user": user.to_json(), "User_id": encrypted_id}

    #     else:
    #         return {"message": "password incorrect"},402
    # except Exception as e:
    #   print(e)
    #   return {"erorr": f"{e}"}

# not working
@app.route('/users/verify', methods=["GET"])
def verify_user():
  # print(request.headers) # => Authorusization: id
  decrypted_id = jwt.decode(request.headers["Authorization"], os.environ.get("JWT_SECRET"), algorithms=["HS256"])["user_id"]
  # user = models.User.query.filter_by(id=request.headers["Authorization"]).first() # How to look user up? We can't do it by request.json
  # print(user)
  user = models.User.query.filter_by(id=decrypted_id['id']).first()
  # if not user:
  #   return {
  #     "message": "user not found"
  #   }, 404
  if user:
    return {"user": user.to_json()}
  else:
    return {"message": "user not found"}, 404
  # return {"user": user.to_json()}




if __name__ == '__main__':
  port = os.environ.get('PORT') or 5000
  app.run('0.0.0.0', port=port, debug=True)