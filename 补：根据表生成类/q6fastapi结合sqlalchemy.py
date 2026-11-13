"""
FastAPI和SQLAlchemy结合
"""

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from table_2_models import Departments, Employees
from database_API和SQL结合时用 import SessionLocal, engine

app = FastAPI()

# 依赖项：获取数据库会话
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get('/')
def root():
  return {'欢迎':'来到系统'}

# 部门相关接口
@app.post("/departments/")    #POST不能用地址栏直接访问，需要访问http://127.0.0.1:8000/docs
def create_department(name: str, location: str, db: Session = Depends(get_db)):
  db_department = Departments(name=name, location=location)
  db.add(db_department)
  db.commit()
  db.refresh(db_department)
  return db_department

@app.get("/departments/")
def read_departments(db: Session = Depends(get_db)):
  return db.query(Departments).all()

@app.get("/departments/{department_id}")
def read_department(department_id: int, db: Session = Depends(get_db)):
  department = db.query(Departments).filter(Departments.id == department_id).first()
  if not department:
    raise HTTPException(status_code=404, detail="Department not found")
  return department

if __name__ == "__main__":
  # 直接在代码中启动uvicorn服务器
  uvicorn.run(app="q6fastapi结合sqlalchemy:app",host='127.0.0.1', port=8000, reload=True)

  #访问http://127.0.0.1:8000/departments/，即可得到:
  # [{"name":"研发部","location":"北京总部","id":1},{"name":"市场部","location":"上海公司","id":2},{"name":"费控部","location":"合肥公司","id":3}]

  #访问http://127.0.0.1:8000/departments/2，即可得到{"name":"市场部","location":"上海公司","id":2


