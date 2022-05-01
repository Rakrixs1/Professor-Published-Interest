import pymysql
import pandas as pd
  

def mysqlconnect(query):
        conn = pymysql.connect(
        host='127.0.0.1',
        port=int(3306),
        user='root',
        passwd='Lucky676',
        db='academicworld'
        )
      
        cur = conn.cursor()

        output = pd.read_sql(query, conn)
        
        conn.close()
        return output

'''
spot check if function is working
if __name__ == '__main__':
    faculty = mysqlconnect('select * from faculty limit 10')
    print(faculty)
'''






