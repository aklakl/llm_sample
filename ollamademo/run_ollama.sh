#!/bin/bash
nohup ollama serve >>ollamaServices.log &

#Docs=>https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/
#Downlaod => https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
#Please note that Quick Tunnels are meant to be ephemeral and should only be used for testing purposes. For production usage, we recommend creating Named Tunnels. (https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/)
#Expose my ollama service for outside temporary using cloudflared
cloudflared tunnel --url localhost:11434/

#Start ngrok for ssh
ngrok tcp 22 > /dev/null &