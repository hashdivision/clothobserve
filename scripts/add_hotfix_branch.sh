#!/bin/bash
set -e

if [ -z "$1" ] ; then
    echo "Usage: $0 version_and_hotfix_name"
	exit 1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

git fetch origin
git checkout -b "hotfix-$1" master
git push -u origin HEAD
echo "$1" > HOTFIX
git add HOTFIX
git commit -m "Creates hotfix branch $1"
git push