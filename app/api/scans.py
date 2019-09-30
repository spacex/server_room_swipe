from flask import url_for, g, abort, jsonify, request
from flask_login import current_user
from app import db
from app.api import bp
from app.models import User, Scan
from app.api.errors import bad_request
from app.api.auth import token_auth
import json

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

@bp.route('/users', methods=['POST'])
@token_auth.login_required
def create_user():
    # only admins can add users
    if current_user.is_authenticated and not current_user.is_admin:
        return bad_request("user doesn't have admin rights")
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data or 'badge_id' not in data:
        return bad_request('must include username, badge_id and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/scans', methods=['POST'])
@token_auth.login_required
def register_scan():
    data = request.get_json() or {}
    data = json.loads(data)

    if 'timestamp' not in data or 'badge_id' not in data:
        return bad_request('must contain timestamp and badge id fields')
    user = User.query.filter_by(badge_id=data['badge_id']).first()
    if not user:
        return bad_request('unknown badge_id')
    if 'username' not in data:
        data['username'] = user.username
    if 'device_name' not in data:
        return bad_request('must contain device_name')

    scan = Scan()
    scan.from_dict(data)
    db.session.add(scan)
    db.session.commit()
    response = jsonify(scan.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_scan', id=scan.id)
    return response


