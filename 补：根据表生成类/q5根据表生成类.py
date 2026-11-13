'''据表生成类'''
"""
    sqlacodegen一个实用工具，能根据现有数据库表结构（或SQL语句）自动生成模型类，
省去手动编写模型类的麻烦，尤其适合已有数据库的项目迁移
    它支持多种数据库（MySQL、SQLite、PostgreSQL等），生成的模型内包含表名、字段、类型、主键、外键、索引等完整信息
"""
"""
因为我们要根据表生成模型类，所以我们需要提前创建一个PY文件出来，用于放自动生成的代码
"""

import subprocess
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session


# 创建数据库引擎
db_host = "localhost"
db_port = 3306
db_name = "fastapi_first"
db_user_name = "root"
db_password = "123456"
url = f"mysql+pymysql://{db_user_name}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"
engine = create_engine(url, echo=True)

# 配置会话工厂
engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# 生成模型类~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def table_2_model(run=False):
  """将数据库表映射为Python类"""
  if not run:
    return
  output_path = "table_2_models.py"

  venv_python = sys.executable # 若PyCharm使用虚拟环境，这里会返回.venv下的python.exe
  print("当前使用的Python路径：", venv_python) # 确认输出是.venv/Scripts/python.exe

  cmd = [venv_python, "-m", "sqlacodegen", url]
  result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")

  # 打印执行结果（定位问题核心）
  print("=== 命令执行结果 ===")
  print(f"返回码（0=成功，非0=失败）：{result.returncode}")
  print(f"标准输出：\n{result.stdout}")
  print(f"错误输出：\n{result.stderr}") # 重点看这里，会显示失败原因

  with open(output_path, "w", encoding="utf-8") as f:
    f.write(result.stdout)


if __name__ == "__main__":
  table_2_model(True)
  #运行即可生成到 table_2_models.py
  # insert_dept_emp()


#在终端输入
# sqlacodegen mysql+pymysql://root:123456@localhost:3306/fastapi_first/补：根据表生成类 > models.py
#也会自动生成类
"""
  方式	                            说明
手动命令	      终端输入sqlacodegen mysql+pymysql://... > table_2_models.py
本节写的代码	  用 Python 脚本调用同样的命令，把输出写到 table_2_models.py
"""
