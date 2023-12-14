from work_DB import select
from sql_provider import SQLProvider
import os.path


provider = SQLProvider(os.path.join(os.path.dirname(__file__), './sql/bp_auth'))


def login_check(db_config, user_id, ug):
    if ug == "None":
        sql = provider.get('login_outer.sql', id=user_id)
        usg = 'user'
    else:
        sql = provider.get('login_inner.sql', id=user_id)
        usg = ug
    pr = select(db_config, sql)
    if pr is None:
        return 'db_error.html', None
    else:
        ret = {'login': pr[0]['Login'], 'user_group': usg}
        return 'alredy_auth.html', ret


def auth_protocol(method, db_config, form):
    ret = dict()
    data = dict()
    if method == 'GET':
        html = 'input_auth.html'
    else:
        log = form['Login']
        pas = form['Pass']
        if log == "" or pas == "":
            return 'input_auth.html', [], 3
        sql = provider.get('auth.sql', login=log, password=pas)
        pr = select(db_config, sql)
        if pr is None:
            return 'db_error.html', [], None
        elif pr == -1:
            sql = provider.get('auth2.sql', login=log, password=pas)
            pr = select(db_config, sql)
            if pr is None:
                return 'db_error.html', [], None
            elif pr == -1:
                html = 'input_auth.html'
                sql = provider.get('login_inner_check.sql', login=log)
                pr = select(db_config, sql)
                if pr is None:
                    return 'db_error.html', [], None
                elif pr == -1:
                    sql = provider.get('login_outer_check.sql', login=log)
                    pr = select(db_config, sql)
                    if pr is None:
                        return 'db_error.html', [], None
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
        data['user_id'] = pr[0]['user_id']
        data['user_group'] = pr[0]['user_group']
        data['db_config'] = f'{ug}_db_config.json'
        ret['Login'] = log
        ret['User_group'] = ug
    return html, data, ret
