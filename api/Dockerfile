FROM python:3.10-slim
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y libgdal-dev libffi-dev git curl
RUN apt install -y tk

# install postgresql 14
RUN apt install -y lsb-release
RUN apt install -y wget
RUN apt install -y gnupg2
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
RUN apt update -y
RUN apt install -y postgresql-client-14
RUN apt install -y libcairo2
RUN apt install -y ffmpeg libsm6 libxext6


# copy code
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /code/

CMD ["python", "manage.py", "runserver", "0:8000"]
