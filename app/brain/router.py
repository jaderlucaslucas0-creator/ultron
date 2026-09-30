from app.skills.manager import find_skill
from app.brain.reasoning import answer_with_ai

def route_request(text):
    return find_skill(text) or answer_with_ai
