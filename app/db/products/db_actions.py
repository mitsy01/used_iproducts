from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.products.models import Product
from app.pydantic_models.products import ProductModel, ProductModelResponse
from app.db.base import get_db
from app.config import settings


async def get_all_prod(db: AsyncSession):
    query = await db.execute(select(Product))
    return query.scalars().all()


async def add_prod(product: ProductModel, db: AsyncSession):
    product = Product(**product.model_dump())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def delete_prod(name_prod: str, price: float, db: AsyncSession):
    query = await db.execute(select(Product).filter_by(name_prod=name_prod, price=price))
    product = query.scalars().first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Такого товару не знайдено.")
    
    await db.delete(product)
    await db.commit()
    return product


async def update_prod(product_id: str, update_data: ProductModelResponse, db: AsyncSession):
    query = await db.execute(select(Product).where(Product.id==product_id))
    product = query.scalar_one_or_none()
    
    if product is None:
        return None
    
    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)
        
    await db.commit()
    await db.refresh(product)
    return product
    
    