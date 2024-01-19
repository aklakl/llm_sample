#refer:https://github.com/ngrok/ngrok-api-python

import ngrok

# Construct the API client
client = ngrok.Client("your_auth_oken")

def run_test_ngrok():
    # List all online tunnels
    for t in client.tunnels.list():
        print(t)

    # Create an IP policy that allows traffic from some subnets
    policy = client.ip_policies.create()
    for cidr in ["24.0.0.0/8", "12.0.0.0/8"]:
        client.ip_policy_rules.create(cidr=cidr, ip_policy_id=policy.id, action="allow")
    print("policy=>",policy)


def run_ngrok_server():
    # List all online tunnels
    for t in client.tunnels.list():
        print(t)

    # Create an IP policy that allows traffic from some subnets
    policy = client.ip_policies.create()
    for cidr in ["24.0.0.0/8", "12.0.0.0/8"]:
        client.ip_policy_rules.create(cidr=cidr, ip_policy_id=policy.id, action="allow")
    print("policy=>",policy)


#running main method
if __name__ == "__main__":
    #run_test_ngrok()
    run_ngrok_server()