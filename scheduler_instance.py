from apscheduler.schedulers.background import BackgroundScheduler
import pytz

lima_tz = pytz.timezone('America/Lima')
scheduler = BackgroundScheduler(timezone=lima_tz)