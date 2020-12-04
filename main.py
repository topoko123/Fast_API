#Author: Chatchawal Sangkeettrakarn
#Date: September 20,2020.

from fastapi import FastAPI
import uvicorn
import numpy as np
import re
import math
import requests
from bs4 import BeautifulSoup
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def result(res):
    return {"result":res}

@app.get("/")
async def main():
    return 'Hello World'

@app.get("/test")
async def test():
    return 'Test Tutorial'

@app.get("/add")
async def add(a: int = 0, b: int = 0):
    return a+b

@app.get("/mul")
async def mul(a: int = 0, b: int = 0):
    return a*b

@app.get("/pow")
async def pow(a: int = 0, b: int = 0):
    return math.pow(a,b)


def tonumlist(li):
    ls = li.split(',')
    for i in range(len(ls)):
        ls[i] = float(ls[i])
    return list(ls)

@app.get("/asc")
async def asc(li):
    ls = tonumlist(li)
    ls.sort()
    return ls

@app.get("/desc")
async def desc(li):
    ls = tonumlist(li)
    ls.sort(reverse=True)
    return ls

@app.get("/sum")
async def sum(li):
    ls = tonumlist(li)
    return np.sum(np.array(ls))

@app.get("/avg")
async def avg(li):
    ls = tonumlist(li)
    return np.average(ls)

@app.get("/mean")
async def mean(li):
    ls = tonumlist(li)
    return np.mean(ls)

@app.get("/max")
async def max(li):
    ls = tonumlist(li)
    return np.amax(ls)

@app.get("/min")
async def min(li):
    ls = tonumlist(li)
    return np.amin(ls)

@app.get("/validation-ctzid")
async def validation_ctzid(text):
    if(len(text) != 13):
        return False
    
    sum = 0
    listdata = list(text)
    
    for i in range(12):
        sum+=int(listdata[i])*(13-i)

    d13 = (11-(sum%11))%10
        
    return d13==int(listdata[12])

@app.get("/validation-email")
async def validation_email(text):  
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.search(regex,text):
        return True
    else:
        return False
    
@app.get("/bmi")
async def bmi(h:int=1, w:int=0 ):
    h = (h/100)**2
    bmi = w/h
    des = ""
    
    if (bmi < 18.5):
        des = "น้ำหนักต่ำกว่าเกณฑ์"
    elif (bmi >= 18.5 and bmi <= 22.9 ):
        des = "สมส่วน"
    elif (bmi >=23.0 and 24.9):
        des = "น้ำหนักเกิน"
    elif (bmi >=25.0 and 29.9):
        des ="โรคอ้วน"
    else :
        des = "โรคอ้วนอันตราย"

    js = {'bmi':f'{bmi:.2f}', 'description': des}
    return js
    
@app.get("/basenum")
async def basenumber(BaseNumberInput:str = 0, BaseNumberFunction:str = ""):
    BaseNumberFunction_ = BaseNumberFunction.upper()
    ResultFirstRow_ = ""
    ResultSecondRow_ = ""
    #Base Number :Binary,Dec,Oce
    try:
        if (BaseNumberFunction_ == "B2O"):   
            if (re.search('[0-9]', BaseNumberInput)):
                BinToDec_ = int(BaseNumberInput, 2)
                ResultFirstRow_ = "ฐานสิบ: "+ str(int (BaseNumberInput, 2))
                ResultSecondRow_ = "ฐานแปด: "+ oct(int(BinToDec_)).replace("0o", "")
            else :
               ResultFirstRow_ = "กรอกไม่ถูกต้อง"
               ResultSecondRow_ = "กรอกไม่ถูกต้อง"

        #Base Number :Binary,Dec,Hex      
        elif (BaseNumberFunction_ == "B2H"):
            
            if (re.search('[0-1]', BaseNumberInput)):
                BinToDec_ = int(BaseNumberInput, 2)
                ResultFirstRow_ = "ฐานสิบ: "+ str(int (BaseNumberInput, 2))
                ResultSecondRow_ = "ฐานสิบหก: " + hex(int(BinToDec_)).replace("0x","").upper() 
            else :
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                ResultSecondRow_ = "กรอกไม่ถูกต้อง"
                
        #Base number :Oct,binary,dec
        elif (BaseNumberFunction_ == "O2B"):  
            if (re.search('[0-9]', BaseNumberInput)):
                OctToDec_ = int(BaseNumberInput, 8)
                ResultFirstRow_ = "ฐานสิบ: "+ str(int(BaseNumberInput, 8))
                ResultSecondRow_ = "ฐานสอง: "+ bin(int(OctToDec_)).replace("0b", "")
            else :
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                ResultSecondRow_ = "กรอกไม่ถูกต้อง"
                
        #Base number :Oct,Dec,Hex
        elif (BaseNumberFunction_ == "O2H"):
            if (re.search('[0-9]', BaseNumberInput)):
                OctToDec_ = int(BaseNumberInput, 8)
                ResultFirstRow_ = "ฐานสิบ: "+ str(int(BaseNumberInput, 8))
                ResultSecondRow_ = "ฐานสิบหก: "+ hex(int(OctToDec_)).replace("0x","").upper()
            else :
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                ResultSecondRow_ = "กรอกไม่ถูกต้อง"
                
        #Base Number :Hec to Bin
        elif (BaseNumberFunction_ == "H2B"):           
            if (re.search('[0-9a-fA-F]', BaseNumberInput)):
                HexToDec_ = int(BaseNumberInput, 16)
                ResultFirstRow_ = "ฐานสิบ: "+ str(int(BaseNumberInput, 16))
                ResultSecondRow_ = "ฐานสอง: "+ bin(int(HexToDec_)).replace("0b", "")
            else:
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                ResultSecondRow_ = "กรอกไม่ถูกต้อง"
                
        #Base Number :Hex to Decimal
        elif (BaseNumberFunction_ == "H2O"):        
            if (re.search('[0-9a-fA-F]', BaseNumberInput)):
                HexToDec_ = int(BaseNumberInput, 16)
                ResultFirstRow_ = "ฐานสิบ"+ str(int(BaseNumberInput, 16))
                ResultSecondRow_ = "ฐานแปด" + oct(int(HexToDec_)).replace("0o", "")
            else :
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                ResultSecondRow_ = "กรอกไม่ถูกต้อง"
                
        #Base Number :Dec,Binary,Oct
        elif (BaseNumberFunction_ == "D2O"):
            InputFilter_ = BaseNumberInput.isdigit()
            if (InputFilter_ == False):
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                
            elif (InputFilter_ == True):
                _InDecimal = int(BaseNumberInput)
                ResultFirstRow_ = "ฐานสอง: "+ str(bin(int(_InDecimal)).replace("0b", ""))
                ResultSecondRow_ = "ฐานแปด: "+ str(oct(int(_InDecimal)).replace("0o", ""))
            else:
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                ResultSecondRow_ = "กรอกไม่ถูกต้อง"
                
        #Base Number : Dec,Binary,HEX
        elif (BaseNumberFunction_ == "D2H"):
            InputFilter_ = BaseNumberInput.isdigit()
            if (InputFilter_ == False):                
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                
            elif (InputFilter_ == True):
                _InDecimal = int(BaseNumberInput)
                ResultFirstRow_ = "ฐานสอง: "+ str(bin(int(_InDecimal)).replace("0b", ""))
                ResultSecondRow_ = "ฐานสิบหก: "+ str(hex(int(_InDecimal)).replace("0x", "").upper())
            else :
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                ResultSecondRow_ = "กรอกไม่ถูกต้อง"    
        
        #Base Number :Dec,Binary
        elif (BaseNumberFunction_ == "D2B"):
            InputFilter_ = BaseNumberInput.isdigit()
            if (InputFilter_ == False):                
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                
            elif (InputFilter_ == True):
                _InDecimal = int(BaseNumberInput)
                ResultFirstRow_ = "ฐานสอง: "+ str(bin(int(_InDecimal)).replace("0b", ""))
                ResultSecondRow_ = "ไม่มีเลขฐานแล้ว  :p"
        else :
                ResultFirstRow_ = "กรอกไม่ถูกต้อง"
                ResultSecondRow_ = "กรอกไม่ถูกต้อง"

    except Exception as e:
        print (e,type(e))
        ResultFirstRow_ = "กรอกไม่ถูกต้อง"
        ResultSecondRow_ = "กรอกไม่ถูกต้อง"
    
    print (ResultFirstRow_, ResultSecondRow_)
    jsonout = {'Number1':ResultFirstRow_, 'Number2':ResultSecondRow_}
    return jsonout

@app.get("/google-search",response_class=PlainTextResponse)
def google_search(text):
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:81.0) Gecko/20100101 Firefox/81.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    url = 'https://www.google.com/search?q=' + str(text)
    res = requests.get(url, headers = headers)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    t = soup.findAll('div', {'class':"r"})
    i = 0
    result = ''
    for a in t:
        href = a.a['href']
        head = a.h3.text
        result = result + head + '<br>' + href + '<br><br>'
        i += 1
        if(i >= 5):
            break
    
    return(result)




if __name__ == '__main__':
   uvicorn.run(app, host="0.0.0.0", port=80, debug=True) 