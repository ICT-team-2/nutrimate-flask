import configparser
import cx_Oracle


class OracleConnection():
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.result = self.config.read('oracle.ini', encoding='utf8')
        self.conn = cx_Oracle.connect(user=self.config['ORACLE']['USER'],
            password=self.config['ORACLE']['PASSWORD'],
            dsn=self.config['ORACLE']['URL'], encoding="UTF-8")
    
    def connect(self):
        return self.conn
    
    def cursor(self):
        return self.conn.cursor()
    
    def close(self):
        self.conn.close()
    
    def commit(self):
        self.conn.commit()  # 삽입한 데이터 커밋
    
    def rollback(self):
        self.conn.rollback()
    
    def __del__(self):
        self.close()
