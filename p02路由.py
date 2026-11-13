''' 路由介绍'''
#请求路径就叫路由
"""
路由：
    就是URL地址和处理函数之间的映射关系，它决定了当用户访问某个特定网址时，服务器应执行哪段代码来返回结果
    
FastAPI的路由定义基于Python的装饰器模式，如

@app.get('/')                           #整体是个装饰器写法    #app为FastAPI实例  #.get为请求方法   #('/')为请求路径，/代表根路径
async def root():                       #请求上面的路径('/')时，就执行该函数
    return {'message':'hello word'}     #请求('/')路径时，就返回响应结果，即 {'message':'hello word'}

#.get为请求方法，按需求可以换成其他的
"""


from fastapi import FastAPI
import uvicorn

# 创建FastAPI实例
app = FastAPI()

#访问根目录时的函数
@app.get("/")
async def root():                        #由async修饰的函数为异步函数      #根路径
    return {"message": "Hello World"}

#访问/hello 目录时，执行的函数
@app.get("/hello")
async def get_hello():
    return {"meg": "你好，FastAPI"}

"""
路由分发：将请求路径（路由）拆分放到不同的模块中，当然也可动手输入不同的路径，实现自动分发，有个工具：APIRouter(使用前先导包)
"""
#

if __name__ == '__main__':
    uvicorn.run(app='p02路由:app',host='127.0.0.1',port=8000,reload=True)
#uvicorn p02路由:app --reload 执行后
# 在http://127.0.0.1:8000后面加上“/hello”，即 http://127.0.0.1:8000/hello 即可执行get_hello函数，并返回结果 {"meg": "你好，FastAPI"}