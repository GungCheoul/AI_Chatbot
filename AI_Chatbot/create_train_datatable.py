import pymysql
from config.DB_Config import *

db = None
try:
    db = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASSWORD,
        db=DB_NAME,
        charset='utf8'
    )

    sql = '''
        CREATE TABLE IF NOT EXISTS chatbot_train_data (
        id INT UNSIGNED NOT NULL AUTO_INCREMENT,
        intent VARCHAR(45) NULL,
        answer TEXT NOT NULL,
        answer_add VARCHAR(2048) NULL,
        PRIMARY KEY (id))
    ENGINE = InnoDB DEFAULT CHARSET=utf8
    '''

    with db.cursor() as cursor:
        cursor.execute(sql)

except Exception as e:
    print(e)

finally:
    if db is not None:
        db.close()
