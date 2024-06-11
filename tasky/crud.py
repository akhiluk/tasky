from sqlalchemy.orm import Session
from tasky import models, schemas, utils

def create_user(db: Session, user: schemas.UserCreate):
    user.password = utils.hash(user.password)
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, username: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    return user

# =============================================================================================
# =============================================================================================

def get_task_lists(db: Session, user: models.User, skip: int = 0, limit: int = 10) -> list:
    db_task_lists = db.query(models.TaskList).filter(models.TaskList.user_id == user.id).offset(skip).limit(limit).all()
    return db_task_lists

def get_task_list(db: Session, task_list_id: int, user: models.User):
    db_task_list = db.query(models.TaskList).filter(models.TaskList.id == task_list_id, models.TaskList.user_id == user.id).first()
    return db_task_list

def create_task_list(db: Session, task_list: schemas.TaskListCreate, user: models.User):
    db_task_list = models.TaskList(user_id = user.id, **task_list.model_dump())
    db.add(db_task_list)
    db.commit()
    db.refresh(db_task_list)
    return db_task_list

def update_task_list(db: Session, task_list: schemas.TaskListUpdate, user: models.User):
    db_task_list = db.query(models.TaskList).filter(models.TaskList.id == task_list.id, models.TaskList.user_id == user.id)
    if db_task_list is not None:
        db_task_list.update({"name": task_list.name})
        db.commit()
    return db_task_list.first()

def delete_task_list(db: Session, task_list_id: int):
    db_task_list = db.query(models.TaskList).filter(models.TaskList.id == task_list_id)
    db_task_list.delete(synchronize_session = False)
    db.commit()
    
# =============================================================================================
# =============================================================================================

def get_tasks(db: Session, user: models.User, task_list: int = 0, skip: int = 0, limit: int = 10, show_completed: bool = False) -> list:
    if show_completed:
        if task_list > 0:
            db_tasks = db.query(models.Task).filter(models.Task.user_id == user.id, models.Task.list_id == task_list).offset(skip).limit(limit).all()
        else:
            db_tasks = db.query(models.Task).filter(models.Task.user_id == user.id).offset(skip).limit(limit).all()
    else:
        if task_list > 0:
            db_tasks = db.query(models.Task).filter(models.Task.user_id == user.id, models.Task.list_id == task_list, models.Task.is_completed == False).offset(skip).limit(limit).all()
        else:
            db_tasks = db.query(models.Task).filter(models.Task.user_id == user.id, models.Task.is_completed == False).offset(skip).limit(limit).all()
    
    return db_tasks

def get_task(db: Session, task_id: int, user: models.User):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.user_id == user.id).first()
    return db_task

def create_task(db: Session, task: schemas.TaskCreate, user: models.User):
    db_task_list = get_task_list(db, task.list_id, user)
    if db_task_list is not None:
        db_task = models.Task(user_id = user.id, **task.model_dump())
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task
    else:
        return None

def update_task(db: Session, task: schemas.TaskUpdate, user: models.User):
    db_task_list = get_task_list(db, task.list_id, user)
    if db_task_list is not None:
        task_update_query = db.query(models.Task).filter(models.Task.id == task.id, models.Task.user_id == user.id)
        task_update_query.update(task.model_dump())
        db.commit()
        return task_update_query.first()
    else:
        return None
    
def delete_task(db: Session, id: int):
    db_task = db.query(models.Task).filter(models.Task.id == id)
    db_task.delete(synchronize_session = False)
    db.commit()