import os
from flask import Blueprint
from sql_provider import SQLProvider
from work_DB import *
from access import *


blueprint_order = Blueprint('bp_order', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/', methods=['GET', 'POST'])
@login_required
@group_validation
def order_index():
    if request.method == 'GET':
        sql = provider.get('basket.sql')
        items = select(current_app.config['db_config'], sql)
        if items == -1 or items is None:
            return render_template('db_error.html')
        basket = session.get('basket', {})
        return render_template('order_list.html', items=items, basket=basket)
    else:
        if 'Clear' in request.form:
            session.pop('basket', None)
        elif 'Decrease' in request.form:
            prod_id = request.form['ID']
            if session['basket'][prod_id]['amount'] == 1:
                session['basket'].pop(prod_id)
            else:
                session['basket'][prod_id]['amount'] -= 1
        else:
            if 'basket' not in session:
                session['basket'] = dict()
            prod_id = request.form['ID']
            if prod_id in session['basket']:
                session['basket'][prod_id]['amount'] += 1
            else:
                sql = provider.get('added.sql', prod_id=prod_id)
                item = select(current_app.config['db_config'], sql)
                if item == -1 or item is None:
                    return render_template('db_error.html')
                else:
                    item = item[0]
                session['basket'][prod_id] = {'amount': 1, 'Name': item['Name'], 'Price': item['Price']}
        session.permanent = True
        return redirect(url_for('.order_index'))


@blueprint_order.route('/confirm_order')
@login_required
def conf_order():
    basket = session.get('basket', None)
    if basket is None:
        return redirect(url_for('.order_index'))
    if session['user_group'] == 'None':
        us = 'out'
    else:
        us = 'in'
    revenu = 0
    dsql = ''
    for key in basket:
        revenu += basket[key]['amount']*basket[key]['Price']
        dsql += provider.get('insert_det.sql', id=key, price=basket[key]['Price'], amount=basket[key]['amount'], user_id=session['user_id'], us=us)
    session.pop('basket')
    sql = provider.get(f'insert_order_{us}.sql', id=session['user_id'], sum=revenu, us=us)
    sql += dsql
    ret = insert(current_app.config['db_config'], sql)
    return render_template('confirm_order.html', result=ret)
