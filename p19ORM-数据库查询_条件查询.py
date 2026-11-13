'''查询条件'''
"""
数据库条件查询
    select (Book).where(条件1,条件2……)      #多个条件要同时满足
    
条件：
    比较判断：== > < >= <=等
    模糊条件：like()
    与非判断：& l ~
    包含判断：in_()
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
#在路径，地址栏里面就可以筛选
# 需求：路径参数 书籍id（
@app.get("/book/get_book/{book_id}")    #用户在发请求的时候，传进来一个路径参数（主键id）
async def get_book_list(book_id: int, db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.id == book_id))   #模型类的某个属性值和具体的值作判断
    #条件查询select (Book).where(条件1,条件2……) 与查询核心语句结合 await db.execute(select(模型类))
    book = result.scalar_one_or_none()      #满足条件的提取，不满足的提示Null
    return book
#地址栏中输入http://127.0.0.1:8000/book/get_book/2，即可得到查询结果
# {"bookname":"三国","price":180.0,"create_time":"1987-08-18T09:07:28","author":"罗贯中","id":2,"publisher":"光明","update_time":"2026-06-18T09:07:29"}


#其实也可以用其他列名来判断）
# 需求：条件 价格大于等于200（结果返回列表的形式）
@app.get("/book/search_book")
async def get_search_book(db: AsyncSession = Depends(get_database)):
    result = await db.execute(select(Book).where(Book.price >= 200))
    book = result.scalars().all()
        # 可能有多条 → 用.all()转成列表
    return book
#访问http://127.0.0.1:8000/book/search_book，可查到只有一条数据满足价格大于等于200
#[{"bookname":"红楼梦","price":200.0,"create_time":"1986-08-18T09:06:44","author":"曹雪芹","id":1,"publisher":"人教版","update_time":"2026-05-18T09:07:01"}]

if __name__ == '__main__':
    uvicorn.run(app='p19ORM-数据库查询_条件查询:app', host='127.0.0.1', port=8000, reload=True)
