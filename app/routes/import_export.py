from flask import Blueprint, request, jsonify, send_file
from datetime import datetime
from .auth import login_required, get_current_user_id
from ..models import db, Contact, ContactMethod
from ..utils.excel import export_contacts_to_excel, import_contacts_from_excel

import_export_bp = Blueprint('import_export', __name__)


@import_export_bp.route('/export', methods=['GET'])
@login_required
def export_contacts():
    """Export all contacts of current user to Excel"""
    user_id = get_current_user_id()
    
    contacts = Contact.query.filter_by(user_id=user_id).order_by(Contact.name).all()
    
    if not contacts:
        return jsonify({'error': '没有联系人可导出'}), 400
    
    # Generate Excel file
    excel_file = export_contacts_to_excel(contacts)
    
    # Generate filename with timestamp
    filename = f"通讯录_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    return send_file(
        excel_file,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name=filename
    )


@import_export_bp.route('/import', methods=['POST'])
@login_required
def import_contacts():
    """Import contacts from Excel file"""
    user_id = get_current_user_id()
    
    if 'file' not in request.files:
        return jsonify({'error': '请上传Excel文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400
    
    if not file.filename.endswith(('.xlsx', '.xls')):
        return jsonify({'error': '请上传Excel文件（.xlsx或.xls格式）'}), 400
    
    try:
        # Parse Excel file
        contacts_data = import_contacts_from_excel(file)
        
        if not contacts_data:
            return jsonify({'error': 'Excel文件中没有有效的联系人数据'}), 400
        
        # Import contacts
        imported_count = 0
        for contact_data in contacts_data:
            # Create contact
            contact = Contact(
                user_id=user_id,
                name=contact_data['name'],
                is_favorite=contact_data.get('is_favorite', False)
            )
            db.session.add(contact)
            db.session.flush()
            
            # Add contact methods
            for method_data in contact_data.get('methods', []):
                if method_data['type'] in ContactMethod.VALID_TYPES:
                    method = ContactMethod(
                        contact_id=contact.id,
                        type=method_data['type'],
                        value=method_data['value']
                    )
                    db.session.add(method)
            
            imported_count += 1
        
        db.session.commit()
        
        return jsonify({
            'message': f'成功导入 {imported_count} 个联系人',
            'imported_count': imported_count
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'导入失败: {str(e)}'}), 500
