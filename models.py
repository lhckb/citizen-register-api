from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.traversals import ColIdentityComparatorStrategy

engine = create_engine('sqlite:///citizens.db')
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Citizens(Base):
    __tablename__ = 'citizens'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    surname = Column(String(80), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    email = Column(String(50), unique=True)
    cellphone = Column(String(25), unique=True, nullable=False)
    cep = Column(String(9), nullable=False)
    street = Column(String(40))
    neighbourhood = Column(String(25))
    city = Column(String(40), nullable=False)
    state = Column(String(40))

    def __repr__(self):
        return f'''{self.surname}, {self.name} /
    CPF: {self.cpf} / Phone: {self.cellphone} / CEP: {self.cep} /
    Address line 1: {self.street}'''

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

    
def initDatabase():
    Base.metadata.create_all(bind = engine)

if __name__ == '__main__':
    initDatabase()