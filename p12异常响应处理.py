''' '''
"""
异常处理：
    对于客户端引发的错误（4××，如资源未找到、认证失败），应使用fastapi.HTTPException来中断正常处理流程
    并返回标准错误响应.
首先要导包：from fastapi import HTTPException
函数里面定义异常:写判断条件，出现异常 raise HTTPException(参数) 抛出异常
    eg:
        if ~~~~:
            raise HTTPException(参数)
    
"""

from fastapi import FastAPI,HTTPException       #导入异常响应包
import uvicorn

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#需求：按id查询新闻 → id值为1~6，如果不在区间就异常响应
@app.get('/news/{id}')
async def get_news(id:int):
    if id not in range(1, 7):
        raise HTTPException(
            status_code=404,              # HTTP 状态码（必填）
            detail='您查找的信息不存在'      # 错误详情（可选，尽量写上）
        )
        #
    return {'id':id}        # ← 只有没报错时才会执行

"""
raise = 出错了，告诉浏览器"这是错误"（状态码 4xx/5xx）
return = 一切正常，返回数据给浏览器（状态码 200）
所以错误用 raise，正常用 return。
"""
# 终端输入uvicorn p12异常响应处理:app --reload 或
if __name__ == '__main__':
    uvicorn.run(app='p12异常响应处理:app',host='127.0.0.1',port=8000,reload=True)

# http://127.0.0.1:8000/news/5  返回  {"id":5}
# http://127.0.0.1:8000/news/55 返回  {"detail":"您查找的信息不存在"}


