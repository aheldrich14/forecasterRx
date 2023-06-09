FROM python:3.8

COPY requirements.txt /opt/app/requirements.txt
WORKDIR /opt/app
RUN pip install -r requirements.txt

COPY . /opt/app
EXPOSE 8050
CMD ["python", "app.py"]
