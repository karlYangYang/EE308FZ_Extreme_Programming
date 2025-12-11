from flask import Blueprint, request, jsonify
from .auth import login_required, get_current_user_id
from ..models import db, Contact, ContactMethod

contacts_bp = Blueprint('contacts', __name__)


@contacts_bp.route('', methods=['GET'])
@login_required
def get_contacts():
    """Get all contacts for current user"""
    user_id = get_current_user_id()
    
    # Optional filter by favorite
    favorite_only = request.args.get('favorite', '').lower() == 'true'
    
    # Optional search by name
    search = request.args.get('search', '').strip()
    
    query = Contact.query.filter_by(user_id=user_id)
    
    if favorite_only:
        query = query.filter_by(is_favorite=True)
    
    if search:
        query = query.filter(Contact.name.ilike(f'%{search}%'))
    
    contacts = query.order_by(Contact.is_favorite.desc(), Contact.name).all()
    
    return jsonify({
        'contacts': [contact.to_dict() for contact in contacts],
        'total': len(contacts)
    }), 200


@contacts_bp.route('', methods=['POST'])
@login_required
def create_contact():
    """Create a new contact"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    if not data:
        return jsonify({'error': '请提供联系人信息'}), 400
    
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': '联系人姓名是必填项'}), 400
    
    # Create contact
    contact = Contact(
        user_id=user_id,
        name=name,
        is_favorite=data.get('is_favorite', False)
    )
    db.session.add(contact)
    db.session.flush()  # Get the contact ID
    
    # Add contact methods if provided
    methods = data.get('methods', [])
    for method_data in methods:
        method_type = method_data.get('type', '').strip()
        method_value = method_data.get('value', '').strip()
        
        if method_type and method_value:
            if method_type not in ContactMethod.VALID_TYPES:
                continue
            method = ContactMethod(
                contact_id=contact.id,
                type=method_type,
                value=method_value
            )
            db.session.add(method)
    
    db.session.commit()
    
    return jsonify({
        'message': '联系人创建成功',
        'contact': contact.to_dict()
    }), 201


@contacts_bp.route('/<int:contact_id>', methods=['GET'])
@login_required
def get_contact(contact_id):
    """Get a single contact"""
    user_id = get_current_user_id()
    
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    if not contact:
        return jsonify({'error': '联系人不存在'}), 404
    
    return jsonify({'contact': contact.to_dict()}), 200


@contacts_bp.route('/<int:contact_id>', methods=['PUT'])
@login_required
def update_contact(contact_id):
    """Update a contact"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    if not contact:
        return jsonify({'error': '联系人不存在'}), 404
    
    if not data:
        return jsonify({'error': '请提供更新信息'}), 400
    
    # Update name if provided
    if 'name' in data:
        name = data['name'].strip()
        if name:
            contact.name = name
    
    # Update favorite status if provided
    if 'is_favorite' in data:
        contact.is_favorite = bool(data['is_favorite'])
    
    db.session.commit()
    
    return jsonify({
        'message': '联系人更新成功',
        'contact': contact.to_dict()
    }), 200


@contacts_bp.route('/<int:contact_id>', methods=['DELETE'])
@login_required
def delete_contact(contact_id):
    """Delete a contact"""
    user_id = get_current_user_id()
    
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    if not contact:
        return jsonify({'error': '联系人不存在'}), 404
    
    db.session.delete(contact)
    db.session.commit()
    
    return jsonify({'message': '联系人删除成功'}), 200


@contacts_bp.route('/<int:contact_id>/favorite', methods=['POST'])
@login_required
def toggle_favorite(contact_id):
    """Toggle favorite status of a contact"""
    user_id = get_current_user_id()
    
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    if not contact:
        return jsonify({'error': '联系人不存在'}), 404
    
    # Toggle favorite status
    contact.is_favorite = not contact.is_favorite
    db.session.commit()
    
    return jsonify({
        'message': '收藏状态更新成功',
        'contact': contact.to_dict()
    }), 200


@contacts_bp.route('/<int:contact_id>/methods', methods=['POST'])
@login_required
def add_contact_method(contact_id):
    """Add a contact method to a contact"""
    user_id = get_current_user_id()
    data = request.get_json()
    
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    if not contact:
        return jsonify({'error': '联系人不存在'}), 404
    
    if not data:
        return jsonify({'error': '请提供联系方式信息'}), 400
    
    method_type = data.get('type', '').strip()
    method_value = data.get('value', '').strip()
    
    if not method_type or not method_value:
        return jsonify({'error': '联系方式类型和值都是必填项'}), 400
    
    if method_type not in ContactMethod.VALID_TYPES:
        return jsonify({'error': f'无效的联系方式类型，有效类型: {", ".join(ContactMethod.VALID_TYPES)}'}), 400
    
    method = ContactMethod(
        contact_id=contact.id,
        type=method_type,
        value=method_value
    )
    db.session.add(method)
    db.session.commit()
    
    return jsonify({
        'message': '联系方式添加成功',
        'method': method.to_dict(),
        'contact': contact.to_dict()
    }), 201


@contacts_bp.route('/<int:contact_id>/methods/<int:method_id>', methods=['DELETE'])
@login_required
def delete_contact_method(contact_id, method_id):
    """Delete a contact method"""
    user_id = get_current_user_id()
    
    contact = Contact.query.filter_by(id=contact_id, user_id=user_id).first()
    if not contact:
        return jsonify({'error': '联系人不存在'}), 404
    
    method = ContactMethod.query.filter_by(id=method_id, contact_id=contact_id).first()
    if not method:
        return jsonify({'error': '联系方式不存在'}), 404
    
    db.session.delete(method)
    db.session.commit()
    
    return jsonify({
        'message': '联系方式删除成功',
        'contact': contact.to_dict()
    }), 200
