from fastapi import FastAPI, Query
import requests

app = FastAPI()

file_id = '1zOweCB2jidgHwirp_8oBnFyDgJKkWdDA'
url = f'https://drive.google.com/uc?export=download&id={file_id}'
response = requests.get(url=url)
dados_json = response.json()

@app.get('/users/pais/')
def users(pais: str = Query(None)):
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
    pessoas_times = []
    total_users = 0
    for item in dados_json:
        if item["team"]["name"] == team:
            team_name = item["team"]["name"]
            
            pessoas_times.append({
                "team_name":item["team"]["name"],
                "leader":item["team"]["leader"],
                "projects":item["team"]["projects"]
            })
            total_users += 1
            
    leaders = 0
    completed_projects = 0
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
    }
