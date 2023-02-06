FROM python:3.8-slim-buster
RUN mkdir /service
COPY ./service/requirements.txt /service/requirements.txt
WORKDIR /service
RUN pip3 install -r requirements.txt
COPY /service /service

CMD [ "python3", "-m" , "flask", "--app", "ai-ml-app", "run", "--host=0.0.0.0"]