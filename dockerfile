FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Replace 'app.py' with the name of your main application script
CMD python -m venv venv pip install -r requirements.txt uvicorn main:app --reload