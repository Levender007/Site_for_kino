from flask import Blueprint, render_template, session, request, current_app, redirect, url_for
from model.bpauth_model import *

blueprint_auth = Blueprint('bp_auth', __name__, template_folder='templates')


@blueprint_auth.route('/', methods=['GET', 'POST'])
def auth_index():
    if 'user_id' in session:
        html, ct = login_check(current_app.config['auth_db_config'], session['user_id'], session['user_group'])
    else:
        html, data, ct = auth_protocol(request.method, current_app.config['auth_db_config'], request.form)
        if 'user_id' in data:
            session['user_id'] = data['user_id']
            session['user_group'] = data['user_group']
            current_app.config['db_config'] = current_app.config[data['db_config']]
            current_app.config['SECRET_KEY'] = os.urandom(20).hex()
    return render_template(html, context=ct)


@blueprint_auth.route('/exit')
def logoff():
    if 'user_id' in session:
        session.clear()
    current_app.config['db_config'] = current_app.config['undefined_db_config.json']
    return redirect(url_for('main_menu'))
