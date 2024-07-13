from fastapi import FastAPI, HTTPException
import requests
import datetime


app = FastAPI()


def tomorrow(date:str):
    """Allow to get the following date of given date.\n
        Date must be in isoformat
    """
    dateList = date.split('-')

    firstDate = datetime.date(int(dateList[0]), int(dateList[1]), int(dateList[2]))

    delta = datetime.timedelta(days=1)

    tomorrowDate = firstDate + delta

    return tomorrowDate.isoformat()


def month (date:str):
    """Allow to get list of dates relate to month.\n 
        Date must be in isoformat
    """
    new_date:str = date+"-01"
    monthDate:list = []
    monthDate.append(new_date)
    while tomorrow(monthDate[-1]).split("-")[1] == date.split("-")[1]:
        monthDate.append(tomorrow(monthDate[-1]))

    return monthDate
    

@app.get("/")
def home():

    return {}
    

@app.get("/lecture")
async def get_lecture(date:str = str(datetime.date.today()) , zone:str = "afrique"):
    
    try:
        response = requests.get(f"https://api.aelf.org//v1/messes/{date}/{zone}")
        if response.status_code == 200:
            #res = {"status_code":response.status_code, "data":{"date":datetime.date.today().strftime("%d %B, %Y"), "ref":response.json()}}
            #print(res)
            return {"status_code":response.status_code, "data":{"date":date, "ref":response.json()["messes"][0]['lectures'][2]["ref"], "text":response.json()["messes"][0]['lectures'][2]['contenu']}}
        else:
            return {"status_code":response.status_code, "response":response.json()}

    except Exception as e:
        return {"status":response.status_code, "response":response.text, "message":e}


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


@app.get("/month")
async def get_all_monthly(date:str, zone:str="afrique"):

    dates = month(date)

    res:list = []

    for el in dates:

        response = requests.get(f"https://api.aelf.org//v1/messes/{el}/{zone}")

        res.append({"date":el,"ref":response.json()["messes"][0]['lectures'][-1]["ref"]})

    return {"status_code":"200", "data":res}


