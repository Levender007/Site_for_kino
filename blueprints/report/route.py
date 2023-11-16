from flask import Blueprint
from model.bpreport_model import *
from access import *


blueprint_report = Blueprint('bp_report', __name__, template_folder='templates')


@blueprint_report.route('/')
@login_required
@group_validation
def report_menu():
    html, ct = all_reports(current_app.config['report_db_config.json'])
    return render_template(html, context=ct)


@blueprint_report.route('/report/<proc>')
@login_required
def report(proc):
    if 'create_report' not in current_app.config['access.json'][session['user_group']]:
        return redirect(url_for('.see_report', proc=proc))
    html, ct = operating_mode(current_app.config['report_db_config.json'], proc)
    return render_template(html, proc=proc, title=ct)


@blueprint_report.route('/create-report/<proc>', methods=['GET', 'POST'])
@login_required
@group_validation
def create_report(proc):
    html, ct = use_proc(current_app.config['report_db_config.json'], proc, request.method, request.form)
    return render_template(html, context=ct, date=request.form.get('date', ''))


@blueprint_report.route('/see-report/<proc>', methods=['GET', 'POST'])
@login_required
@group_validation
def see_report(proc):
    html, ct = select_report(current_app.config['report_db_config.json'], proc, request.method, request.form)
    return render_template(html, context=ct, date=request.form.get('date', ''))
