from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

import crud, models, schemas, auth
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, username=user.username, password=user.password)

from datetime import timedelta
from fastapi import Response

@app.post("/token")
def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=15)  # Example value
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.UserOut)
def read_users_me(current_user: schemas.UserOut = Depends(auth.get_current_user)):
    return current_user

@app.post("/logs/", response_model=schemas.ActivityLogSchema)
def create_activity_log_for_user(
    request: Request,
    action: str,
    current_user: schemas.UserOut = Depends(auth.get_current_user),
    db: Session = Depends(get_db),
):
    ip_address = request.client.host
    return crud.add_activity_log(db=db, user_id=current_user.id, action=action, ip_address=ip_address)

@app.get("/logs/{user_id}", response_model=List[schemas.ActivityLogSchema])
def read_logs_by_user(user_id: int, db: Session = Depends(get_db)):
    logs = crud.get_logs_by_user(db, user_id=user_id)
    return logs

@app.get("/dashboard/", response_model=List[schemas.ActivityLogSchema])
def read_dashboard(db: Session = Depends(get_db), current_user: schemas.UserOut = Depends(auth.get_current_user)):
    if current_user.role != "manager":
        raise HTTPException(status_code=403, detail="Not authorized")
    logs = crud.get_all_logs(db)
    return logs

@app.post("/shopify_accounts/", response_model=schemas.ShopifyAccountOut)
def create_shopify_account(
    account: schemas.ShopifyAccountCreate, db: Session = Depends(get_db)
):
    return crud.create_shopify_account(db=db, name=account.name)

@app.post("/users/link_shopify_account/", response_model=schemas.UserWithShopifyAccounts)
def link_user_to_shopify_account(
    link: schemas.UserShopifyLinkCreate, db: Session = Depends(get_db)
):
    crud.assign_user_to_shopify_account(
        db=db,
        user_id=link.user_id,
        shopify_account_id=link.shopify_account_id,
        access_level=link.access_level,
    )
    user = crud.get_user_by_username(db, username="some_username")  # Replace with actual username
    return user

@app.get("/shopify/orders")
def get_shopify_orders(request: Request, current_user: schemas.UserOut = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    # Simulate a call to the Shopify API
    orders = [{"id": 1, "total_price": 100}, {"id": 2, "total_price": 200}]

    # Log the action
    ip_address = request.client.host
    crud.add_activity_log(db=db, user_id=current_user.id, action="Fetched Shopify orders", ip_address=ip_address)

    return orders
