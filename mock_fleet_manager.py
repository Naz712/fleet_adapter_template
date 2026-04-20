from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NavigateRequest(BaseModel):
    map_name: str
    destination: dict
    speed_limit: float = 0.0

class LocalizeRequest(BaseModel):
    x: float
    y: float
    yaw: float
    map_name: str

@app.post('/ev1/navigate')
def navigate(robot_name: str, req: NavigateRequest):
    print(f'[navigate] {robot_name} → {req.destination} on {req.map_name}')
    return {'success': True, 'msg': ''}

@app.post('/ev1/stop')
def stop(robot_name: str):
    print(f'[stop] {robot_name} stopped')
    return {'success': True, 'msg': ''}

@app.post('/ev1/localize')
def localize(robot_name: str, req: LocalizeRequest):
    print(f'[localize] {robot_name} at x={req.x} y={req.y} on {req.map_name}')
    return {'success': True, 'msg': ''}