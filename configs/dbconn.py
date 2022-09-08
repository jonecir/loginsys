#!python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DBConnectionHandler:

    def __init__(self) -> None:
        self.__connection_string = 'mysql+pymysql://root:admin01@localhost:3306/loginsys'
        self.__engine = self.__create_db_engine()
        self.session = None

    def __create_db_engine(self):
        engine = create_engine(self.__connection_string)
        return engine

    #Caso precise executar cmds SQL

    def __get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
