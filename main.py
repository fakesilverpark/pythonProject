#main.py
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
app = FastAPI()

datas = []

file_path = '/Users/Python/work/athlete/athlete/선수_등록_통계.txt'
f = open(file_path, 'r')
lines = f.readlines()[2:]
header = ["종목명", "연령", "남", "여", "계"]

for line in lines:
    line = line.replace("\n", " ")
    line = line.split('\t')
    datas.append(line)

def number(num):
    num = num.strip()
    if (num.isdigit()):
        num = int(num)
    else:
        num = 0
    return num

def dictioning(x, y):
    diction = {}
    for i in range(len(x)):
        diction[x[i]] = y[i]
    return diction

def searchByAge(age):
    wanted = []
    for data in datas:
        if (data[1] == age):
            num = number(data[-1])
            temp = [data[0], num]
            wanted.append(temp)
    x = []
    y = []

    for key, value in wanted:
        x.append(key)
        y.append(value)
    
    return dictioning(x, y)

def searchBySports(sport):
    sport = sport.split()
    descision = sport[1]
    sport = sport[0]
    wanted = []
    for data in range(len(datas)):
        if (datas[data][0] == sport):
            wanted = datas[data:data+5]
            break
    if (wanted == []):
        print("말씀하신 데이터는 검색할 수 없습니다")
        return []
    
    if (descision == "성별"):  # gender
        x = ['남성', '여성', '합계']
        men = number(wanted[0][2]) + number(wanted[1][2]) + number(wanted[2][2])
        women = number(wanted[0][3]) + number(wanted[1][3]) + number(wanted[2][3])
        total = number(wanted[0][4]) + number(wanted[1][4]) + number(wanted[2][4])
        y = [men, women, total]
    else:  # age
        x = ['12세이하부', '15세이하부', '18세이하부', '대학부', '일반부']
        y = [number(wanted[0][-1]), number(wanted[1][-1]), number(wanted[2][-1]), number(wanted[3][-1]), number(wanted[4][-1])]

    return dictioning(x, y)

def searchByWonmen():
    wanted = []
    for data in datas:
        num = number(data[3])
        temp = [data[0], num]
        wanted.append(temp)
    x = []
    y = []

    for key, value in wanted:
        x.append(key)
        y.append(value)

    return dictioning(x, y)

def searchByMen():
    wanted = []
    for data in datas:
        num = number(data[2])
        temp = [data[0], num]
        wanted.append(temp)
    x = []
    y = []

    for key, value in wanted:
        x.append(key)
        y.append(value)
    
    return dictioning(x, y)

def searchByTotal():
    wanted = []
    for data in datas:
        num = number(data[-1])
        temp = [data[0], num]
        wanted.append(temp)
    x = []
    y = []

    for key, value in wanted:
        x.append(key)
        y.append(value)
    
    return dictioning(x, y)

def generate_athlete_data(index):
    # 입력된 index에 따른 데이터 처리
    match index:
        case "12세이하부":
            data = searchByAge("12세이하부")
        case "15세이하부":
            data = searchByAge("15세이하부")
        case "18세이하부":
            data = searchByAge("18세이하부")
        case "대학부":
            data = searchByAge("대학부")
        case "일반부":
            data = searchByAge("일반부")
        case "여성":
            data = searchByWonmen()
        case "남성":
            data = searchByMen()
        case "합계":
            data = searchByTotal()
        case _:
            data = searchBySports(index)

    # data가 딕셔너리 형식일 경우 DataFrame 생성
    if isinstance(data, dict):
        return pd.DataFrame(data, index=[0])  # 딕셔너리를 기반으로 DataFrame 생성
    else:
        print("No valid data found.")
        return pd.DataFrame()  # 데이터가 없으면 빈 DataFrame 반환

@app.get("/", response_class=HTMLResponse)
async def show_weather():
    # 사용자로부터 입력을 받는 HTML 폼 생성
    html_content = f"""
    <html>
        <head>
            <title>선수 등록 정보 입력</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; }}
                table {{ margin: 0 auto; border-collapse: collapse; width: 80%; }}
                th, td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                th {{ background-color: #f4f4f4; }}
            </style>
        </head>
        <body>
            <h1>선수 등록 정보 검색</h1>
            <form method="get" action="/show_data">
                <label for="index">검색할 종목명:</label>
                <input type="text" id="index" name="index" placeholder="예: 축구, 농구 등">
                <input type="submit" value="검색">
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/show_data", response_class=HTMLResponse)
async def show_data(index: str):
    # 사용자가 입력한 값(index)을 처리하고 결과를 반환
    data = generate_athlete_data(index)  # 입력된 index 값으로 데이터 처리
    
    # HTML 테이블로 변환
    table_html = data.to_html(index=False, escape=False, justify="center", border=1)

    # HTML 페이지 생성
    html_content = f"""
    <html>
        <head>
            <title>{index} 선수 등록 정보</title>
            <style>
                body {{ font-family: Arial, sans-serif; text-align: center; }}
                table {{ margin: 0 auto; border-collapse: collapse; width: 80%; }}
                th, td {{ padding: 10px; border: 1px solid #ddd; text-align: center; }}
                th {{ background-color: #f4f4f4; }}
            </style>
        </head>
        <body>
            <h1>{index} 선수 등록 정보</h1>
            {table_html}
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
