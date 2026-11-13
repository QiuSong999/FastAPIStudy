"""
生成基类
"""
from sqlalchemy.ext.declarative import declarative_base     #导包

# 生成基类,所有模型需继承该类
Base = declarative_base()
