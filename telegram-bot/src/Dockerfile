FROM python:3.10-slim

ARG heroku_app_name
ARG api_uri
ARG mode
ARG lambda_function
ARG aws_access_key
ARG aws_secret_key
ARG bot_token

ENV HEROKU_APP_NAME = ${heroku_app_name}
ENV API_URI = ${api_uri}
ENV MODE = ${mode}
ENV LAMBDA_FUNCTION = ${lambda_function}
ENV AWS_ACCESS_KEY = ${aws_access_key}
ENV AWS_SECRET_KEY = ${aws_secret_key}
ENV BOT_TOKEN = ${bot_token}

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]