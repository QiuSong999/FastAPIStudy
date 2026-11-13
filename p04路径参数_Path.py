""" """
import uvicorn

"""
上章讲到
@app.get('/book/{id}')          #id为路径参数的名字
async def get_book(id:int):     #int表示限定id的类型      
    return {'id':id,'title':f'这是第{id}本书'}
    
http://127.0.0.1:8000/book/n,就会输出{"id":1,"title":"这是第n本书"}
最后一个n只要是整数就行，现在我只有100本数，所以要限定范围
路径参数只要是整数就可以，现在要进一步限定范围，用path函数

路径参数——类型注解Path
首先要导入FastAPI函数
@app.get('/book/{id}')                  #id为路径参数的名字
async def get_book(id:int=Path(……)):       #int表示限定id的类型 ，Path=()进一步限定     
    return {'id':id,'title':f'这是第{id}本书'}
    
像Path,Query,Field都是类型限制参数，用来限制传入参数的类型
path()的参数如下
    ...                         必填
    gt/ge                       大于/大于等于
    lt/le                       小于/小于等于
    description                  描述
    min_length 或 max_length     长度限制      
……
"""

from fastapi import FastAPI,Path        #导包
app = FastAPI()

#访问根目录时的函数，即http://127.0.0.1:8000/访问的函数
@app.get("/")
async def root():                        #由async修饰的函数为异步函数      #根路径
    return {"message": "Hello World"}

@app.get('/book/{id}')      #id为路径参数的名字
async def get_book(id:int=Path(...,gt=0,lt=101,description='书籍id的取值范围为[1,99]')):
    #限制整数型的基础之上，（gt=0,lt=101）限制数值在1~100之间, description=添加描述信息
    return {'id':id,'title':f'这是第{id}本书'}

#uvicorn p04路径参数_Path:app --reload 执行后
#http://127.0.0.1:8000/99，即可得到  {"id":99,"title":"这是第99本书"}，如果最后输入的不在1~99会报错

#需求：查找书籍的作者，路径参数name,长度范围2-10
@app.get('/author/{name}')
async def get_name(name:str=Path(...,min_length=2,max_length=10)):
    return {'msg':f'这是“{name}”的信息'}
##http://127.0.0.1:8000/author/邱嵩  即可得到  {"msg":"这是“邱嵩”的信息"}
#或http://127.0.0.1:8000/docs 刷新可填写name,并查看返回值

if __name__ == '__main__':
        uvicorn.run(app='p04路径参数_Path:app',host='127.0.0.1',port=8000,reload=True)
