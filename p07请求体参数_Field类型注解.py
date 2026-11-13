''' 请求体Field限制'''
"""
给请求体参数作进一步限定，用Field函数
Field函数里面的参数，和Path函数类似
有：
    ...                         必填
    gt/ge                       大于/大于等于
    lt/le                       小于/小于等于
    description                  描述
    min_length 或 max_length     长度限制      
    ……
"""
from fastapi import FastAPI
from pydantic import BaseModel,Field        #导包

app = FastAPI()

#访问根目录时的函数，即http://127.0.0.1:8000/访问的函数
@app.get("/")
async def root():                        #由async修饰的函数为异步函数      #根路径
    return {"message": "Hello World"}

# 注册：用户名和密码　→ str
# 1.定义类型
class User(BaseModel):      #继承的类是固定的，用之前先导入
    username:str=Field(default='张三',min_length=2,max_length=10,description='用户名长度要求2~10个字')
    password:str=Field(min_length=4,max_length=20,description='密码要求在4-20个字之间')

# 2.写路由
@app.post('/register')
async def register(user:User):      #此时前一步定义的类User就是一个类型
    return user

#post请求不能通过http://127.0.0.1:8000/register访问，因为浏览器地址栏访问是 GET 请求
#只能通过http://127.0.0.1:8000/docs

"""
终端输入uvicorn p06请求体参数_Field类型注解:app --reload 执行后
1、浏览器访问：http://127.0.0.1:8000/docs
2、找到 POST /register 接口，点击 Try it out
3、在 Request body 里修改：
    {
      "username": "邱嵩",
      "password": "123456"
    }
4、点击 Execute，就能看到返回结果
{
  "username": "邱嵩",
  "password": "123456"
}
"""
"""
请求体参数不在URL里面，出现在消息体里面
1、请求体参数的作用？
    创建、更新资源
2、如何定义、使用请求体参数？
    首先定义类型
    再类型注解
3、请求体参数如何加类型注解？
    Python原生注解和Field函数注解
"""