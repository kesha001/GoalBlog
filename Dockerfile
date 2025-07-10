FROM python:3.12-slim

WORKDIR ./

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY app ./app

COPY goalblog.py config.py babel.cfg README.md tests ./
COPY entrypoint.sh ./entrypoint.sh
COPY migrations migrations

ENV FLASK_APP goalblog.py
ENV FLASK_DEBUG 0

RUN chmod a+x entrypoint.sh

RUN pybabel compile -d app/translations

EXPOSE 5000

ENTRYPOINT ["./entrypoint.sh"]


