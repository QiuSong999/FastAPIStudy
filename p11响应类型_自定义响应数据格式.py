''' '''
"""
自定义响应数据格式：
    response_model是路径操作装饰器（如@app.get或@app.post）的关键参数，它通过一个Pydantic模型来严格定义和约束API端点的输出格式
    这一机制在提供自动数据验证和序列化的同时，更是保障数据安全性的第一道防线
    
如何自定义响应数据的格式？
    首先要定义类型,再写接口
"""

#案例：返回自定义响应数据格式
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel      #自定义响应类型导包

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#需求：定义一个新闻接口 → 响应数据格式 id、title、content
#定义类型
class News(BaseModel):
    id:int
    title:str
    content:str

#写接口
@app.get('/news/{id}',response_model=News)      #数据响应类型为自定义的类
async def get_news(id:int):
    return {
        'id':id,
        'title':f'这是第{id}本书',
        'content':'这是一本很有趣的书'   #如果这一行去掉，就会报错
                                     #因为response_model=News要求返回值必须包含News类里面定义的所有字段
    }


if __name__ == '__main__':
    uvicorn.run(app='p11响应类型_自定义响应数据格式:app', host='127.0.0.1', port=8000, reload=True)
#或终端输入uvicorn p11响应类型_自定义响应数据格式:app --reload
#http://127.0.0.1:8000/news/5，可以的到 {"id":5,"title":"这是第5本书","content":"这是一本很有趣的书"}

#如果把接口的一项去掉，比如把 'content':'这是一本很有趣的书' 一行代码去掉，就会报错。因为不和自定义的类型保持一致了



