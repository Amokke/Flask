from datetime import datetime
from typing import List, Optional
import uvicorn as uvicorn
from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("lastname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(50)),
                         sqlalchemy.Column("passwd", sqlalchemy.String(32)),
                         )

products = sqlalchemy.Table("products", metadata,
                            sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                            sqlalchemy.Column("product_name", sqlalchemy.String(32)),
                            sqlalchemy.Column("description", sqlalchemy.String(128)),
                            sqlalchemy.Column("price", sqlalchemy.Integer),
                            )

orders = sqlalchemy.Table("orders", metadata,
                          sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column("id_user", sqlalchemy.ForeignKey('users.id')),
                          sqlalchemy.Column("id_product", sqlalchemy.ForeignKey('products.id')),
                          sqlalchemy.Column("order_date", sqlalchemy.DateTime),
                          sqlalchemy.Column("status", sqlalchemy.Boolean),
                          )

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


class UserIn(BaseModel):
    name: str = Field(title="Name", max_length=32)
    lastname: str = Field(title="Lastname", max_length=32)
    email: str = Field(title="Email", max_length=50)
    passwd: str = Field(title="Password", max_length=32)


class User(UserIn):
    id: int = Field(title="id")


class ProductIn(BaseModel):
    product_name: str = Field(title="Product_name", max_length=32)
    description: str = Field(title="Description", max_length=128)
    price: int = Field(title="Price")


class Product(ProductIn):
    id: int = Field(title="id")


class OrderIn(BaseModel):
    id_user: int = Field(title="id_user")
    id_product: int = Field(title="id_product")
    order_date: Optional[datetime] = datetime.now()
    status: bool = Field(default=True)


class Order(OrderIn):
    id: int = Field(title="id")


@app.post('/users/', response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(**user.model_dump())
    last_record_id = await database.execute(query)
    return {**user.model_dump(), 'id': last_record_id}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.model_dump())
    await database.execute(query)
    return {**new_user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {f"Пользователь с id {user_id} удален"}


@app.post('/products/', response_model=Product)
async def create_product(product: ProductIn):
    query = products.insert().values(**product.model_dump())
    last_record_id = await database.execute(query)
    return {**product.model_dump(), 'id': last_record_id}


@app.get("/products/", response_model=List[Product])
async def read_products():
    query = products.select()
    return await database.fetch_all(query)


@app.get("/products/{product_id}", response_model=Product)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    return await database.fetch_one(query)


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, new_product: ProductIn):
    query = products.update().where(products.c.id == product_id).values(**new_product.model_dump())
    await database.execute(query)
    return {**new_product.model_dump(), "id": product_id}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    await database.execute(query)
    return {f"Продукт с id {product_id} удален"}


@app.post('/orders/', response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(**order.model_dump())
    last_record_id = await database.execute(query)
    return {**order.model_dump(), 'id': last_record_id}


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.model_dump())
    await database.execute(query)
    return {**new_order.model_dump(), "id": order_id}


@app.delete("/orders/{order_id}")
async def delete_product(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {f"Заказ номер {order_id} удален"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
