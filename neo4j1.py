from neo4j import GraphDatabase, basic_auth

def neo4jconnect(db):
        driver = GraphDatabase.driver("bolt://localhost:7687", auth = basic_auth("neo4j","12345"))
        session = driver.session(database = db)
        
        session.close()
        return session

''''
#spot check connection
if __name__ == '__main__':
    faculty = neo4jconnect('academicworld')
    print(faculty)

class Neo4jConnection:
    
    def __init__(self, uri, db):
        self.__uri = uri
        self.__db = db
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth= basic_auth("neo4j", "12345"))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
'''