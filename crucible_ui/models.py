from crucible_ui import db
from datetime import datetime

class RoleAssignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    member_name = db.Column(db.String(100), nullable=False)
    role_id = db.Column(db.String(20), nullable=False)
    role_name = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"RoleAssignment('{self.member_name}', '{self.role_id}')"

class RoleStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.String(20), unique=True, nullable=False)
    role_name = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='PENDING')  # PENDING, CLAIMED
    assigned_to = db.Column(db.String(100), nullable=True)
    
    def __repr__(self):
        return f"RoleStatus('{self.role_id}', '{self.status}')"    