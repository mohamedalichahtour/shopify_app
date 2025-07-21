from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="staff")
    logs = relationship("ActivityLog", back_populates="user")
    shopify_accounts = relationship("UserShopifyAccount", back_populates="user")

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    action = Column(String)
    ip_address = Column(String)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="logs")

class ShopifyAccount(Base):
    __tablename__ = "shopify_accounts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    users = relationship("UserShopifyAccount", back_populates="shopify_account")

class UserShopifyAccount(Base):
    __tablename__ = "user_shopify_accounts"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    shopify_account_id = Column(Integer, ForeignKey("shopify_accounts.id"), primary_key=True)
    access_level = Column(String, default="limited")
    user = relationship("User", back_populates="shopify_accounts")
    shopify_account = relationship("ShopifyAccount", back_populates="users")
