from app.skills.manager import find_skill
from app.brain.reasoning import answer_with_ai
from app.agents.registry import choose_agent

def route_request(text,db=None,conversation_id=None,memories=None):
    skill=find_skill(text)
    if skill:
        return skill
    agent=choose_agent(text)
    if db is None or memories is None:
        return agent.run(text)
    return answer_with_ai(text,db,conversation_id,memories,agent=agent)
