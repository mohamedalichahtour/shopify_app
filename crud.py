from sqlalchemy.orm import Session
from models import User, ActivityLog
from security import hash_password  # Import direct ici, plus d'import cyclique
import models

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, username: str, password: str, role: str = "staff"):
    hashed_pw = hash_password(password)
    user = User(username=username, hashed_password=hashed_pw, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def add_activity_log(db: Session, user_id: int, action: str, ip_address: str):
    log = ActivityLog(user_id=user_id, action=action, ip_address=ip_address)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_logs_by_user(db: Session, user_id: int):
    return db.query(ActivityLog).filter(ActivityLog.user_id == user_id).all()

def get_all_logs(db: Session):
    return db.query(ActivityLog).all()


def get_shopify_accounts_by_user(db: Session, user_id: int):
    associations = db.query(models.UserShopifyAccount).filter(models.UserShopifyAccount.user_id == user_id).all()
    results = []
    for assoc in associations:
        account = assoc.shopify_account
        account.access_level = assoc.access_level  # injecte le niveau d'accès dans l'objet pour la réponse
        results.append(account)
    return results

def create_shopify_account(db: Session, name: str):
    account = models.ShopifyAccount(name=name)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def assign_user_to_shopify_account(db: Session, user_id: int, shopify_account_id: int, access_level: str = "limited"):
    association = models.UserShopifyAccount(
        user_id=user_id,
        shopify_account_id=shopify_account_id,
        access_level=access_level,
    )
    db.add(association)
    db.commit()
    db.refresh(association)
    return association
