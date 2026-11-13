''' 查询'''
"""
数据库的增删改查，都是在建表的基础上，新建接口进行操作
数据库会话通过Depends依赖注入的方式注入到路由里面
"""
#-----------------------------------------------------
"""

核心语句：await db.execute(select(模型类))  返回一个ORM对象
    模型类是查询哪个表，这个表对应的模型类的名字天上
    select()是一个ORM语句
    查询的数据就在返回的ORM对象里面
获取数据格式：
    1、获取所有数据：
        scalars().all()     #基于上步骤的ORM对象操作
    2、获取单条数据：
        scalars().first()       #获取第一条数据
        get(模型类,主键值)        #基于db数据库会话，回去主键值对应的数据
"""

from datetime import datetime
import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()


# 1. 创建异步引擎
ASYNC_DATABASE_URL = "mysql+aiomysql://root:123456@localhost:3306/FastAPI_first?charset=utf8"
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  # 可选，输出 SQL 日志
    pool_size=10,  # 设置连接池活跃的连接数
    max_overflow=20  # 允许额外的连接数
)


# 2. 定义模型类： 基类 + 表对应的模型类
# 基类：创建时间、更新时间；书籍表：id、书名、作者、价格、出版社
class Base(DeclarativeBase):
    __abstract__ = True     #这句作用是告诉 SQLAlchemy："这个类只是一个'模板'，不要为它创建数据库表
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, onupdate=func.now, comment="修改时间")


class Book(Base):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(primary_key=True, comment="书籍id")
    bookname: Mapped[str] = mapped_column(String(255), comment="书名")
    author: Mapped[str] = mapped_column(String(255), comment="作者")
    price: Mapped[float] = mapped_column(Float, comment="价格")
    publisher: Mapped[str] = mapped_column(String(255), comment="出版社")


# 3. 建表：定义函数建表 → FastAPI 启动的时候调用建表的函数
async def create_tables():
    # 获取异步引擎，创建事务 - 建表
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # Base 模型类的元数据创建


@app.on_event("startup")
async def startup_event():
    await create_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}

###################################################################################
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,  # 绑定数据库引擎
    class_=AsyncSession,  # 指定会话类
    expire_on_commit=False  # 提交后会话不过期，不会重新查询数据库
)


# 依赖项
async def get_database():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话给路由处理函数
            await session.commit()  # 提交事务
        except Exception:
            await session.rollback()  # 有异常，回滚
            raise
        finally:
            await session.close()  # 关闭会话

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@app.get("/book/books")
async def get_book_list(db: AsyncSession = Depends(get_database)):
    # 参数解释：      db: AsyncSession	        参数名是 db，类型是 AsyncSession（异步数据库会话）
    #               Depends(get_database)	代表这个参数不是手动传的，是 FastAPI 自动注入的

    result = await db.execute(select(Book))     # 查询 → 返回一个 ORM 对象
    # book = result.scalars().all()             # 获取所有
    # book = result.scalars().first()            # 获取第一个
    book = await db.get(Book, 3)         # 获取单条数据 → 根据主键id=3获取
        #只有 1 条（或 0 条） → 用 .first() 或 db.get()
    return book

if __name__ == '__main__':
    uvicorn.run(app='p18ORM-数据库查询:app', host='127.0.0.1', port=8000, reload=True)

