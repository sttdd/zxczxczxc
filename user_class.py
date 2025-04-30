from sqlalchemy import Column, func, Integer, Date, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker

Base = declarative_base()

class Connect:
    @staticmethod
    def con():
        engine = create_engine("postgresql://postgres:1234@localhost:5432/sofia")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        return Session()

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    employees = relationship('Employee', back_populates='company')

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    s_pas = Column(Integer, nullable=False)
    n_pas = Column(Integer, nullable=False)
    adres = Column(String, nullable=False)
    data = Column(String, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    company = relationship('Company', back_populates='employees')