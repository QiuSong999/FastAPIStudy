from fastapi import FastAPI
import uvicorn      #代码运行需要的包

#创建FastAPI实例
app = FastAPI()


@app.get("/")
async def root():        #由async修饰的函数为异步函数      #根路径
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == '__main__':
    uvicorn.run(app='main:app',host='127.0.0.1',port=8000,reload=True)

#代码运行后，在浏览器中输入http://127.0.0.1:8000/，会输出{"message":"Hello World"}
#在浏览器中输入http://127.0.0.1:8000/hello/邱嵩，会输出{"message":"Hello 邱嵩"}

"""
1、为什么创建虚拟环境？
    隔离项目的运行环境，避免依赖冲突，保持全局环境的干净和确定
    
2、运行FastAPI的方式：
    方式1：
        点run按钮
    方式2：
        在终端输入的格式： 
        uvicorn 文件名:实例名 --reload  
            #文件名，不需要加后缀。如本文件启动是  uvicorn main:app --reload 
            #实例名由自己定期的，通常为app
            #uvicorn是FastAPI高性能的服务器，用来运行FastAPI项目
            #--reload 表示修改了代码会自动重启服务器
            
3、打开交互式文档：http://127.0.0.1:8000在后面添加/docs,即  http://127.0.0.1:8000/docs     
"""
