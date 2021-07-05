#!/bin/bash

PORT="${PORT:=1194}"
HOST="${HOST:=CHANGEME}" # ex: vpn.changeme.com
SUBNET="${SUBNET:=192.168.255.0}"
SUBNET_MASK="${SUBNET_MASK:=255.255.255.0}"

echo "docker-compose run openvpn ovpn_genconfig -u udp://$HOST:$PORT  -N -b -p \"route 10.10.10.0 255.255.255.0\" -p \"route $SUBNET $SUBNET_MASK\" -n \"8.8.8.8\""
docker-compose run openvpn ovpn_genconfig -u udp://$HOST:$PORT -N -b -p "route 10.10.10.0 255.255.255.0" -p "route $SUBNET $SUBNET_MASK" -n "8.8.8.8"

echo "docker-compose run openvpn ovpn_initpki"
docker-compose run openvpn ovpn_initpki

if [ ! -z $? ]; then
  echo "> You might have had an error in the like of:
  unable to load Private Key
  140315878260040:error:06065064:digital envelope routines:EVP_DecryptFinal_ex:bad decrypt:crypto/evp/evp_enc.c:583:
  140315878260040:error:0906A065:PEM routines:PEM_do_header:bad decrypt:crypto/pem/pem_lib.c:461:"
  echo "> In such case, make sure your input and the \$CA_PASS environment variable in the docker-compose.yml file matches. Current: \$CA_PASS='$CA_PASS'"
fi
