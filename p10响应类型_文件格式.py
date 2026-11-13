''' '''
import uvicorn

"""
响应文件格式：
    FileResponse是FastAPI提供的专门用于高效返回文件内容（eg:图片、PDF、Excel、音视频等）的响应类。
    他能够智能处理文件路径、媒体类型推断、范围请求和缓存头部，是服务静态文件的推荐方式
"""

#案例：返回文件格式类型
from fastapi import FastAPI
from fastapi.responses import FileResponse      #响应类型导包

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#接口：返回一张图片内容
@app.get('/file')
async def get_file():
    path = './files/house.jpg'      #先定义个中间变量，相对路径写法
    return FileResponse(path)

#控制台输入 uvicorn p10响应类型_文件格式:app --reload
#打开http://127.0.0.1:8000/file，即可的到house.jpg图片

if __name__ == '__main__':
        uvicorn.run(app='p10响应类型_文件格式:app',host='127.0.0.1',port=8000,reload=True)