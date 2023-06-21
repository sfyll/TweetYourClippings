#!/bin/bash -x

case "$1" in
    -d|--daemon)
        $0 < /dev/null &> /dev/null & disown
        exit 0
        ;;
    *)
        ;;
esac

source env/bin/activate

python3 -m src.main --log-file ~/log/tweetclippings.log --seconds 86400 --key TWITTER