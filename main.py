import requests
import json
from fastapi import FastAPI, Query
from time import perf_counter

app = FastAPI()

JSON_100K = '1zOweCB2jidgHwirp_8oBnFyDgJKkWdDA'
JSON_1K = '1BX03cWxkvB_MbZN8_vtTJBDGiCufyO92'

file_id = '1zOweCB2jidgHwirp_8oBnFyDgJKkWdDA'
url = f'https://drive.google.com/uc?export=download&id={JSON_1K}'

def request_url():
    response = requests.get(url=url)
    return response

@app.get('/evaluation/')
def evaluation():
    start_time_response = perf_counter()
    
    response = request_url()
    dados_json = response.json()
    team_insights(team="UX Wizards")
    
    end_time_response = perf_counter()
    
    time_response = (end_time_response - start_time_response) * 1000
    return {
        "status":response.status_code,
        "miliseconds":f'{time_response:.2f}ms'
    }

@app.get('/users/pais/')
def users(pais: str = Query(None)):
    response = request_url()
    dados_json = response.json()
    
    dados_filtrados = []
    
    for item in dados_json:
        if item["country"].lower() == pais.lower():
            dados_filtrados.append({
                "nome":item["name"],
                "idade":item["age"],
                "país":item["country"]
            })
    
    if response.status_code == 200:
        return dados_filtrados
    else:
        return {"erro":f"{response.status_code} - {response.text}"}
    
@app.get('/superusers/')
def super_users():
    response = request_url()
    dados_json = response.json()
    
    dados_filtrados = []
    
    for item in dados_json:
        if item["score"] >= 900 and item["active"] == True:
            dados_filtrados.append({
                "nome":item["name"],
                "idade":item["age"],
                "país":item["country"],
                "score":item["score"],
                "ativo":item["active"],
                
            })
    
    if response.status_code == 200:
        return dados_filtrados
    else:
        return {"erro":f"{response.status_code} - {response.text}"}

@app.get(f'/team-insights/')
def team_insights(team: str = Query(None)):
    response = request_url()
    dados_json = response.json()
    
    pessoas_times = []
    
    total_users = 0
    active_users = 0
    leaders = 0
    completed_projects = 0
    
    for item in dados_json:
        if item["team"]["name"] == team:
            team_name = item["team"]["name"]
            
            if item["active"] == True:
                active_users += 1
            
            pessoas_times.append({
                "team_name":item["team"]["name"],
                "leader":item["team"]["leader"],
                "projects":item["team"]["projects"]
            })
            total_users += 1
    active_users_percentage = round((active_users / total_users) * 100, 2)
    
    for pessoa in pessoas_times:
        if pessoa["leader"] == True:
            leaders += 1
        for i in range(len(pessoa["projects"])):
            if pessoa["projects"][i]["completed"]:
                completed_projects += 1
    
    return {
        "name":team_name,
        "people":total_users,
        "leaders":leaders,
        "completed_projects":completed_projects,
        "active_users_percentage":active_users_percentage,
    }
