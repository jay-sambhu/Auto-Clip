#!/usr/bin/env python3
"""
清空数据库中的所有项目数据
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.core.database import get_db
from backend.models.project import Project
from backend.models.clip import Clip
from backend.models.collection import Collection
from backend.models.task import Task
from sqlalchemy.orm import Session

def clean_database():
    """Clear all project-related data from the database."""
    print("🧹 Starting database cleanup...")
    
    # 获取数据库会话
    db = next(get_db())
    
    try:
        # 删除所有数据（按依赖关系顺序）
        print("Deleting task data...")
        deleted_tasks = db.query(Task).delete()
        print(f"✅ Deleted {deleted_tasks} tasks")
        
        print("Deleting collection data...")
        deleted_collections = db.query(Collection).delete()
        print(f"✅ Deleted {deleted_collections} collections")
        
        print("Deleting clip data...")
        deleted_clips = db.query(Clip).delete()
        print(f"✅ Deleted {deleted_clips} clips")
        
        print("Deleting project data...")
        deleted_projects = db.query(Project).delete()
        print(f"✅ Deleted {deleted_projects} projects")
        
        # 提交事务
        db.commit()
        
        print("\n🎉 Database cleanup complete!")
        print("The database is now clean with no project data.")
        
    except Exception as e:
        print(f"❌ Error during database cleanup: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()

if __name__ == "__main__":
    clean_database()
