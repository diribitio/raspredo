from typing import List
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from CHAProblem import *


class Preference(BaseModel):
    house_id: int
    weight: int


class House(BaseModel):
    id: int
    capacity: int


class Agent(BaseModel):
    id: int
    preferences: List[Preference]


class Request(BaseModel):
    agents: List[Agent]
    houses: List[House]


app = FastAPI()


@app.post("/")
async def main(req: Request):
    a = []
    h = []
    e = []

    for house in req.houses:
        h.append(houseInternal('house-' + str(house.id), house.capacity))

    for agent in req.agents:
        agent_preferences = []
        for preference in agent.preferences:
            e.append(('agent-' + str(agent.id), 'house-' + str(preference.house_id), preference.weight))
            for house in h:
                if house.name == 'house-' + str(preference.house_id):
                    agent_preferences.append(house)
        agent.preferences = agent_preferences
        a.append(agentInternal('agent-' + str(agent.id), agent.preferences))

    # print the attributes of the agents and houses
    for agent in a:
        print(agent.name)
        print(agent.preferences)
    for house in h:
        print(house.name)
        print(house.capacity)
    for edge in e:
        print(edge)

    chap = CHAProblem(a, h, e, False, 9999)
    chap.solve()

    return {"message": [chap.return_values['solution'][0]['agents'], chap.return_values['solution'][1]['houses'],
                        chap.return_values['solution'][3]['matchings']]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
