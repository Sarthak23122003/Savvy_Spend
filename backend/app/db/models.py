from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    # user_id = Column(Integer, ForeignKey('users.id'))  # Uncomment if user model is added

    def __repr__(self):
        return f"<Expense(id={self.id}, description='{self.description}', amount={self.amount}, date={self.date})>"