from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base



class Product(Base):
    __tablename__ = "products"
    
    id: Mapped[str] = mapped_column(String(100), primary_key=True) 
    name_prod: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(String(150))
    price: Mapped[float] = mapped_column()
    count: Mapped[str] = mapped_column(String(100))
    
    

