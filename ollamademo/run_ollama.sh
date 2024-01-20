#!/bin/bash
nohup ollama serve >>ollamaServices.log &

#Docs=>https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/
#Downlaod => https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
cloudflared tunnel --url localhost:11434/