#!/bin/bash
echo 'STARTING UPDATE'
echo $(printenv)

REMOTE=$1
REF=$2

echo 'The update process will begin momentarily.'
echo 'This update may take more than 15 minutes.'
echo 'Please be patient and DO NOT REMOVE POWER FROM THE ROV!'

sleep 10

echo 'adding lock'
touch $HOME/.updating


if [ -z "$4" ]; then
    echo 'skipping backup...'
else
    echo 'removing old backup'
    rm -rf $HOME/.companion

    echo 'backup current repo'
    cp -r $HOME/companion $HOME/.companion
fi

cd $HOME/companion

echo 'stashing local changes'
git -c user.name="companion-update" -c user.email="companion-update" stash

echo 'tagging revert-point as' $(git rev-parse HEAD)
git tag revert-point -f

echo 'Check for local changes to save.'
git stash

if [ -z "$3" ]; then
    echo 'using branch reference'
    git fetch $REMOTE
    echo 'moving to' $(git rev-parse $REMOTE/$REF)
    git reset --hard $REMOTE/$REF
else
    echo 'using tag reference'
    TAG=$3
    echo 'fetching'
    git fetch $REMOTE --tags

    echo 'moving to' $(git rev-parse $TAG)
    git reset --hard $TAG
fi

echo 'running post-update'
$HOME/companion/scripts/post-update.sh
