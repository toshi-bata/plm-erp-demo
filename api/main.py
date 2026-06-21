from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import plm, erp

app = FastAPI(
    title="PLM/ERP Demo API",
    description="Manufacturing PLM and ERP data lookup API for use with HOOPS AI MCP results.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plm.router, prefix="/plm", tags=["PLM"])
app.include_router(erp.router, prefix="/erp", tags=["ERP"])
app.include_router(erp.query_router, prefix="/query", tags=["Bulk Query"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "service": "PLM/ERP Demo API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="0.0.0.0", port=8010, reload=True)
