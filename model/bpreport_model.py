from work_DB import *
from sql_provider import SQLProvider
import os.path


provider = SQLProvider(os.path.join(os.path.dirname(__file__), './sql/bp_report'))


def all_reports(db_config):
    html = 'report_menu.html'
    sql = provider.get('reports_list_for_menu.sql')
    res = select(db_config, sql)
    if res is None:
        html = 'db_error.html'
    elif res != -1:
        for rep in res:
            rep['href_name'] = rep['href_name'].split('; ')[0]
    return html, res


def operating_mode(db_config, proc):
    html = 'operating_mode.html'
    sql = provider.get('proc_desc.sql', proc=proc)
    res = select(db_config, sql)
    if res is None or res == -1:
        html = 'db_error.html'
    else:
        res = res[0]['href_name'].split('; ')[0]
    return html, res


def use_proc(db_config, proc, method, form):
    sql = provider.get('proc_desc.sql', proc=proc)
    res = select(db_config, sql)
    if res is None or res == -1 or res[0]['href_name'] == '':
        html = 'db_error.html'
        return html, None
    else:
        ret = [res[0]['href_name'].split('; ')[0], ]
    if method == 'GET':
        res = res[0]['href_name'].split('; ')[1]
        html = f"input_{res}.html"
    else:
        html = 'proc_res.html'
        res = call_proc(db_config, f'kino.{proc}', (form['date'], 0), (1,))
        if res is None:
            html = 'db_error.html'
            ret = None
        else:
            ret.append(res[0])
    return html, ret


def select_report(db_config, proc, method, form):
    sql = provider.get('proc_desc.sql', proc=proc)
    res = select(db_config, sql)
    if res is None or res == -1 or res[0]['href_name'] == '':
        html = 'db_error.html'
        return html, None
    else:
        ret = [res[0]['href_name'].split('; ')[0], ]
    if method == 'GET':
        res = res[0]['href_name'].split('; ')[1]
        html = f"input_{res}.html"
    else:
        html = 'report_res.html'
        sql = provider.get(f'select_{proc}.sql', date=form['date'])
        ret.append(select_tab(db_config, sql))
        if ret[1] is None:
            html = 'db_error.html'
            ret = None
    return html, ret
