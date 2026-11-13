from fastapi import FastAPI
import uvicorn

# 创建FastAPI实例
app = FastAPI()


@app.get("/")
async def root():  # 由async修饰的函数为异步函数      #根路径
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app='p01FastAPI介绍:app',host='127.0.0.1',port=8000,reload=True)


"""
1、为什么创建虚拟环境？
    隔离项目的运行环境，避免依赖冲突，保持全局环境的干净和确定

2、FastAPI程序启动服务器的方式：
    方式1： python代码输入 
    if __name__ == '__main__':
        uvicorn.run(app='文件名:app',host='127.0.0.1',port=8000,reload=True)
        #参数同下
    方式2： 在终端输入的格式： 
        uvicorn 文件名:实例名 --reload  
            #文件名，不需要加后缀。如本文件启动是  uvicorn p01FastAPI介绍:app --reload 
            #实例名由自己定期的，通常为app
            #uvicorn是FastAPI高性能的服务器，用来运行FastAPI项目
            #--reload 表示修改了代码会自动重启服务器
            
http://127.0.0.1:8000 或者 localhost:8000  打开的是根目录

※ 程序启动之后，FastAPI底层会创建一个字典，字典的键就是“请求路径” ，键所对应的值为“对应的方法名”
※ 我们在浏览器上访问填写路径时，Fast API会获取路径，将其当做“键”去找对应的“值”，这个值就是方法名，然后调用该方法
※ 如果定义方法的时候前面没有加async, fast API在处理请求的时候就按照同步请求处理，加了async， fast API就按照异步请求处理
※ 想给客户端响应什么内容，就可以用return返回什么内容


3、打开交互式文档：http://127.0.0.1:8000在后面添加/docs,即  http://127.0.0.1:8000/docs     

## FastAPI 让你的 Python 函数变成了"网址"，浏览器访问这个网址，就能执行函数并看到返回结果。
## FastAPI 帮你搭建了一个 Web 服务器，让你写的 Python 代码可以通过 HTTP 协议被浏览器访问
"""