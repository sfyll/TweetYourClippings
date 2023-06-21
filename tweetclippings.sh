#!/bin/bash

source env/bin/activate

python3 -m src.main --log-file ~/log/tweetclippings.log --seconds 86400 --key TWITTER