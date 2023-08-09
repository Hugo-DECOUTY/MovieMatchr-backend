from fastapi import FastAPI
import asyncio
from moviematchr.utils.socket import socket_manager

from moviematchr.utils.utils import init_bdd
from moviematchr.daemons.desactivation_licences_daemon import desactivation_licences_daemon
from moviematchr.utils.utils import init_env, init_bdd
from moviematchr.routers.account import router as AccountRouter
from moviematchr.routers.tickets import router as TicketsRouter
from moviematchr.routers.orders import router as OrdersRouter
from moviematchr.routers.licences import router as LicencesRouter
from moviematchr.routers.sellers import router as SellersRouter
from moviematchr.routers.transactions import router as TransactionsRouter

init_env()
init_bdd()

tags_metadata = [
    {
        "name": "Account",
    },
    {
        "name": "Tickets",
    },
    {
        "name": "Orders",
    },
    {
        "name": "Licences",
    },
    {
        "name": "Sellers",
    },
    {
        "name": "Transactions",
    },
]

app = FastAPI(title="Admin Platform Back", openapi_tags=tags_metadata)
socket_manager.mount_to("/ws", app)

# Add routes from routes folder
app.include_router(AccountRouter, tags=["Account"])
app.include_router(TicketsRouter, tags=["Tickets"])
app.include_router(OrdersRouter, tags=["Orders"])
app.include_router(LicencesRouter, tags=["Licences"])
app.include_router(SellersRouter, tags=["Sellers"])
app.include_router(TransactionsRouter, tags=["Transactions"])

@app.on_event("startup")
async def start_background_task():
    asyncio.create_task(desactivation_licences_daemon())

# Hello World route (remove before release)
@app.get("/")
async def root():
    return {"message": "Hello World!"}
