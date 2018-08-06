#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

git fetch origin

if [ -f FEATURE ]; then
    local feature_name=$(<FEATURE)
    git rm FEATURE
    rm FEATURE
    git commit -m "Prepares feature ${feature_name} to be merged into development"
    git push

    git checkout development
    git merge --no-ff "feature-${feature_name}"
    git push origin development

    git push origin --delete "feature-${feature_name}"
    git branch -d "feature-${feature_name}"
elif [ -f VERSION]; then
    local version=$(<VERSION)
    git rm VERSION
    rm VERSION
    git commit -m "Prepares release ${version} to be merged into master and development"
    git push

    git checkout master
    git merge --no-ff "release-${version}"
    git tag -a "${version}"
    git push origin "${version}"
    git push origin master

    git checkout development
    git merge --no-ff "release-${version}"
    git push origin development

    git push origin --delete "release-${version}"
    git branch -d "release-${version}"
elif [ -f HOTFIX]; then
    local hotfix=$(<HOTFIX)
    git rm HOTFIX
    rm HOTFIX
    git commit -m "Prepares hotfix ${hotfix} to be merged into master and development"
    git push

    git checkout master
    git merge --no-ff "hotfix-${hotfix}"
    git tag -a "${hotfix}"
    git push origin "${hotfix}"
    git push origin master

    git checkout development
    git merge --no-ff "hotfix-${hotfix}"
    git push origin development

    git push origin --delete "hotfix-${hotfix}"
    git branch -d "hotfix-${hotfix}"
else
    echo "Check your branch. This script will work on feature, release and hotfix branches only"
fi