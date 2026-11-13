'''路径参数 '''
"""
之前我们向服务器发请求，比如向根路径发起请求，无论发起多少次，返回结果都是{"message": "Hello World"}
现要实现：同一个接口逻辑，根据参数不同返回不同的数据

参数就是客户端发送请求时，附带的额外信息和指令
参数的作用是让同一个接口能根据不同的输入，返回不同的输出，实现动态交互

参数分类：
    路径参数：
    查询参数：
    请求体：
"""
"""
路径参数：
    位置：URL路径的一部分，如 /book/{id}   id就是路径参数，需要在路径上定义
    作用：指向唯一的、特定的资源
    方法：get
    
@app.get('/book/{id}')          #路径里面有请求参数id                 #id就是路径参数
async def get_book(id:int):     #方法中的参数也必须是id                #int约定参数的类型
    return {'id':id,'title':f'这是第{id}本书'}
※ 如果@app.get有请求参数了，那么方法的参数名要和这个请求参数名字一样，这样浏览器上的请求参数才能给该方法的参数附上值
"""

from fastapi import FastAPI
import uvicorn
app = FastAPI()

#访问根目录时的函数
@app.get("/")
async def root():                        #由async修饰的函数为异步函数      #根路径
    return {"message": "Hello World"}

@app.get('/book/{id}')      #id为路径参数的名字
async def get_book(id:int):       #括号里面定义一个跟路径参数同名的形参
    return {'id':id,'title':f'这是第{id}本书'}

#uvicorn p03参数简介和路径参数:app --reload 执行后
#http://127.0.0.1:8000/book/1 可返回结果  {"id":1,"title":"这是第1本书"}

#路径参数也可上传多个参数
@app.get("/items/{category}/{item_id}")
async def get_item(category: str, item_id: int):
    return {"category": category, "item_id": item_id}
#http://127.0.0.1:8000/items/book/123 可返回结果  {"category":"book","item_id":123}

if __name__ == '__main__':
        uvicorn.run(app='p03参数简介和路径参数:app',host='127.0.0.1',port=8000,reload=True)