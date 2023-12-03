from work_DB import select
from sql_provider import SQLProvider
from flask import current_app
import os.path


provider = SQLProvider(os.path.join(os.path.dirname(__file__), './sql/bp_auth'))


def login_check(db_config, user_id, ug):
    if ug is None:
        sql = provider.get('login_outer.sql', id=user_id)
        usg = 'user'
    else:
        sql = provider.get('login_inner.sql', id=user_id)
        usg = ug
    pr = select(db_config, sql)
    ret = {'login': pr[0]['Login'], 'user_group': usg}
    return ret


def auth_protocol(method, db_config, form):
    ret = dict()
    data = dict()
    if method == 'GET':
        html = 'input_auth.html'
    else:
        log = form['Login']
        pas = form['Pass']
        sql = provider.get('auth.sql', login=log, password=pas)
        pr = select(db_config, sql)
        if pr is None:
            html = 'non_res.html'
            return html, data, ret
        elif pr == -1:
            sql = provider.get('auth2.sql', login=log, password=pas)
            pr = select(db_config, sql)
            if pr is None:
                html = 'non_res.html'
                return html, data, ret
            elif pr == -1:
                html = 'input_auth.html'
                sql = provider.get('login_inner_check.sql', login=log)
                pr = select(db_config, sql)
                if pr is None:
                    html = 'non_res.html'
                    return html, data, ret
                elif pr == -1:
                    sql = provider.get('login_outer_check.sql', login=log)
                    pr = select(db_config, sql)
                    if pr is None:
                        html = 'non_res.html'
                        return html, data, ret
                    elif pr == -1:
                        ret = 1
                    else:
                        ret = 2
                else:
                    ret = 2
                return html, data, ret
            pr[0]['user_group'] = "None"
        html = 'auth_results.html'
        ug = pr[0]['user_group']
        if ug is "None":
            ug = 'user'
        current_app.config['db_config'] = current_app.config[f'{ug}_db_config.json']
        current_app.config['SECRET_KEY'] = os.urandom(20).hex()
        data['user_id'] = pr[0]['user_id']
        data['user_group'] = pr[0]['user_group']
        ret['Login'] = log
        ret['User_group'] = ug
    return html, data, ret
