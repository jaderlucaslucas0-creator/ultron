from app.agents.registry import route

class Orchestrator:
    async def handle(self, message: str) -> str:
        agent = route(message)
        return await agent(message)

orchestrator = Orchestrator()
