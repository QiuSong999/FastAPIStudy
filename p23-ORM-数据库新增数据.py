'''新增数据'''
#ORM对象 = 数据库里的一行数据，在 Python 里变成了一个对象
"""
数据库操作——新增流程：
    定义ORM对象 → 添加对象到事务：add(对象) → commit提交到数据库
"""

from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy import DateTime, func, String, Float, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from pydantic import BaseModel


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
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now,
                                                  comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now,
                                                  onupdate=func.now(), comment="修改时间")


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

##########################################################################
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

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# 需求：用户输入图书信息（id、书名、作者、价格、出版社） → 新增
# 用户输入 → 参数 → 请求体参数（用户输入的参数定义为请求体参数）
class BookBase(BaseModel):
    id: int
    bookname: str
    author: str
    price: float
    publisher: str
    #其中 “创建时间” 和 “修改时间”不用用户手动输入，会自动插入系统时间


@app.post("/book/add_book")     #post，只能http://127.0.0.1:8000/docs新增
async def add_book(book: BookBase, db: AsyncSession = Depends(get_database)):   #book代表用户输入的信息，先将其转为ORM对象
    # 增加数据思路：ORM对象 → add → commit
    book_obj = Book(**book.__dict__)    #先book转化成字典，然后展开字典，就拿到了所有的键值对.再用模型Book转化一下成ORM对象
# **direct 是字典解包（Dict Unpacking）操作符，作用是把字典拆成 key=value 形式的关键字参数
#将 {"name": "张三", "age": 18}  →  变成  name="张三", age=18
    db.add(book_obj)
    await db.commit()
    return book

# http://127.0.0.1:8000/docs，在里面新增

if __name__ == '__main__':
    uvicorn.run(app='p23-ORM-数据库新增数据:app', host='127.0.0.1', port=8000, reload=True)
