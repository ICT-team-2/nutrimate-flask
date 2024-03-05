import configparser
import cx_Oracle


class OracleConnection():
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.result = self.config.read('oracle.ini', encoding='utf8')
        self.conn = cx_Oracle.connect(user=self.config['ORACLE']['USER'],
            password=self.config['ORACLE']['PASSWORD'],
            dsn=self.config['ORACLE']['URL'], encoding="UTF-8")
        self.cursor = self.conn.cursor()
    
    def connect(self):
        return self.conn
    
    def cursor(self):
        return self.cursor
    
    def close(self):
        self.cursor.close()
        self.conn.close()
    
    def commit(self):
        self.conn.commit()  # 삽입한 데이터 커밋
    
    def rollback(self):
        self.conn.rollback()
    
    def execute(self, sql):
        self.cursor.execute(sql)
    
    def fetchall(self):
        return self.cursor.fetchall()
    
    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchmany(self):
        return self.cursor.fetchmany()
    
    def __del__(self):
        self.close()
