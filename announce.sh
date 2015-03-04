#!/bin/bash

DIR="$(dirname "$0")"

while test $# -gt 0; do
  case $1 in
    -i)
      shift
      ip link show dev $1 > /dev/null
      test $? -ne 0 && exit
      INTERFACE="-i $1"
      ;;
    -b)
      shift
      ip link show dev $1 > /dev/null
      test $? -ne 0 && exit
      BATADV="-b $1"
      ;;
    -u)
      shift
      alfred-json -z -r 158 -s $1 > /dev/null
      test $? -ne 0 && exit
      ALFREDSOCKET="-u $1"
      ;;
    -s)
      shift
      SITECODE="-s $1"
      ;;
    -h|--help)
      echo "Usage: $0 [-i <ifname>] [-b <batadv-dev>] [-u <alfred-socket>] [-s <site_code>]"
      exit
      ;;
  esac
  shift
done

"${DIR}"/announce.py -d "${DIR}"/nodeinfo.d/ ${INTERFACE} ${BATADV} ${SITECODE} | gzip | alfred $ALFREDSOCKET $INTERFACE -s 158
"${DIR}"/announce.py -d "${DIR}"/statistics.d/ ${INTERFACE} ${BATADV} ${SITECODE} | gzip | alfred $ALFREDSOCKET $INTERFACE -s 159
