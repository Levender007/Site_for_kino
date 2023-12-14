from flask import Blueprint
from model import bpquery_model
from access import *


blueprint_query = Blueprint('bp_query', __name__, template_folder='templates')


@blueprint_query.route('/')
@login_required
@group_validation
def menu():
    return render_template('menu.html')


@blueprint_query.route('/<func>', methods=['GET', 'POST'])
@login_required
@group_validation
def query(func):
    f = getattr(bpquery_model, func)
    html, ct = f(current_app.config['db_config'], request.method, request.form)
    return render_template(html, context=ct)
