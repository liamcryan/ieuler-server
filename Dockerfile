FROM python:3.7

COPY . /usr/local/ieuler/

COPY ./instance/config.py /usr/local/var/app-instance/

WORKDIR /usr/local/ieuler

RUN useradd -ms /bin/bash ieuler && chown -R ieuler: /usr/local/ieuler \
    && chown ieuler: /usr/local/var/app-instance

RUN pip3 install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org -r requirements.txt \
    && pip3 install gunicorn

USER ieuler
