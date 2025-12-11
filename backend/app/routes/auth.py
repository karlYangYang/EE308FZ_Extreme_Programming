from flask import Blueprint, request, jsonify, session
from functools import wraps
from ..models import db, User

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    """Decorator to require login via session"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': '请先登录'}), 401
        return f(*args, **kwargs)
    return decorated_function


def get_current_user_id():
    """Get current logged in user ID from session"""
    return session.get('user_id')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    if not data:
        return jsonify({'error': '请提供注册信息'}), 400
    
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not username or not email or not password:
        return jsonify({'error': '用户名、邮箱和密码都是必填项'}), 400
    
    if len(username) < 3:
        return jsonify({'error': '用户名至少需要3个字符'}), 400
    
    if len(password) < 6:
        return jsonify({'error': '密码至少需要6个字符'}), 400
    
    # Check if user already exists
    if User.query.filter_by(username=username).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': '邮箱已被注册'}), 400
    
    # Create new user
    user = User(username=username, email=email)
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    # Set session
    session.permanent = True
    session['user_id'] = user.id
    
    return jsonify({
        'message': '注册成功',
        'user': user.to_dict()
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请提供登录信息'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': '请输入用户名和密码'}), 400
    
    # Find user by username or email
    user = User.query.filter(
        (User.username == username) | (User.email == username)
    ).first()
    
    if not user or not user.check_password(password):
        return jsonify({'error': '用户名或密码错误'}), 401
    
    # Set session
    session.permanent = True
    session['user_id'] = user.id
    
    return jsonify({
        'message': '登录成功',
        'user': user.to_dict()
    }), 200


@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged in user info"""
    user_id = get_current_user_id()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    return jsonify({'user': user.to_dict()}), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """User logout"""
    session.clear()
    return jsonify({'message': '登出成功'}), 200
