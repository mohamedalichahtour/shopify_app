from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# -------- Utilisateur --------
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: Optional[str]

    class Config:
        from_attributes = True

# -------- Logs d'activité --------
class ActivityLogSchema(BaseModel):
    id: int
    user_id: int
    action: str
    ip_address: str
    timestamp: datetime

    class Config:
        from_attributes = True

# -------- Compte Shopify --------
class ShopifyAccountCreate(BaseModel):
    name: str  # Nom ou identifiant de la boutique

class ShopifyAccountOut(BaseModel):
    id: int
    name: str
    access_level: Optional[str] = None  # Ajouté dynamiquement si besoin

    class Config:
        from_attributes = True

# -------- Liaison User <-> ShopifyAccount --------
class UserShopifyLinkCreate(BaseModel):
    user_id: int
    shopify_account_id: int
    access_level: Optional[str] = "limited"

class UserWithShopifyAccounts(BaseModel):
    id: int
    username: str
    role: Optional[str]
    shopify_accounts: List[ShopifyAccountOut]

    class Config:
        from_attributes = True
