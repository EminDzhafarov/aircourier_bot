import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Courier
from sqlalchemy import select

async def courier_search(data):
    session = AsyncSession
    today = datetime.datetime.today()
    query = (await session.scalars(
        select(Courier).where(Courier.city_from == data['city_from']).where(Courier.city_to == data['city_to']) \
        .where(Courier.flight_date >= today).where(Courier.status == True) \
        .order_by(Courier.flight_date))).all()
    await session.commit()
    return query