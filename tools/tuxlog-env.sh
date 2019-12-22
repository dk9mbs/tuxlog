#!/bin/bash

ENV=$1
export TUXLOG_ENVIRONMENT="$ENV"
export PS1="[tuxlog:$ENV] \[\e]0;\u@\h: \w\a\]${debian_chroot:+($debian_chroot)}\u@\h:\w>"
#echo "$ENV environment for tuxlog activated"
