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
    pr = select(db_config, sql)
    ret = pr[0]
    if pr is None or pr == -1:
        html = 'non_film_res.html'
        return html, ret
    sql = provider.get('seans_info.sql', title=n)
    pr = select(db_config, sql)
    ret['seans_info'] = pr
    if pr is None:
        html = 'non_film_res.html'
        return html, ret
    else:
        html = 'film_info.html'
        return html, ret
