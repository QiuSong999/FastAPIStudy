from typing import List, Optional

from sqlalchemy import Date, DateTime, Float, ForeignKeyConstraint, Index, String
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime

class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = 'book'

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True, comment='书籍的id')
    bookname: Mapped[str] = mapped_column(String(255, 'utf8_unicode_ci'), comment='书名')
    author: Mapped[str] = mapped_column(String(50, 'utf8_unicode_ci'), comment='作者')
    price: Mapped[float] = mapped_column(Float, comment='价格')
    publisher: Mapped[str] = mapped_column(String(50, 'utf8_unicode_ci'), comment='出版社')
    create_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='创建时间')
    update_time: Mapped[datetime.datetime] = mapped_column(DateTime, comment='修改时间')


class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = (
        Index('name', 'name', unique=True),
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(String(50, 'utf8_unicode_ci'))
    location: Mapped[Optional[str]] = mapped_column(String(100, 'utf8_unicode_ci'))

    employees: Mapped[List['Employees']] = relationship('Employees', back_populates='department')


class Employees(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        ForeignKeyConstraint(['department_id'], ['departments.id'], name='employees_ibfk_1'),
        Index('department_id', 'department_id')
    )

    id: Mapped[int] = mapped_column(INTEGER(11), primary_key=True)
    name: Mapped[str] = mapped_column(String(50, 'utf8_unicode_ci'))
    department_id: Mapped[int] = mapped_column(INTEGER(11))
    age: Mapped[Optional[int]] = mapped_column(INTEGER(11))
    hire_date: Mapped[Optional[datetime.date]] = mapped_column(Date)

    department: Mapped['Departments'] = relationship('Departments', back_populates='employees')
