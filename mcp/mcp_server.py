import http
import json
import math
from typing import List, Optional
from fastapi import Body, FastAPI, HTTPException, Query, requests
from fastapi_mcp import FastApiMCP
from geopy.geocoders import Nominatim

from pydantic import BaseModel, Field, validator
import uvicorn
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from fastapi import FastAPI, Body, HTTPException
import httpx

app = FastAPI()


API_KEY = "***************"

@app.get("/ip-to-location")
async def ip_to_location(ip: str = Query(..., description="IP address to locate")):
    headers = {
        'content-type': "application/json",
        'authorization': f"apikey {API_KEY}"
    }

    url = f"https://api.collectapi.com/ip/ipToLocation?data.ip={ip}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail=f"Request failed: {str(e)}")

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"CollectAPI failed: {response.text}")

        return response.json()



@app.post("/", description="Retrieve the coordinates (latitude and longitude) of a given city or settlement.")
async def get_coordinate(city: str):
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city)
    return [location.latitude, location.longitude]


@app.post("/destination", description="Calculate the great-circle (straight line) distance between two coordinates using the Haversine formula.")
async def haversine(lat1: float, lon1: float, lat2: float, lon2: float):
    R = 6371  

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance


mcp = FastApiMCP(app)
mcp.mount()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8081)
