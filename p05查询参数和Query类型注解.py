''' '''
"""
查询参数：
    声明的参数不是路径参数时，路径操作函数会把该参数自动解释为查询参数
    位置：URL?之后,参数名1=参数值1 如果有多个用&连接
    作用：对资源集合进行过滤、排序、分页等操作
    方法：get
    
给查询参数作进一步限定，用Query函数
Query函数里面的参数，和Path函数类似
有：
    ...                         必填
    gt/ge                       大于/大于等于
    lt/le                       小于/小于等于
    description                  描述
    min_length 或 max_length     长度限制      
    ……
"""

from fastapi import FastAPI,Query        #导包
import uvicorn
app = FastAPI()

#访问根目录时的函数，即http://127.0.0.1:8000/访问的函数
@app.get("/")
async def root():                        #由async修饰的函数为异步函数      #根路径
    return {"message": "Hello World"}

#需求： 查询新闻 → 分页，skip:跳过的记录数， limit:返回的记录数
@app.get('/news/news_list1')     #查询参数不需要在路径这里定义参数名
async def get_news_list(skip:int,limit:int=10):
    return {'skep':skip,'limit':limit}

#uvicorn p05查询参数和Query类型注解:app --reload   运行后，
#输入 http://127.0.0.1:8000/news/news_list1?skip=0&limit=10
#可以的到  {"skep":0,"limit":10}

##路径参数允许用Path做额外的限制，同理查询参数，允许用Query作额外的限制
@app.get('/news/news_list2')
async def get_news_list(
        skip:int=Query(0,description='跳过的记录数',lt=100),       #skip:int=Query(...,),
        limit:int=Query(10,description='返回的记录数')):
    return {'skep':skip,'limit':limit}

#终端输入uvicorn p04查询参数和Query类型注解:app --reload 执行后
#http://127.0.0.1:8000/news/news_list2 输出 {"skep":0,"limit":10}，skep参数未上传，用默认值0；limit未上传，用默认值10
#http://127.0.0.1:8000/news/news_list2?skip=3&limit=20 输出 {"skep":3,"limit":20}，参数上传，用上传的参数覆盖默认值

if __name__ == '__main__':
        uvicorn.run(app='p05查询参数和Query类型注解:app',host='127.0.0.1',port=8000,reload=True)

