FROM python:3.7
WORKDIR /source
COPY requirements.txt requirements.txt
#this packages need be extracted to poetry
RUN pip3 install uvicorn aioredis fastapi_cache2 python-dotenv nest_asyncio pyngrok
RUN pip3 install -r requirements.txt
COPY ./ /source
CMD ["python3", "main.py" ]
#CMD ["uvicorn", "main:app","--reload", "--host", "0.0.0.0", "--port", "8888" ]