from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.action_data_class import DataInteraction


def _get_end_of_current_week():
    now = datetime.now()
    days_ahead = 0 - now.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    next_monday = now + timedelta(days=days_ahead)
    next_monday_midnight = next_monday.replace(hour=0, minute=0, second=0, microsecond=0)
    return next_monday_midnight


async def wrapper_today(session):
    await session.set_profit_stat(today=0)


async def wrapper_week(session):
    await session.set_profit_stat(week=0)


async def start_schedulers(scheduler: AsyncIOScheduler, session: DataInteraction):
    scheduler.add_job(
        wrapper_today,
        'cron',
        args=[session],
        hours=0,
        minutes=0
    )
    scheduler.add_job(
        wrapper_week,
        'interval',
        args=[session],
        days=7,
        next_run_time=_get_end_of_current_week()
    )

