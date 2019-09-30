from flask import url_for, g, abort, jsonify, request
from flask_login import current_user
from app import db
from app.api import bp
from app.models import User, Scan, PioneerBadge
from app.api.errors import bad_request
from app.api.auth import token_auth
import json
import random
import string

NEW_USER_NAME = 'new_user'

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    # only admins can view users
    if current_user.is_authenticated and not current_user.is_admin:
        return bad_request("user doesn't have admin rights")
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/scans/<int:id>', methods=['GET'])
@token_auth.login_required
def get_scan(id):
    return jsonify(Scan.query.get_or_404(id).to_dict())

def randomString(stringLength=6):
    """Generate random string with both lower- and upper-case letters"""
    return ''.join(random.choice(string.ascii_letters) for i in range(stringLength))

@bp.route('/scans', methods=['POST'])
@token_auth.login_required
def register_scan():
    data = request.get_json() or {}
    data = json.loads(data)

    if 'timestamp' not in data:
        return bad_request('must contain timestamp field')
    if 'badge_id' not in data:
        return bad_request('must contain badge id field')
    if 'device_name' not in data:
        return bad_request('must contain device_name')

    new_user = User.query.filter_by(username=NEW_USER_NAME).first()
    if new_user:
        new_user.username = '_'.join([new_user.username, randomString()])
        new_user.badge_id = data['badge_id']
        db.session.add(new_user)
        db.session.commit()
        response = jsonify(new_user.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_user', id=new_user.id)
        return response
    elif PioneerBadge.query.filter_by(badge_id=data['badge_id']).first():
        new_user = User()
        new_user.username = NEW_USER_NAME
        db.session.add(new_user)
        db.session.commit()
        response = jsonify(new_user.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_user', id=new_user.id)
        return response
    else:
        scan = Scan()
        scan.from_dict(data)
        db.session.add(scan)
        db.session.commit()
        response = jsonify(scan.to_dict())
        response.status_code = 201
        response.headers['Location'] = url_for('api.get_scan', id=scan.id)
        return response
