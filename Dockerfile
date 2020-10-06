FROM python:3.7
LABEL maintainer="lucas.key.kawazoi@gmail.com"

ENV PYTHONPATH=/app
WORKDIR /app

RUN apt-get update
RUN apt-get install gettext -y

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY .config.template .
RUN mkdir ~/.aws/
RUN envsubst < /app/.config.template > ~/.aws/config
RUN rm /app/.config.template

COPY . /app
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["python","src/main.py"]
EXPOSE 8000
