# Build python virtualenv
FROM python:3.9.1-alpine3.12 as python-build
RUN apk add --no-cache \
 	build-base bash git ca-certificates

RUN pip3 install --upgrade pip setuptools

RUN mkdir /opt/chatsubo-gate
COPY requirements.txt /opt/chatsubo-gate
WORKDIR /opt/chatsubo-gate

RUN pip3 install virtualenv
RUN virtualenv venv --python=$(which python3)
RUN	./venv/bin/pip install -r ./requirements.txt

FROM python:3.9.1-alpine3.12
ENV USER=chatsubo-gate
ENV UID=1324
ENV GID=1324
ENV CHATSUBO_GATE_PORT=7474

COPY --from=python-build /opt/chatsubo-gate/venv /opt/chatsubo-gate/venv
RUN addgroup -g "$GID" chatsubo-gate
RUN adduser \
	--disabled-password \
	--gecos "" \
	--ingroup "$USER" \
	--no-create-home \
	--uid "$UID" \
	"$USER"

ADD app /opt/chatsubo-gate/app
COPY docker-entrypoint.sh /opt/chatsubo-gate/docker-entrypoint.sh
WORKDIR /opt/chatsubo-gate
RUN chmod +x /opt/chatsubo-gate/docker-entrypoint.sh
RUN chown -R "$UID":"$GID" /opt/chatsubo-gate

#USER "$UID"
EXPOSE "$CHATSUBO_GATE_PORT"
ENTRYPOINT ["/bin/sh", "/opt/chatsubo-gate/docker-entrypoint.sh"]
