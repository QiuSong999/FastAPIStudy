''' '''
import uvicorn

"""
响应类型的设置方式：
    1、装饰器中指定响应类
        场景：固定返回类型（HTML、纯文本等）
        
        @app.get('/html',response_class=HTMLResponse)
        ……
        
    2、返回响应对象
        场景：文件下载，图片，流式响应
        
        ……
        return FileResponse(file_path)
        
"""
#案例：返回HTML内容类型
from fastapi import FastAPI
from fastapi.responses import HTMLResponse      #响应类型导包

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#接口 → 响应HTML代码
@app.get('/html',response_class=HTMLResponse)
async def get_html():
    return '<h1>这是一级标题</h1>'
"""
<h1>这是一级标题</h1>解释如下：
    <h1>:   HTML 的开始标签，表示"一级标题"（Heading 1）
    "这是一级标题":   要显示的文字内容
    </h1>:  HTML 的结束标签，表示标题在这里结束
"""
#控制台输入 uvicorn p09响应类型_HTML:app --reload
#http://127.0.0.1:8000/html，即可得到界面  “这是一级标题” 标题是加大加粗的
#http://127.0.0.1:8000/docs 可以看到相应类型变成 content-type: text/html

if __name__ == '__main__':
        uvicorn.run(app='p09响应类型_HTML:app',host='127.0.0.1',port=8000,reload=True)
