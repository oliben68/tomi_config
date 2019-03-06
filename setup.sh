#!/usr/bin/env bash

ROOT=tomi
COMPONENT=config
PROJECT=${ROOT}_${COMPONENT}
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

rm -rf /Users/oliviersteck/Documents/sources/python/${ROOT}/${PROJECT}/build

source activate "vanilla"
${DIR}/configurate.sh
echo "---------------------------------------------------------------------------------------------------------------------------------------"

source activate "vanilla"
${DIR}/configurate.sh
echo "---------------------------------------------------------------------------------------------------------------------------------------"