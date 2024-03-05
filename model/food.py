import cx_Oracle
import csv

from oracle_connection import OracleConnection
# db -> csv로 데이터 추출하는 코드(중요x)
oracle = OracleConnection()
# 오라클 데이터베이스 연결 설정
connection = oracle.connect()
# 데이터베이스 버전 확인
print(connection.version)


# CSV 파일을 읽어 Oracle DB에 입력하기 위한 함수 정의
def insert_data_from_csv(file_path, connection):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # 첫 번째 행(해더) 건너뛰기
        
        with connection.cursor() as cursor:
            for row in reader:
                # SQL 쿼리 준비, 테이블명과 컬럼명을 정확히 지정해야 함
                insert_query = """
                INSERT INTO food
                (food_id, food_name, food_group, food_intake, intake_unit,
                food_cal, food_protein, food_carbo, food_provi, food_salt, food_chole)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)
                """
                
                # 데이터 삽입
                cursor.execute(insert_query, row)
            
            # 삽입한 데이터 커밋
            connection.commit()


# CSV 파일 경로 지정 및 데이터 삽입 함수 호출
insert_data_from_csv('../food.csv', connection)

# 연결 종료
connection.close()
