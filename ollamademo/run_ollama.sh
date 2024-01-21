#!/bin/bash
nohup ollama serve >>ollamaServices.log &

#Docs=>https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/do-more-with-tunnels/trycloudflare/
#Downlaod => https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
#Please note that Quick Tunnels are meant to be ephemeral and should only be used for testing purposes. For production usage, we recommend creating Named Tunnels. (https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/)
#Expose my ollama service for outside temporary using cloudflared
cloudflared tunnel --url localhost:11434/ >cloudflared.log &

#Start ngrok for ssh
#Generate an SSH Key Pair on UNIX and UNIX-Like Systems=>https://docs.oracle.com/en/cloud/cloud-at-customer/occ-get-started/generate-ssh-key-pair.html#GUID-8B9E7FCB-CEA3-4FB3-BF1A-FD3406A2432F
#https://ngrok.com/docs/api/resources/ssh-credentials/
#https://ngrok.com/docs/agent/ssh-reverse-tunnel-agent/
ngrok tcp 22 > /dev/null &