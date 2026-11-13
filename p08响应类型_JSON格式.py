''' '''
"""
响应类型：
    默认情况下，FastAPI会将路径操作函数返回的Python对象（字典、列表、Pydantic模型等），经jsonable_encoder转换未
    JSON兼容格式，并包装未JSONResponse返回。如果需要返回非JSON数据，FastAPI也提供了丰富的响应类型来返回不同的数据
    
具体如下：
    响应类型                    用途                          示例
 ★ JSONResponse        默认响应，返回JSON数据       return {"key": "value"}
 ★ HTMLResponse            返回HTML内容        return HTMLResponse(html_content)
    PlainTextResponse       返回纯文本           return PlainTextResponse("text")
 ★ FileResponse            返回文件下载          return FileResponse(path)
    StreamingResponse       流式响应                生成器函数返回数据 
    RedirectResponse        重定向                 return RedirectResponse(url)
    
在http://127.0.0.1:8000/docs中的content-type可以查看类型,默认是application/json










"""