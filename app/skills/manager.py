from app.skills.builtin.calculator import CalculatorSkill
SKILLS=[CalculatorSkill()]
def find_skill(text):
    return next((s for s in SKILLS if s.matches(text)),None)
def skill_context():
    return "\n".join("- %s: %s" % (s.name,s.description) for s in SKILLS)
