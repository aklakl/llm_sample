from pyngrok import ngrok

# Setting an auth token allows us to open multiple
# tunnels at the same time
#ngrok.set_auth_token("your_auth_oken")
ngrok.set_auth_token("your_auth_oken")


# Open a HTTP tunnel on the default port 80
# <NgrokTunnel: "https://<public_sub>.ngrok.io" -> "http://localhost:80">
#http_tunnel = ngrok.connect()

# Open a SSH tunnel
# <NgrokTunnel: "tcp://0.tcp.ngrok.io:12345" -> "localhost:22">
ssh_tunnel = ngrok.connect("22", "tcp")
print("ssh_tunnel=>",ssh_tunnel)

# Open a tunnel to MySQL with a Reserved TCP Address
# <NgrokTunnel: "tcp://1.tcp.ngrok.io:12345" -> "localhost:3306">
#ngrok.connect("22", "tcp",remote_addr="airedale-native-chicken.ngrok-free.app:22")


# # Open a named tunnel from the config file
# named_tunnel = ngrok.connect(name="my_tunnel_name")


# The NgrokTunnel returned from methods like connect(),
# get_tunnels(), etc. contains the public URL
#ngrok.disconnect(ngrok_tunnel.public_url)

print("====completed===")