
from fastapi import FastAPI

from Routes import news_routes

app = FastAPI(title="News App Backend")

# Include routes
app.include_router(news_routes.router)

print("✅ Loaded routes:")
for route in app.routes:
    print(" -", route.path)

@app.get("/")
def root():
    return {"message": "News App Backend running successfully 🚀"}
