from fastapi import FastAPI

from DesafioInfog2.routers import auth, clients, products

app = FastAPI()

app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(products.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}

