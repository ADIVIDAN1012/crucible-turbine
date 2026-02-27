from flask import jsonify, request, render_template, redirect, url_for
from crucible_ui import app, db
from crucible_ui.models import RoleAssignment, RoleStatus
import json

# API endpoint to submit role selection
@app.route('/api/select-role', methods=['POST'])
def select_role():
    try:
        data = request.get_json()
        
        member_name = data.get('memberName')
        role_id = data.get('selectedRole')
        timestamp = data.get('timestamp')
        
        if not member_name or not role_id:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Check if role is already claimed
        role_status = RoleStatus.query.filter_by(role_id=role_id).first()
        if role_status and role_status.status == 'CLAIMED':
            return jsonify({'success': False, 'message': f'Role {role_id} has already been claimed'}), 400
        
        # Create new role assignment
        assignment = RoleAssignment(
            member_name=member_name,
            role_id=role_id,
            role_name=get_role_name(role_id)
        )
        db.session.add(assignment)
        
        # Update role status
        if role_status:
            role_status.status = 'CLAIMED'
            role_status.assigned_to = member_name
        else:
            role_status = RoleStatus(
                role_id=role_id,
                role_name=get_role_name(role_id),
                status='CLAIMED',
                assigned_to=member_name
            )
            db.session.add(role_status)
        
        db.session.commit()
        
        return jsonify({'success': True, 'message': f'Successfully assigned {role_id} to {member_name}'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to get all role assignments
@app.route('/api/assignments', methods=['GET'])
def get_assignments():
    try:
        assignments = RoleAssignment.query.all()
        assignments_data = []
        
        for assignment in assignments:
            assignments_data.append({
                'id': assignment.id,
                'member_name': assignment.member_name,
                'role_id': assignment.role_id,
                'role_name': assignment.role_name,
                'timestamp': assignment.timestamp.isoformat()
            })
        
        return jsonify({'success': True, 'data': assignments_data}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# API endpoint to get role statuses
@app.route('/api/roles', methods=['GET'])
def get_roles():
    try:
        roles = RoleStatus.query.all()
        roles_data = []
        
        for role in roles:
            roles_data.append({
                'role_id': role.role_id,
                'role_name': role.role_name,
                'status': role.status,
                'assigned_to': role.assigned_to
            })
        
        # Add unclaimed roles
        all_roles = ['PRID_1', 'PRID_2', 'PRID_3', 'PRID_4', 'PRID_5']
        existing_role_ids = [role.role_id for role in roles]
        
        for role_id in all_roles:
            if role_id not in existing_role_ids:
                roles_data.append({
                    'role_id': role_id,
                    'role_name': get_role_name(role_id),
                    'status': 'PENDING' if role_id != 'PRID_1' else 'RESERVED',
                    'assigned_to': 'Aditya Sadhu' if role_id == 'PRID_1' else None
                })
        
        return jsonify({'success': True, 'data': roles_data}), 200
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

# Helper function to get role name
def get_role_name(role_id):
    role_names = {
        'PRID_1': 'Supervisor',
        'PRID_2': 'Auditor',
        'PRID_3': 'Designer',
        'PRID_4': 'Integrator',
        'PRID_5': 'DBA'
    }
    return role_names.get(role_id, 'Unknown')

# Initialize default roles
def init_roles():
    # Check if roles already exist
    existing_roles = RoleStatus.query.all()
    if len(existing_roles) == 0:
        # Create default role statuses
        default_roles = [
            {'role_id': 'PRID_1', 'role_name': 'Supervisor', 'status': 'RESERVED', 'assigned_to': 'Aditya Sadhu'},
            {'role_id': 'PRID_2', 'role_name': 'Auditor', 'status': 'PENDING', 'assigned_to': None},
            {'role_id': 'PRID_3', 'role_name': 'Designer', 'status': 'PENDING', 'assigned_to': None},
            {'role_id': 'PRID_4', 'role_name': 'Integrator', 'status': 'PENDING', 'assigned_to': None},
            {'role_id': 'PRID_5', 'role_name': 'DBA', 'status': 'PENDING', 'assigned_to': None}
        ]
        
        for role_data in default_roles:
            role = RoleStatus(**role_data)
            db.session.add(role)
        
        db.session.commit()

# Function to sync workspace headers (as referenced in run.py)
def sync_workspace_headers():
    with app.app_context():
        db.create_all()
        init_roles()