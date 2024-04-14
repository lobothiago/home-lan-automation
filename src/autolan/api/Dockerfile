FROM python:3.8.10-slim

ARG PIP_INDEX_URL="https://pypi.org/simple"
ARG NETRC
    
ENV AUTOLAN_META="/opt/autolan/metadata"
RUN mkdir -p $AUTOLAN_META

COPY requirements.txt $AUTOLAN_META/requirements.txt

RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --index-url "$PIP_INDEX_URL" -r $AUTOLAN_META/requirements.txt

ENV APP_HOME="/opt/app"
RUN mkdir -p $APP_HOME
COPY autolan/ $APP_HOME/autolan

WORKDIR $APP_HOME
ENV PYTHONPATH="$APP_HOME:$PYTHONPATH"

EXPOSE 8080

CMD [ "gunicorn", \
      "-c", "autolan/api/gunicorn.conf.py", \
      "autolan.api.main:application()" ]
