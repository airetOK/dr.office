FROM python:3.9.12-slim
RUN apt-get update && \
    apt-get install -y libpq-dev gcc
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
WORKDIR /dr.office
COPY . .
ENV FLASK_APP=app.py
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
EXPOSE 5000