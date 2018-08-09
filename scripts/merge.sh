#!/bin/bash
set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "${DIR}/.."

git pull origin development

if [ -f FEATURE ]; then
    feature_name=$(<FEATURE)
    git rm FEATURE
    git commit -m "Prepare feature ${feature_name} to be merged into development"
    git push

    git checkout development
    git merge --no-ff "feature-${feature_name}"
    git push origin development

    git push origin --delete "feature-${feature_name}"
    git branch -d "feature-${feature_name}"
elif [ -f BUGFIX ]; then
    bugfix_name=$(<BUGFIX)
    git rm BUGFIX
    git commit -m "Prepare bugfix ${bugfix_name} to be merged into development"
    git push

    git checkout development
    git merge --no-ff "bugfix-${bugfix_name}"
    git push origin development

    git push origin --delete "bugfix-${bugfix_name}"
    git branch -d "bugfix-${bugfix_name}"
elif [ -f VERSION]; then
    version=$(<VERSION)
    git rm VERSION
    git commit -m "Prepare release ${version} to be merged into master and development"
    git push

    git pull origin master
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
    hotfix=$(<HOTFIX)
    git rm HOTFIX
    git commit -m "Prepare hotfix ${hotfix} to be merged into master and development"
    git push

    git pull origin master
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
    echo "Check your branch. This script will work on feature, bugfix, release and hotfix branches only"
fi