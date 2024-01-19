# The code with ChatDev
```
ChatDev github refer:https://github.com/OpenBMB/ChatDev

```

### Running Locally

To get started, follow these steps:

1. **Clone the GitHub Repository:** Begin by cloning the repository using the command:

   ```
   git clone https://github.com/OpenBMB/ChatDev.git
   ```

2. **Set Up Python Environment:** Ensure you have a version 3.9 or higher Python environment. You can create and
   activate this environment using the following commands, replacing `ChatDev_conda_env` with your preferred environment
   name:

   ```
   #install the conda refer:https://docs.conda.io/projects/miniconda/en/latest/
   mkdir -p ~/miniconda3
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
   bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
   rm -rf ~/miniconda3/miniconda.sh

   ~/miniconda3/bin/conda init bash
   ~/miniconda3/bin/conda init zsh

   export PATH=~/miniconda3/bin:$PATH
   echo $PATH
   
   conda create -n ChatDev_conda_env python=3.9 -y

   #face issue with "CondaError: Run 'conda init' before 'conda activate'"  fixed by this => https://stackoverflow.com/questions/55507519/python-activate-conda-env-through-shell-script
   source ~/miniconda3/etc/profile.d/conda.sh
   conda activate ChatDev_conda_env

   ```

3. **Install Dependencies:** Move into the `ChatDev` directory and install the necessary dependencies by running:

   ```
   cd ChatDev
   pip3 install -r requirements.txt
   ```

4. **Set up your custom OpenAI service** Go to Google colab Start the ngrok mapping litellm server first refer => https://colab.research.google.com/drive/1GKlfU7Fjq30oQPirHvCcQy_e_B8vNEDs?usp=sharing    
Or use LM Studio build your local LLM => https://lmstudio.ai/

5. **Switch to your custom OpenAI API Key:** Export your OpenAI API key as an environment variable. Replace `"your_OpenAI_API_key"` with
   your actual API key. Remember that this environment variable is session-specific, so you need to set it again if you
   open a new terminal session.
   On Unix/Linux:

   ```

   #Sometimes if OPENAI_API_BASE not work , please set up to BASE_URL try once. refer:https://github.com/OpenBMB/ChatDev/issues/312
   export OPENAI_API_KEY="sk-llllllllllllllllllllll"
   export BASE_URL="http://192.168.137.176:1234/v1"
   #export BASE_URL=http://airedale-native-chicken.ngrok-free.app/v1


   ```

   On Windows:

   ```
   $env:OPENAI_API_KEY="your_OpenAI_API_key"
   $env:OPENAI_API_BASE="your_OPENAI_API_BASE"

   ```

6. **Build Your Software:** Use the following command to initiate the building of your software,
   replacing `[description_of_your_idea]` with your idea's description and `[project_name]` with your desired project
   name:
   On Unix/Linux:

   ```
   #python3 run.py --task "[description_of_your_idea]" --name "[project_name]"
   BASE_URL="http://192.168.137.176:1234/v1" OPENAI_API_KEY="sk-llllllllllllllllllllll" python3 run.py --task "web shopping system(It include User Authentication and Authorization/User registration and login functionality/Product Management/Shopping Cart/Order Processing/Search and Navigation/ include the Design document)" --name "web_shopping_sys"

   ```

   On Windows:

   ```
   python run.py --task "[description_of_your_idea]" --name "[project_name]"

   ```

7. **Run Your Software:** Once generated, you can find your software in the `WareHouse` directory under a specific
   project folder, such as `project_name_DefaultOrganization_timestamp`. Run your software using the following command
   within that directory:
   On Unix/Linux:

   ```
   cd WareHouse/project_name_DefaultOrganization_timestamp
   python3 main.py
   ```

   On Windows:

   ```
   cd WareHouse/project_name_DefaultOrganization_timestamp
   python main.py
   ```


### Running with Docker 

To get started, follow these steps:

1. **Clone the GitHub Repository:** Begin by cloning the repository using the command:

   ```
   git clone https://github.com/OpenBMB/ChatDev.git


   docker build .


   #Retag you just commited the images_id to a real name(Optional)
   docker tag bfb31d0e3f04 mingli512/ming_chatdev:latest


   #Push your docker image to docker hub ($docker_hub_account_name/$project_name:$tagname)=> docker push [OPTIONS] NAME[:TAG]  please refer:https://docs.docker.com/engine/reference/commandline/push/
   docker push mingli512/ming_chatdev:latest


   #How to Create a Docker Image From a Container refer:https://www.dataset.com/blog/create-docker-image/
   #First convert your container to the docker images use => docker commit $YOUR_container_name
   docker commit ming_chatdev


   #chatdev default port is 8000(netstat -an | grep 8000), and run the container with ming_chatdev 
   docker run -d -it -p 8000:8000 --name ming_chatdev mingli512/ming_chatdev:latest 


   #Login the docker container
   docker exec -it 28e6c48fcf5e /usr/bin/bash


   #(Optional)after login the docker container make sure you have some tools
   apt update && apt install -y net-tools procps curl telnet vim && rm -rf /var/lib/apt/lists/*


   #Could be use your local LLM
   export OPENAI_API_KEY="your_OpenAI_API_key"
   export BASE_URL=http://airedale-native-chicken.ngrok-free.app/v1


   #Build Your Software: Use the following command to initiate the building of your software, replacing [description_of_your_idea] with your idea's description and [project_name] with your desired project name: On Unix/Linux:
   #python3 run.py --task "[description_of_your_idea]" --name "[project_name]"
   #python3 run.py --task "design a 2048 game" --name "2048"  --org "THUNLP" --config "Default"
   python3 run.py --task "web shopping system(It include User Authentication and Authorization/User registration and login functionality/Product Management/Shopping Cart/Order Processing/Search and Navigation/ include the Design document)" --name "web_shopping_sys"

   #Run Your Software: Once generated, you can find your software in the WareHouse directory under a specific project folder, such as project_name_DefaultOrganization_timestamp. Run your software using the following command within that directory: On Unix/Linux:
   cd WareHouse/project_name_DefaultOrganization_timestamp
   python3 main.py


   #(Optional ) you can start a flask app to get a Visualizer, which is local web demo for visualizing real-time logs, replayed logs, and ChatChain.the difference between real-time logs and replayed logs lies in that the former is mainly for debugging, which can print the agent's dialogue information, environment changes and many additional system information in real time during the process of software generation, such as file changes and git information. The latter is used to replay the generated log and only prints the dialogue information of the agent.just run it.refer:https://github.com/OpenBMB/ChatDev/blob/main/wiki.md
   python3 visualizer/app.py







   ```

### Running based on Gemini API 

To get started, follow these steps:

1. **Clone the GitHub Repository:** 

   ```
   reflect  => https://github.com/OpenBMB/ChatDev/issues/313


   ```

