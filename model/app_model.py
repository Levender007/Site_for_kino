from work_DB import select
from sql_provider import SQLProvider
import os.path


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql/app'))


def home(db_conf):
    sql = provider.get('home_page.sql')
    ret = select(db_conf, sql)
    return ret


def film(db_config, n):
    sql = provider.get('film_info.sql', title=n)
    ret = select(db_config, sql)
    if ret is None or ret == -1:
        html = 'db_error.html'
        return html, ret
    ret = ret[0]
    sql = provider.get('seans_info.sql', title=n)
    ret['seans_info'] = select(db_config, sql)
    if ret['seans_info'] is None:
        html = 'db_error.html'
        return html, None
    else:
        html = 'film_info.html'
        return html, ret
