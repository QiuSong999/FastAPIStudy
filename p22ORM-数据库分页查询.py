'''分页查询:用户指定想要的页码，每页显示多少条数据'''
"""
分页查询：
    select(模型类).offset(起始索引).limit(每页数量)
            #起始索引和每页数量由用户输入指定
            offset:跳过的记录数（起始索引）
            limit:返回的记录数（每页的数量）
            offset值=(当前页码-1)*每页的数量
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
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, comment="创建时间")
    update_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, onupdate=func.now(), comment="修改时间")


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

##############################################################################
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
@app.get("/book/get_book_list")
async def get_book_list(
    page: int = 1,                #要哪一页的数据（用户输入）
    page_size: int = 3,           #每页显示多少条数据(（用户输入）)
    db: AsyncSession = Depends(get_database)
):
    # （页码 - 1） * 每页数量
    skip = (page - 1) * page_size       #起始索引

    # offset 跳过的记录数（起始索引数）  ； limit 每页的记录数（每页显示的数量）
    stmt = select(Book).offset(skip).limit(page_size)       #接收用户输入的第几页以及每页显示的数据条数
    result = await db.execute(stmt)
    books = result.scalars().all()
    return books

if __name__ == '__main__':
    uvicorn.run(app='p22ORM-数据库分页查询:app', host='127.0.0.1', port=8000, reload=True)


"""
ORM查询总结：
    核心思路：
    ★select() → db.execute() → 从ORM对象获取数据 → 响应结果
        select可以更复杂的查询：条件查询where 、聚合查询func 、分页查询
    ★db.get(模型类,主键值)        #根据主键值查询
    
从ORM对象获取数据的方式：
    获取所有数据
        scalars().all()
    获取单条数据
        scalars().first()            #提取第一条数据
        scalars_one_or_none()       #提取一条数据或null（没有满足的就null）
        scalar()                    #提取标量值，即一个数（配合聚合函数使用）  
"""
