""" 请求体参数"""
"""
在HTTP协议中，一个完整的请求由三部分组成：
    请求行：包含方法、URL、协议版本
    请求头：元数据信息
    请求体：实际要发送的数据内容
    
请求体参数：
    位置：HTTP请求的消息体中
    作用：创建、更新资源携带大量数据，如：JSON
    方法：POST、PUT等
请求体不能在地址栏中传参，地址栏只能接收get方法
    
请求体参数
    １、定义类型
    ２、类型注解
"""

from fastapi import FastAPI       #导包
import uvicorn
from pydantic import BaseModel

app = FastAPI()

#访问根目录时的函数，即http://127.0.0.1:8000/访问的函数
@app.get("/")
async def root():                        #由async修饰的函数为异步函数      #根路径
    return {"message": "Hello World"}

# 注册：用户名和密码　→ str
# 1.定义类型
class User(BaseModel):      #继承的类是固定的
    username:str
    password:str


# 2.写路由
@app.post('/register')
    #post请求不能通过http://127.0.0.1:8000/register访问，因为浏览器地址栏访问是 GET 请求
    #只能通过http://127.0.0.1:8000/docs
async def register(user:User):      #此时前一步定义的类User就是一个类型
    return user
    # 必须有User类里面的 username 和 password 字段，且都是字符串
"""
终端输入uvicorn p05请求体参数:app --reload 执行后
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

if __name__ == '__main__':
        uvicorn.run(app='p06请求体参数:app',host='127.0.0.1',port=8000,reload=True)