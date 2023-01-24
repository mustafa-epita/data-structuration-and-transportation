# Final Assignment by Mustafa Faris and Swati Khandare
import requests
from datetime import date
from time import mktime
from typing import Dict, List

from datetime import datetime, timedelta




def fetchDepartingFlights(ds: str) -> List[Dict]:
  now = datetime.strptime(ds, '%Y-%m-%d')
  d = now - timedelta(days=1)
  prevWeek = d.date().strftime('%Y-%m-%d')

  BASE_URL = "https://opensky-network.org/api"
  params = {
    "airport": "LFPG",
    "begin": toSecondsSinceEpoch(prevWeek),
    "end": toSecondsSinceEpoch(ds)
  }
  cdg_flights = f"{BASE_URL}/flights/departure"
  response = requests.get(cdg_flights, params=params)
  return response.json()

def toSecondsSinceEpoch(input_date: str) -> int:
  return int(mktime(date.fromisoformat(input_date).timetuple()))