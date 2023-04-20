import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

async def courier_search(data):
    today = datetime.today()
    query = (await session.execute(select(Courier).where(Courier.city == data['city_from']).where(Courier.dest == data['city_to']) \
                    .where(Courier.flight_date >= today).where(Courier.status == True) \
                    .order_by(Courier.flight_date))).all()
    await session.commit()
    return query