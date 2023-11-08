from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root@localhost/mydb'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())


@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []

    for user in users:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        user_list.append(user_data)

    return jsonify(user_list)

@app.route('/users/<username>', methods=['GET'])
def get_user_by_username(username):
    user = User.query.filter(User.username.ilike(username)).first()
    if user:
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
        return jsonify(user_data)
    else:
        return jsonify({"error": "User not found"}), 404


@app.route('/users', methods=['POST'])
def create_user():
    try:
        # Parse the JSON data from the request
        data = request.get_json()

        # Create a new user object
        new_user = User(
            username=data['username'],
            email=data['email']
        )

        # Add the new user to the session and commit the changes to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400  # Bad Request


@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    else:
        return jsonify({"error": "User not found"}), 404  # Not Found


app.run(port=3000)
