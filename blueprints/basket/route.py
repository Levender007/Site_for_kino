import os
from flask import Blueprint
from sql_provider import SQLProvider
from work_DB import *
from access import *


blueprint_order = Blueprint('bp_order', __name__, template_folder='templates')
provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))


@blueprint_order.route('/<seansID>', methods=['GET', 'POST'])
@login_required
@group_validation
def order_index(seansID):
    if request.method == 'GET':
        basket = session.get(f'basket{seansID}', {})
        if len(basket.keys()) == 0:
            bas = (-1, -2)
        elif len(basket.keys()) == 1:
            bas = list(basket.keys())
            bas = (bas[0], -1)
        else:
            bas = tuple(basket.keys())
        sql = provider.get('basket.sql', bas=bas, id=seansID)
        items = select(current_app.config['db_config'], sql)
        sql = provider.get('seans_info.sql', id=seansID)
        seans = select(current_app.config['db_config'], sql)
        if items is None or seans == -1 or seans is None:
            return render_template('db_error.html')
        return render_template('order_list.html', items=items, basket=basket, seans=seans[0])
    else:
        if 'Clear' in request.form:
            session.pop(f'basket{seansID}', None)
        elif 'Decrease' in request.form:
            session[f'basket{seansID}'].pop(request.form['ID'])
        else:
            if f'basket{seansID}' not in session:
                session[f'basket{seansID}'] = dict()
            prod_id = request.form['ID']
            if prod_id not in session[f'basket{seansID}']:
                sql = provider.get('added.sql', prod_id=prod_id)
                item = select(current_app.config['db_config'], sql)
                if item == -1 or item is None:
                    return render_template('db_error.html')
                else:
                    item = item[0]
                session[f'basket{seansID}'][prod_id] = {'RowOfSeat': item['RowOfSeat'], 'Seat': item['Seat'], 'Price': item['Price']}
        session.permanent = True
        return redirect(url_for('.order_index', seansID=seansID))


@blueprint_order.route('/confirm_order/<seansID>')
@login_required
def conf_order(seansID):
    basket = session.get(f'basket{seansID}', None)
    if basket is None:
        return redirect(url_for('.order_index', seansID=seansID))
    if session['user_group'] == 'None':
        us = 'out'
    else:
        us = 'in'
    revenu = 0
    sql = ['', '']
    for key in basket:
        revenu += basket[key]['Price']
        buf = provider.get('insert_det.sql', id=key, price=basket[key]['Price'], user_id=session['user_id'], us=us).split(';')
        sql.append(buf[0])
        sql.append(buf[1])
    session.pop(f'basket{seansID}')
    buf = provider.get(f'insert_order_{us}.sql', id=session['user_id'], sum=revenu, us=us).split(';')
    sql[0] = buf[0]
    sql[1] = buf[1]
    ret = multi_execute(current_app.config['db_config'], sql)
    return render_template('confirm_order.html', result=ret)
