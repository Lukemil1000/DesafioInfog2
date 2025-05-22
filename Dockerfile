FROM python:3.13-slim

WORKDIR app/
COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["uvicorn", "DesafioInfog2.main:app", "--host", "0.0.0.0"]