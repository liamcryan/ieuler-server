FROM python:3.7

COPY . /usr/local/ieuler/

RUN useradd -ms /bin/bash -d /usr/local/ieuler ieuler \
    && chown -R ieuler: /usr/local/ieuler \
    && pip3 install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt

USER ieuler
WORKDIR /usr/local/ieuler
