FROM python:3.7
COPY requirements.txt ./app/requirements.txt
RUN pip3 install uvicorn
RUN pip3 install -r app/requirements.txt
COPY ./ /app
CMD ["python3", "app/main.py" ]
#CMD ["uvicorn", "source.main:source","--reload", "--host", "localhost", "--port", "8080" ]