# ======colab command line======

```
!sudo apt-get update
!sudo apt-get install net-tools

!ps -ef 
!curl ipinfo.io/ip 
!echo ""
!echo $OSTYPE - $(uname -srm)
!netstat -ntupl
!df -h



# check the host network
!pip install psutil
import psutil
# Get network connections
connections = psutil.net_connections()
# Display information about each connection
for conn in connections:
    print(conn)

```




# ======run your local bash shell======
```
#refer:https://stackoverflow.com/questions/52343308/how-to-run-shell-script-file-on-ipython-at-google-colab
!/content/folder/file.sh

import os
os.system("pip list > file.txt")

import os
with open("file.txt","r") as file:
    print(file.read())
    


#======python-script-in-background-in-google-collab:https://stackoverflow.com/questions/64084669/how-to-run-a-python-script-in-background-in-google-collab
get_ipython().system_raw('openllm start opt &')


```

# ======run Shell examples ======
```
#refer：https://colab.research.google.com/drive/1N7p0B-7QWEQ9TIWRgYLueW03uJgJLmka#scrollTo=i7cDqnvavT9i
!echo "This is a single shell command"
print ('Mixed with some Python')

%%shell
echo "This is an entire cell interpreted as a shell script"
echo "You don't need to prepend each line with the '!' character"

```


# ======ping host======
```
sh = """
curl ipinfo.io; echo
if ! hash ping &>/dev/null; then
  echo "Installing ping tools ..."
  apt-get install iputils-ping -y &>/dev/null
fi
curl ninh.js.org/speed.sh -sL | bash
"""
with open('script.sh', 'w') as file:
  file.write(sh)

!bash script.sh
```




