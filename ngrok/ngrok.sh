#!/bin/bash
#ngrok http --domain=dashing-slowly-kiwi.ngrok-free.app 22 >>ngork.log &
ngrok tcp 22 > /dev/null &