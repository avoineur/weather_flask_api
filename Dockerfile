# Dockerfile

FROM python:3.9-slim

#ENV PYTHONPATH "${PYTHONPATH}:app/"

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "wsgi.py"]