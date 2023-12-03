import pymysql.cursors
from pymysql.constants import CLIENT


class DBConnect:
    def __init__(self, config: dict):
        self.config = config
        self.config["client_flag"] = CLIENT.MULTI_STATEMENTS
        self.DB = None
        self.cursor = None

    def __enter__(self):
        try:
            self.DB = pymysql.connect(**self.config)
            self.cursor = self.DB.cursor()
            if self.cursor is None:
                raise ValueError("Курсор не создан")
            self.DB.begin()
            return self.cursor
        except Exception as err:
            print(err.args)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_type)
            print(exc_val)
            print(exc_tb)
        if self.DB and self.cursor:
            if exc_type:
                self.DB.rollback()
            else:
                self.DB.commit()
            self.cursor.close()
            self.DB.close()
        return True


if __name__ == "__main__":
    print("Debug mod")
