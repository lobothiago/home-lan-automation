FROM python:3.8.10-slim

ARG PIP_INDEX_URL="https://pypi.org/simple"
ARG NS="pythonicai/products/docsplit/snr"
ARG PYTHON_SITE_PKGS="/usr/local/lib/python3.8/site-packages"

ENV AUTOLAN_META="/opt/autolan/metadata"
RUN mkdir -p $AUTOLAN_META
COPY dist/autolan*.tar.gz $AUTOLAN_META/
COPY requirements.txt $AUTOLAN_META/requirements.txt

RUN apt-get update && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --index-url "$PIP_INDEX_URL" -r $AUTOLAN_META/requirements.txt --no-cache-dir \
    && pip install $AUTOLAN_META/autolan*.tar.gz --no-cache-dir 

ENTRYPOINT ["autolan"]
