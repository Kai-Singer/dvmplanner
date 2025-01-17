from datetime import timedelta
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def formatTimedelta(time: timedelta):
  days = time.days
  hours, rest = divmod(time.seconds, 3600)
  hours += days * 24
  minutes, seconds = divmod(rest, 60)
  return f'{hours:02}:{minutes:02}:{seconds:02}'