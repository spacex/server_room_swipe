from flask import url_for, g, abort, jsonify, request
from app import db
from app.api import bp
from app.models import User, Badge, Scan
from app.api.errors import bad_request
from app.api.auth import token_auth

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'password' not in data:
        return bad_request('must include username, email and password fields')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('please use a different username')
    if User.query.filter_by(email=data['email']).first():
        return bad_request('please use a different email address')
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

@bp.route('/scans', methods=['POST'])
def register_scan():
    data = request.get_json() or {}
    if 'timestamp' not in data or 'badge_id' not in data:
        return bad_request('must contain timestamp and badge id fields')
    if not Badge.query.filter_by(id=data['badge_id']).first():
        return bad_request('unknown badge_id')
    this_scan = Scan()
    this_scan.from_dict(data)
    db.session.add(this_scan)
    db.session.commit()
    response = jsonify(this_scan.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_scan', id=scan.id)
    return response


