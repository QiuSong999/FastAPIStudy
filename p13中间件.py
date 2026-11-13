''' '''
#如果我们定义了多个接口，而每个接口都要验证用户身份，就用到中间件
"""
中间件：
    中间价是一个在每次请求进入FastAPI应用时，都会被执行的函数。
    它在请求到达实际的路径操作（路由处理函数）之前运行，并且在响应返回给客户端之前再运行一次
    中间件 = 全局统一处理器，让你只写一次公共代码，所有接口都能用。（减少代码重复）
    
    中间件能减少代码重复吗？    能！把公共逻辑抽到中间件
    如何实现？	用 @app.middleware("http") 装饰器
    中间件拦截了所有请求，把公共逻辑放在一个地方处理，业务接口只关心自己的事。
    
中间件如何定义？
    中间件是一种函数，函数的顶部使用装饰器@app.middleware('http')装饰，就成了中间件

中间件的作用：
    给每个请求添加统一的处理逻辑（记录日志、身份认证、跨域、设置响应头、性能检测）

中间件的定义：（单个）
    函数顶部使用装饰器@app.middleware('http)，如下
        @app.middleware('http') 
        async def middleware1(request,call_next):  
            print('中间件开始处理--start')
            response = await call_next(request) 
            print('中间件处理完毕--end')
            return response
        
多个中间件的执行顺序：
    执行自下而上 ，响应至上而下 
"""

from fastapi import FastAPI      #导包
import uvicorn
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#定义两个中间件
@app.middleware('http')     #中间件1
async def middleware1(request,call_next):   #两个参数，一个请求request，一个传递请求的all_next
    print('中间件1 start')
    response = await call_next(request)     #传递请求
    print('中间件1 end')
    return response

@app.middleware('http')     #中间件2           #装饰器：声明这是一个 HTTP 中间件
async def middleware2(request,call_next):     #函数签名：参数固定
    print('中间件2 start') #请求前逻辑（请求到达时执行）
    response = await call_next(request)       #调用下一个中间件/路由（必须）
    print('中间件2 end')   #响应后逻辑（响应返回时执行）
    return response                           #返回响应（必须）
'''
请求和响应的顺序如下：
    中间件2 start      #先执行
    中间件1 start      #再执行
      路由函数     ← 最后执行（你的业务代码）
    中间件1 end        #后返回
    中间件2 end        #最后返回
    
请求执行的时候，代码由下往上顺序
响应返回的时候，代码由上往下顺序
'''

if __name__ == '__main__':
    uvicorn.run(app='p13中间件:app',host='127.0.0.1',port=8000,reload=True)
