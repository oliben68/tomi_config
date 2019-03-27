#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

../base_config.sh ${DIR}/configurate.py

#ROOT=tomi
#COMPONENT=config
#PROJECT=${ROOT}_${COMPONENT}
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
#
#rm -rf ${DIR}/build
#
#source activate "vanilla"
#${DIR}/configurate.sh
#echo "---------------------------------------------------------------------------------------------------------------------------------------"
#
#source activate "vanilla"
#${DIR}/configurate.sh
#echo "---------------------------------------------------------------------------------------------------------------------------------------"