from DBCM import DBConnect


def select(config: dict, _sql: str):
    with DBConnect(config) as cur:
        cur.execute(_sql)
        res = cur.fetchall()
        if res is None:
            return None
        elif len(res) == 0:
            return -1
        else:
            schema = [item[0] for item in cur.description]
            res_dict = []
            for product in res:
                res_dict.append(dict(zip(schema, product)))
            return res_dict


def select_tab(config: dict, _sql: str):
    with DBConnect(config) as cur:
        cur.execute(_sql)
        res = cur.fetchall()
        if res is None:
            return None
        elif len(res) == 0:
            return -1
        else:
            schema = [item[0] for item in cur.description]
            res_dict = [schema, ]
            for product in res:
                res_dict.append(product)
            return res_dict


def select_distinct(config: dict, sql: str):
    with DBConnect(config) as cur:
        cur.execute(sql)
        res = cur.fetchall()
        if res is None:
            return None
        elif len(res) == 0:
            return -1
        else:
            res_tuple = []
            for buf in res:
                res_tuple.append(buf[0])
            res_tuple = tuple(res_tuple)
            return res_tuple


def call_proc(config: dict, proc: str, args=(), argpos=()):
    if len(argpos) > 0 and max(argpos) >= len(args):
        return None
    res = []
    with DBConnect(config) as cur:
        cur.callproc(proc, args)
        for i in argpos:
            cur.execute(f'select @_{proc}_{i}')
            one = cur.fetchone()
            if one is None or len(one) == 0:
                return None
            res.append(one[0])
    if len(res) == 0:
        return 0
    else:
        return res


def insert(config: dict, sql: str):
    res = 1
    with DBConnect(config) as cur:
        cur.execute(sql)
        res = 0
    return res


if __name__ == '__main__':
    print('Debug mode')
