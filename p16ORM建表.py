''' '''
"""
ORM —— 建表流程：（建1个表）
    1、创建数据库引擎：create_async_engine（创建异步引擎）
    2、定义模型类：
        ☆定义1个基类（继承DeclarativeBase）：基类里面一般放公用的属性、函数
        ☆定义1个模型类（继承基类）：创建表所对应的模型类
    3、FastAPI启动时建表：run_sync(基类名.metadata.create_all)建表
    
ORM创建数据库引擎
    首先导包from sqlalchemy.ext.asyncio import create_async_engine
    使用create_async_engine创建异步引擎
"""
from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import DateTime, func, String, Float, select,Integer
    #DeclarativeBase 是 SQLAlchemy 2.0 中用来定义数据模型（表结构）的基类。
    #Mapped 是类型提示，告诉 Python 这个字段的类型，后面定义表中列名的时候用
    #mapped_column 是 字段定义，替代旧的 Column，功能更强

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, DateTime

app = FastAPI()

## 1.创建异步引擎

# Mysql连接格式：'mysql+aiomysql或pymysql://root:123456@localhost:3306/FastAPI_first?charset=utf8'
#root为用户名，123456为密码，localhost为地址，，3306为数据库端口号，day01为数据库的名字
ASYNC_DATABASE_URL = 'mysql+aiomysql://root:123456@localhost:3306/FastAPI_first?charset=utf8'  #URL数据库的地址/连接

#创建引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,     #数据库的连接，前一行代码获取
    echo = True,            #可选，输出SQL日志
    pool_size = 10,         #设置连接池中保持的持久连接数
    max_overflow = 20       #设置连接池允许创建的额外连接数
)

## 2.定义两个模型类（基类 + 对应的模型类）
#基类：继承DeclarativeBase（包含通用属性和字段的映射）
#基类：创建时间、更新时间； 书籍表：id、书名、作者、价格、出版社

#基类：创建一个基类，所有数据库表模型都继承它。
class Base(DeclarativeBase):            ##如果列名没有“创建时间”和“修改时间”，就不用定义这个Base类
    __abstract__ = True     #这句作用是告诉 SQLAlchemy："这个类只是一个'模板'，不要为它创建数据库表
    create_time:Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,comment='创建时间')
    update_time:Mapped[datetime] = mapped_column(DateTime,insert_default=func.now(),default=func.now,onupdate=func.now,comment='修改时间')
    # create_time和update_time —— 通用字段。  作用：给所有表自动添加 "创建时间" 和 "修改时间" 两个字段。
    #default=func.now()	插入数据时，自动填当前时间；onupdate=func.now	更新数据时，自动更新为当前时间
    # 这两个字段几乎在所有的业务表中都需要，写在基类里可以避免重复定义，提高代码复用性

#这两个类中的Mappend,如 create_time:Mapped[datetime] ，目的是：告诉 Python/IDE：create_time 是 datetime 数据类型
# mapped_column，目的是：告诉 SQLAlchemy：这是数据库的一个字段

#定义数据表对应的模型类
class Book(Base):   #继承上面的基类     ，如果没有定义上面的基类，就  class Book(DeclarativeBase):  继承 DeclarativeBase即可
    __tablename__ = 'book'      #数据表名，有表名才会建表
    ##定义表中的列名以及数据类型和约束
    id:Mapped[int] = mapped_column(primary_key=True,autoincrement=True,comment='书籍的id')         #数据表的每一列
    bookname:Mapped[str] = mapped_column(String(255),comment='书名')           #数据表的每一列
    author:Mapped[str] = mapped_column(String(50),comment='作者')              #数据表的每一列
    price:Mapped[float] = mapped_column(Float,comment='价格')                  #数据表的每一列
    publisher:Mapped[str] = mapped_column(String(50),comment='出版社')         #数据表的每一列
#其中create_time和update_time列会自动继承过来


##3.建表：定义函数建表 → fastAPI 启动的时候，调用建表的函数
async def create_tables():      #建表函数
    #获取数据库的异步引擎，创建事务，建表
    async with async_engine.begin() as conn:        # 获取数据库连接，as表示重命名
        await conn.run_sync(Base.metadata.create_all)       #执行建表，

@app.on_event('startup')        #FastAPI 的装饰器，注册一个"启动时执行"的事件
async def startup_event():      #被装饰的异步函数
    await create_tables()       #调用建表函数


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run(app='p16ORM建表:app', host='127.0.0.1', port=8000, reload=True)