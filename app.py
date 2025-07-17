from flask import Flask, request, jsonify
from models.user import User
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user,login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)

#view login
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return jsonify({'message': 'Login successful'}), 200      
    
    return jsonify({'message': 'Invalid credentials'}), 401

#logout
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})
    
#cadastro dos usuarios

@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    if username and password:
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    
    return jsonify({'message': 'Invalid input'}), 400   

@app.route('/user/<int:user_id>', methods=['GET'])
@login_required
def read_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username}), 200
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    
    if user:
        username = data.get('username')
        password = data.get('password')
        
        if username:
            user.username = username
        if password:
            user.password = password
        
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    
    return jsonify({'message': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
@login_required 
def delete_user(user_id):
    user = User.query.get(user_id)
    
    if user_id == current_user.id:
        return jsonify({'message': 'You cannot delete your own account'}), 403
    
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    
    return jsonify({'message': 'User not found'}), 404  

@app.route('/hello-world', methods=['GET'])
def hello_world():
    return 'Hello, World!'
  
if __name__ == '__main__':
    app.run(debug=True)