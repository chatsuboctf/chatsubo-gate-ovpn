.PHONY: build

all: gunicorn

gunicorn:
	./venv/bin/gunicorn app:server -w 1 --log-file - --bind 0.0.0.0:7474

flask:
	./venv/bin/flask run

venv:
	virtualenv venv --python=`which python3.8`

install_pip:
	./venv/bin/pip install -r ./requirements.txt

#docker: docker_build docker_start
#
#docker_build:
#	docker build -t chatsubo-vpn .
#
#docker_start:
#	docker run -d -p 127.0.0.1:5000:5000/tcp chatsubo-vpn

req:
	./venv/bin/pip freeze | grep -v "pkg-resources" > requirements.txt

up:
	docker-compose up --build -d

down:
	docker-compose down

kill:
	docker-compose kill
