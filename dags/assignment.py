# Final Assignment by Mustafa Faris and Swati Khandare

import json
from datetime import datetime
from airflow.decorators import dag, task
from typing import Dict, List
from collections import Counter
from helpers import fetchDepartingFlights

@dag(
  schedule=None,
  start_date=datetime(2023, 1, 11),
  catchup=False
)
def assignment():

  @task
  def reading(ds=None) -> List[Dict]:
    flights = fetchDepartingFlights(ds)
    return flights

  @task
  def writing(content: str, fileName: str) -> None:
    f = open(f"./dags/{fileName}",'w+')
    f.write(content)

  @task
  def transformation(flights: List[Dict]) -> str:
    counter = Counter([flight["estArrivalAirport"] for flight in flights if (flight["estArrivalAirport"] is not None and flight["estArrivalAirport"] != "LFPG")])
    airportName, airportArrivingFlightsCount = counter.most_common(1)[0]
    content = f"The airport most arrival flights: \"{airportName}\", with total number of flights:  {airportArrivingFlightsCount}"
    return content

  @task
  def transformationToJsonStr(flights: List[Dict]) -> str:
    return json.dumps(flights)

  flights = reading()
  writing(transformationToJsonStr(flights), "flights.json")
  writing(transformation(flights), "transformation.txt")

_ = assignment()