from fastapi import APIRouter, HTTPException
from Schemas.news_schema import NewsSummaryRequest,FactCheckRequest
from services.news_services import getTopic
from services.news_summariser import summarise_news
from Utils.ApiResponse import ApiResponse
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from services.factCheck import summarize_with_context,search_with_serper,check_news
import traceback

router = APIRouter(prefix="/news", tags=["News Summarizer"])

@router.post("/summarize")
async def summarize_news(request: NewsSummaryRequest)->JSONResponse:
    try:
        articles=search_with_serper(query=request.query)
        print(articles)
        topic=getTopic(request.query)
        results=summarise_news(text=articles,topic=topic)
        
        response = jsonable_encoder(
        ApiResponse(
            status=200,
            message="News Acquired Successfully",
            data={"title":topic,"summary": results}
        )
    )
        return JSONResponse(response)
    
    except Exception as e:
        print("🔥 INTERNAL ERROR 🔥")
        traceback.print_exc()  # This will print the full traceback in console
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify")
async def verify_fact(request: FactCheckRequest)->JSONResponse:

    web_res=search_with_serper(query=request.news)
    result = summarize_with_context(request.news,context=web_res)
    verdict= check_news(news=request.news,context=web_res)
    response = jsonable_encoder(
        ApiResponse(
            status=200,
            message="News Acquired Successfully",
            data={"result": result,"verdict":verdict}
        )
    )
    return JSONResponse(response)