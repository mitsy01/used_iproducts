from typing import Annotated, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.db.products import db_actions 
from app.db.products.models import Product
from app.db.base import get_db
from app.pydantic_models.products import ProductModel, ProductModelResponse


products_route = APIRouter(prefix="/products", tags=["Products"])


@products_route.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductModelResponse)
async def add_prod(product_model: ProductModel, db: Annotated[AsyncSession, Depends(get_db)]):
    return await db_actions.add_prod(product=product_model, db=db)


@products_route.get("/", response_model=list[ProductModelResponse])
async def get_all_prod(db: Annotated[AsyncSession, Depends(get_db)]):
    return await db_actions.get_all_prod(db=db)


@products_route.put("/{products_id}", response_model=ProductModelResponse)
async def update_prod(product_id: str, product_update: ProductModel, db: Annotated[AsyncSession, Depends(get_db)]):
    update_prod = await db_actions.update_prod(product_id=product_id, data=product_update, db=db)
    
    if update_prod is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Товар не знайдено.")
    
    return update_prod


@products_route.delete("/", status_code=status.HTTP_200_OK, response_model=ProductModel)
async def delete_prod(product: ProductModel, db: Annotated[AsyncSession, Depends(get_db)]):
    return await db_actions.delete_prod(name_prod=product.name_prod, price=product.price, db=db)