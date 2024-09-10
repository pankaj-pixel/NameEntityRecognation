from fastapi import FastAPI,Request,UploadFile,File,HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "html": None})

@app.post("/entity")
async def entity(request: Request, file: UploadFile = File(...)):
    try:
        #content = file.read()
        if not file:
              return {"message": "No file sent"}
        else:
            content = await file.read()
            decode_file =content.decode("utf-8")       
            docs = nlp(decode_file)
            print(docs)
            html_res = displacy.render(docs, style="ent", page=True)
            return templates.TemplateResponse("index.html", {"request": request, "html": html_res})
        #
        #html =displacy.render(docs,style='ent')
        #return HTMLResponse('index.html',content=docs)
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))
