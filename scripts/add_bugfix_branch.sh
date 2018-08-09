#!/bin/bash
set -e

if [ -z "$1" ] ; then
    echo "Usage: $0 bugfix_name"
	exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

git pull origin development
git checkout -b "bugfix-$1" development
git push -u origin HEAD
echo "$1" > BUGFIX
git add BUGFIX
git commit -m "Create bugfix branch for bugfix $1"
git push
