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


def select_distinct(config: dict, sql: str):
    with DBConnect(config) as cur:
        cur.execute(sql)
        res = cur.fetchall()
        if res is not None:
            res_tuple = []
            for buf in res:
                res_tuple.append(buf[0])
            res_tuple = tuple(res_tuple)
            return res_tuple
        else:
            return None


if __name__ == '__main__':
    print('Debug mode')
