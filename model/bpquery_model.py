from work_DB import select
from sql_provider import SQLProvider
import os.path


provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql/bp_query'))


def big_zal(db_config, m, f):
    html = 'big_zal.html'
    sql = provider.get('biggest_zal_info.sql')
    ret = select(db_config, sql)
    if ret is None or ret == -1:
        return html, ret
    else:
        return html, ret[0]


def max_seats(db_config, m, f):
    html = 'max_seats.html'
    sql = provider.get('max_seats.sql')
    ret = select(db_config, sql)
    if ret is None or ret == -1:
        return html, ret
    else:
        return html, ret[0]


def month_by_day_revenu(db_config, method, form):
    if method == 'GET':
        html = 'input_year_month.html'
        ret = None
    else:
        html = 'month_by_day_revenu.html'
        sql = provider.get('month_by_day_revenu.sql', y=form['year'], m=form['month'])
        res = select(db_config, sql)
        ret = {'year': form['year'], 'month': form['month'], 'result': res}
    return html, ret


def non_seans_zal(db_config, m, f):
    html = 'non_seans_zal.html'
    sql = provider.get('non_seans_zal_info.sql')
    ret = select(db_config, sql)
    return html, ret


def seans_count_in_zal(db_config, method, form):
    if method == 'GET':
        html = 'input_year_month.html'
        ret = None
    else:
        html = 'seans_count_in_zal.html'
        sql = provider.get('seans_count_in_zal_in_month.sql', y=form['year'], m=form['month'])
        res = select(db_config, sql)
        ret = {'year': form['year'], 'month': form['month'], 'result': res}
    return html, ret


def seans_for_days(db_config, method, form):
    if method == 'GET':
        html = 'input_day.html'
        ret = None
    else:
        html = 'seans_for_days.html'
        sql = provider.get('seans_info_for_days_ago.sql', d=form['days'])
        res = select(db_config, sql)
        ret = {'days': form['days'], 'result': res}
    return html, ret


def seans_info_in_month(db_config, method, form):
    if method == 'GET':
        html = 'input_year_month.html'
        ret = None
    else:
        html = 'seans_info_in_month.html'
        sql = provider.get('seans_info_in_month.sql', y=form['year'], m=form['month'])
        res = select(db_config, sql)
        ret = {'year': form['year'], 'month': form['month'], 'result': res}
    return html, ret


def seans_sold_in_day(db_config, method, form):
    if method == 'GET':
        html = 'input_year_month_day.html'
        ret = None
    else:
        html = 'seans_sold_in_day.html'
        sql = provider.get('seans_sold_in_day.sql', y=form['year'], m=form['month'], d=form['day'])
        res = select(db_config, sql)
        ret = {'year': form['year'], 'month': form['month'], 'day': form['day'], 'result': res}
    return html, ret


def zal_base_price(db_config, m, f):
    html = 'zal_base_price.html'
    sql = provider.get('zal_base_price.sql')
    ret = select(db_config, sql)
    return html, ret
