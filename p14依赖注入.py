''' 依赖注入'''
#中间件、依赖注入都可以减少代码重复，但是：中间件是控制所有请求，每个请求都会自动执行中间件的所有代码
#依赖注入是我们自己做主，哪些请求需要这些通用的代码，我们就把他注入，注入的接口会执行通用的代码，不注入的不执行
"""
使用依赖注入系统来共享通用逻辑，减少代码重复。
    依赖项：重用的组件（函数/类）负责提供某种功能或数据
    注入：FastAPI自动帮你调用依赖项，并将结果“注入”到路径操作函数中
优点：
    代码复用：一次编写，多次使用
    解耦：业务逻辑和基础设置代码分离
    易于测试：轻松地用模拟依赖替换真实依赖进行测试
    
依赖注入系统使用步骤：
    1、创建依赖项:       创建个函数，把通用的函数给封装起来
    2、导入Depends：    from fastapi from Depends
    3、声明依赖项：      在路由处理函数参数位置，加上依赖项的名字（就是通用函数的函数名）commons = Depends(common_paramenters)

    中间件是控制所有请求，每个请求都会自动执行中间件里面通用的代码
    依赖注入是由我们指定哪些请求，注入的接口才会执行通用的代码

三种减少重复代码的方式：
方式	        适用范围	                    示例
中间件	    全局（所有接口）	    日志、认证、限流、CORS
依赖项     (Depends)	指定接口	    数据库连接、权限验证
装饰器	    指定函数	                 缓存、计时
"""
from fastapi import FastAPI,Query,Depends      #导入Depends
import uvicorn
app = FastAPI()

#设置根目录访问内容
@app.get("/")
async def root():
    return {"message": "Hello World"}

#分页参数逻辑公用：即新闻列表和用户列表公用（非所有列表公用）
##1、创建依赖项
async def common_paramenters(
        skip:int=Query(0,ge=0),     #跳过几条数据
        limit:int=Query(10,le=60)   #每页做多要多少数据
):
    return {'skip':skip,'limit':limit}

#导入Depends，from fastapi import Depends（前面已做）

#2、注入依赖项（声明依赖项）
@app.get('/news/news_list')
async def get_news_list(commons = Depends(common_paramenters)):     #Depends()，括号里面写上依赖项名字common_paramenters
    return commons

@app.get('/user/user_list')
async def get_user_list(commons = Depends(common_paramenters)):      #user_list依赖注入公用的代码
    return commons

@app.get('/csv/csv_list')
async def get_csv_list():       #未依赖注入公用的代码，则不会执行公共代码
    return {'message':'hello'}

if __name__ == '__main__':
    uvicorn.run(app='p14依赖注入:app',host='127.0.0.1',port=8000,reload=True)