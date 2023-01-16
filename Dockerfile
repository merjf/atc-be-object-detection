FROM python:3.8-slim-buster
RUN mkdir /ai-ml-app-service
COPY ./ai-ml-app-service/requirements.txt /ai-ml-app-service/requirements.txt
WORKDIR /ai-ml-app-service
RUN pip3 install -r requirements.txt
COPY /ai-ml-app-service /ai-ml-app-service

CMD [ "python3", "-m" , "flask", "--app", "ai-ml-app", "run", "--host=0.0.0.0"]