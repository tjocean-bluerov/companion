#!/bin/bash
cd $HOME/companion

echo 'validating archive'
if unzip -l $1 | grep -q companion/.git; then
    echo 'archive validated ok'
else
    echo 'Archive does not look like a companion update!'
    exit 1
fi

echo 'adding lock'
touch $HOME/.updating

echo 'removing old backup'
rm -rf $HOME/.companion

echo 'backing up repository'
mv $HOME/companion $HOME/.companion

echo 'extracting archive: ' $1
unzip -q $1 -d $HOME

echo 'running post-sideload.sh'
$HOME/companion/scripts/post-sideload.sh
