from fastapi import FastAPI, HTTPException
import requests
import datetime
app = FastAPI()

api_url:str = "https://api.aelf.org//v1/lectures"

@app.get("/")
def home():

    return {}

@app.get("/lecture")
async def get_lecture(date:str = str(datetime.date.today()) , zone:str = "afrique"):
    
    response = requests.get(f"https://api.aelf.org//v1/messes/{date}/{zone}")


    return {"status_code":response.status_code, "data":{"date":datetime.date.today(), "ref":response.json()["messes"][0]['lectures'][2]["ref"]}}


@app.get("/lectures")
def get_all_lectures(start:str, end:str, zone:str = "afrique"):

    start_list = start.split('-')
    
    end_list = end.split('-')

    start_date = datetime.date(int(start_list[0]), int(start_list[1]), int(start_list[2]))

    end_date = datetime.date(int(end_list[0]), int(end_list[1]), int(end_list[2]))

    delta = datetime.timedelta(days=1)

    dates = []

    res:list = []
 
    while start_date <= end_date:

        dates.append(start_date.isoformat())

        start_date += delta

    for dt in dates:
        
        response = requests.get(f"https://api.aelf.org//v1/messes/{dt}/{zone}")

        res.append({"date":dt,"ref":response.json()["messes"][0]['lectures'][2]["ref"]})
        

    return{"status_code":"200", "data":res}

@app.put("/delete/{id}")
async def get_all_proxies(id:int):

    return {}

