from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import commonteamroster
from nba_api.stats.endpoints import commonallplayers
from nba_api.stats.endpoints import teaminfocommon
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True
)

# # Mount static files directory
# app.mount("/static", StaticFiles(directory="."), name="static")

# @app.get("/")
# async def read_root():
#     return FileResponse("final.html")

# @app.get("/debug")
# async def read_debug():
#     return FileResponse("debug.html")

@app.get("/player")
def get_all_players():
    list = commonallplayers.CommonAllPlayers()
    return list.get_dict() 


@app.get("/player/{player_id}")
def get_player_stats(player_id: int):
    stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    return stats.get_dict()

# get stats tables which include teams played
@app.get("/player/{player_id}/teams")
def get_player_team_history(player_id: int):
    player = playercareerstats.PlayerCareerStats(player_id=player_id).get_dict()
    return {
        (row[1], row[3])  # SEASON_ID and TEAM_ID
        for row in player["resultSets"][0]["rowSet"]
    }

@app.get("/team/{team_id}")
def get_team_name(team_id: int):
    team = teaminfocommon.TeamInfoCommon(team_id=team_id).get_dict()
    return {
        (row[2], row[3])  # TEAM_CITY and TEAM_NAME
        for row in team["resultSets"][0]["rowSet"]
    }


#retrieves roster based on team and season
@app.get("/team/{team_id}/roster/{season}")
def get_team_roster(team_id: int, season: str):
    roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season).get_dict()
    return {
        (row[3], row[14], row[6])  # Name and PLAYER_ID
        for row in roster["resultSets"][0]["rowSet"]
    }

# uvicorn api_test:app --reload
# http://localhost:8000/player/203999