from flask import Blueprint, jsonify, request

from project.logics import MailLogics


mail_blueprint = Blueprint('mail', __name__)


@mail_blueprint.route('/mailer/send', methods=['POST'])
def send():
    data = request.get_json()

    MailLogics().send(data)

    return jsonify({
        'message': 'sended'
    })
