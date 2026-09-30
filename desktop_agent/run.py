import os
import uvicorn

if __name__=="__main__":
    uvicorn.run("agent:app",host="127.0.0.1",port=int(os.getenv("ULTRON_AGENT_PORT","8765")),reload=False)
