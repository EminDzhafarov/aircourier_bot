from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from bot.db.models import Courier, Stats_search, Stats, Blacklist, Admins
from dateutil.parser import isoparse
from datetime import datetime

async def add_courier(session: AsyncSession, data):
    await session.execute(insert(Courier).values(
            user_id=data['user_id'],
            user_name = data['user_name'],
            city_from=data['city_from'],
            city_to=data['city_to'],
            flight_date=isoparse(data['flight_date']),
            phone=data['phone'],
            info=data['info'],
            status=True
        )
    )
    await session.commit()

async def find_couriers(session: AsyncSession, data):
    today = datetime.today()
    return (await session.scalars(select(Courier)
                              .where(Courier.city_from == data['city_from'])
                              .where(Courier.city_to == data['city_to'])
                              .where(Courier.flight_date >= today).where(Courier.status == True)
                              .order_by(Courier.flight_date))).all()

async def add_search_stat(session: AsyncSession, data):
    today = datetime.today()
    await session.execute(insert(
        Stats_search).values(
        user_id=data['user_id'],
        city_from=data['city_from'],
        city_to=data['city_to'],
        timestamp=today))
    await session.commit()

async def get_id_from_link(session: AsyncSession, user_id):
    today = datetime.today()
    return (await session.scalars(select(Courier)
                           .where(Courier.user_id == int(user_id))
                           .where(Courier.flight_date >= today)
                           .where(Courier.status == True)
                           .order_by(Courier.flight_date))).all()

async def get_admin(session: AsyncSession, user_id):
    return (await session.execute(select(Admins.user_id).filter_by(user_id=user_id))).scalar()

async def is_new_user(session: AsyncSession, user_id):
    return (await session.execute(select(Stats).where(Stats.user_id == user_id))).first()

async def add_to_stat(session: AsyncSession, user_id):
    await session.merge(Stats(user_id=user_id, timestamp=datetime.now()))
    await session.commit()

async def get_blacklist(session: AsyncSession, user_id):
    return (await session.execute(select(Blacklist.user_id).filter_by(user_id=user_id))).scalar()

async def get_all_blacklist(session: AsyncSession):
    return (await session.scalars(select(Blacklist))).all()

async def add_to_blacklist(session: AsyncSession, data):
    await session.execute(insert(Blacklist).values(user_id=data['user_id']))
    await session.commit()

async def del_from_blacklist(session: AsyncSession, user_id):
    await session.execute(delete(Blacklist).where(Blacklist.user_id == user_id))
    await session.commit()

async def get_flights(session: AsyncSession, user_id):
    today = datetime.today()
    return (await session.scalars(select(Courier)
                           .where(Courier.user_id == user_id)
                           .where(Courier.flight_date >= today)
                           .where(Courier.status == True))).all()

async def del_from_flight(session: AsyncSession, flight_id):
    await session.execute(update(Courier).where(Courier.id == flight_id).values(status=False))
    await session.commit()