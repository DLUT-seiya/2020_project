# coding:utf-8

'''
mysql数据操作模块
    完成数据模型对象的CRUD操作
'''
import pymysql


class DB_mysql:
    # database='db_mysql', host='localhost', port=3306, user='root', password='123456'
    # database='spider', host='192.168.0.240', port=3306, user='guowh', password='guowh20181127'
    def __init__(self,database='hivemeta', host='192.168.0.240', port=3306, user='guowh', password='guowh20181127', charset='utf8'):
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.charset = charset
        self.__get_cursor()

    def __get_cursor(self):
        # 创建和连接数据库
        self.__my_conn = pymysql.connect(
            database = self.database,
            host = self.host,
            port = self.port,
            user = self.user,
            password = self.password,
            charset = self.charset
        )
        # 获取游标对象
        self.__my_cursor = self.__my_conn.cursor()

    def create_tb(self,sql):
        # 创建表
        self.__my_cursor.execute(sql)
        self.__my_conn.commit()

    def create_index(self,sql):
        # 创建索引
        self.__my_cursor.execute(sql)
        self.__my_conn.commit()

    def insert(self, sql, params, flag=False):
        '''
        增加数据到数据库的方法
        :param sql: 操作的sql语句
        :param params: sql语句中的参数数据：有顺序的列表、元组
        :param flag: False：增加一条数据 True：一次增加多条数据
        :return: 返回执行的行数
        '''
        if not flag:
            rows = self.__my_cursor.execute(sql, params)
        else:
            rows = self.__my_cursor.executemany(sql, params)

        self.__my_conn.commit()
        return rows

    def select(self,sql):
        '''执行查询sql语句，返回查询到的所有数据'''
        self.__my_cursor.execute(sql)
        # 结果返回一个列表
        return self.__my_cursor.fetchall()

    def free(self):
        # 关闭数据库连接，释放资源

        if self.__my_cursor is not None:
            self.__my_cursor.close()
        if self.__my_conn is not None:
            self.__my_conn.close()


if __name__ == "__main__":
    # 构建一个数据操作对象
    db_mysql = DB_mysql()

    # 创建表和索引
    # create_tb_index(db_mysql)

    # create_tb_sql = '''CREATE TABLE baidu_search_key_range(
    #     id int PRIMARY KEY NOT NULL AUTO_INCREMENT,
    #     keyword varchar(200),
    #     word text,
    #     time varchar(200),
    #     num varchar(200));'''
    # db_mysql.create_tb(create_tb_sql)

    db_mysql.free()


