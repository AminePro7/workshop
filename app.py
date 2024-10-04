from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL configurations
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', 'root')
MYSQL_DB = os.getenv('MYSQL_DB', 'workshop')

# SQLAlchemy Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Create a model for 'users' table
class User(db.Model):
    __tablename__ = 'users'  # Specify the table name

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)

# Create operation
@app.route('/add_user', methods=['POST'])
def add_user():
    firstname = request.json['firstname']
    email = request.json['email']
    new_user = User(firstname=firstname, email=email)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully!'})

# Read operation
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'firstname': user.firstname, 'email': user.email} for user in users])

# Read operation by id
@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify({'id': user.id, 'firstname': user.firstname, 'email': user.email})
    else:
        return jsonify({'message': 'User not found'}), 404

# Update operation
@app.route('/update_user/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    user.firstname = request.json['firstname']
    user.email = request.json['email']
    db.session.commit()
    return jsonify({'message': 'User updated successfully!'})

# Delete operation
@app.route('/delete_user/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully!'})

@app.route('/')
def hello_world():
    return f'Hello, from flask app!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Creates all tables based on models
    app.run(debug=True, host=os.environ.get('FLASK_RUN_HOST', '0.0.0.0'), port=int(os.environ.get('FLASK_RUN_PORT', 5000)))
