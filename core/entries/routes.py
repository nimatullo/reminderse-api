from core.entries.service import EntryService
from datetime import datetime

from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required

from core import daily_email
from core.api.users.service import UserService

entries = Blueprint('entries', __name__)
service = EntryService()
user_service = UserService()


@entries.route("/api/link/add", methods=["POST"])
@jwt_required
def add_link():
    if request.is_json:
        entry_title = request.json.get('entry_title')
        url = request.json.get('url')
        category = request.json.get('category')
        date_of_next_send = request.json.get('date_of_next_send')
        if date_of_next_send:
            if datetime.strptime(date_of_next_send, '%Y-%m-%d') < datetime.now():
                return make_response(jsonify({"message": "Invalid date"}), 400)

        return service.add_link(entry_title, url, category, date_of_next_send)


@entries.route("/api/text/add", methods=["POST"])
@jwt_required
def add_text():
    if request.is_json:
        entry_title = request.json.get('entry_title')
        text_content = request.json.get('text_content')
        category = request.json.get('category')
        date_of_next_send = request.json.get('date_of_next_send')
        if date_of_next_send:
            if datetime.strptime(date_of_next_send, '%Y-%m-%d') < datetime.now():
                return make_response(jsonify({"message": "Invalid date"}), 400)

        return service.add_text(entry_title=entry_title, content=text_content, category_title=category, date_of_next_send=date_of_next_send)


@entries.route('/api/link/list', methods=['GET'])
@jwt_required
def all_links():
    CURRENT_USER = user_service.get_current_user()
    return service.get_all_links(CURRENT_USER.id)


@entries.route('/api/text/list', methods=['GET'])
@jwt_required
def all_texts():
    CURRENT_USER = user_service.get_current_user()
    return service.get_all_text(CURRENT_USER.id)


@entries.route("/api/link/<link_id>", methods=["PUT"])
@jwt_required
def edit_link_api(link_id):
    CURRENT_USER = user_service.get_current_user()
    entry_title = request.json.get('entry_title')
    url = request.json.get('url')
    category = request.json.get('category')
    date = request.json.get('date')
    return service.update_link(link_id,
                               CURRENT_USER.id,
                               entry_title,
                               url,
                               category,
                               date)


@entries.route("/api/text/<text_id>", methods=["PUT"])
@jwt_required
def edit_text_api(text_id):
    CURRENT_USER = user_service.get_current_user()
    entry_title = request.json.get('entry_title')
    text_content = request.json.get('text_content')
    category = request.json.get('category')
    date = request.json.get('date')
    return service.update_text(text_id,
                               CURRENT_USER.id,
                               entry_title,
                               text_content,
                               category,
                               date)


@entries.route('/api/link/<link_id>', methods=['GET'])
@jwt_required
def get_link(link_id):
    return service.get_link(link_id)


@entries.route('/api/text/<text_id>', methods=['GET'])
@jwt_required
def get_text(text_id):
    return service.get_text(text_id)


@entries.route('/api/link/<link_id>/pause', methods=["PUT"])
@jwt_required
def pause_link(link_id):
    return service.pause_link(link_id)


@entries.route('/api/text/<text_id>/pause', methods=["PUT"])
@jwt_required
def pause_text(text_id):
    return service.pause_text(text_id)


@entries.route('/api/link/<link_id>/resume', methods=["PUT"])
@jwt_required
def resume_link(link_id):
    return service.resume_link(link_id)


@entries.route('/api/text/<text_id>/resume', methods=["PUT"])
@jwt_required
def resume_text(text_id):
    return service.resume_text(text_id)


@entries.route('/api/link/<link_id>', methods=['DELETE'])
@jwt_required
def delete_link(link_id):
    return service.delete_link(link_id)


@entries.route('/api/text/<text_id>', methods=['DELETE'])
@jwt_required
def delete_text(text_id):
    return service.delete_text(text_id)


@entries.route('/api/entries/send', methods=["POST"])
def send_entries():
    emails_sent = daily_email.send_to_each_user()
    email_list = []
    for user in emails_sent:
        email_list.append({
            "email": user.email,
            "username": user.username
        })
    return make_response(
        jsonify({
            "data": "EMAILS SENT SUCCESSFULLY",
            "number_of_emails": f'{len(emails_sent)} emails sent.',
            "email_list": email_list
        })
    )
