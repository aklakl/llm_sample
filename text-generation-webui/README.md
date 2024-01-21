# Sample to use text-generation-webui with docker 

Ming's Colab text-generation-webui => https://colab.research.google.com/drive/1-pUeLBWvsh0M82OhaXivZigVhtJKhPm_
Text-generation-webui Offical github=>https://github.com/oobabooga/text-generation-webui
Atinoda github=>https://github.com/Atinoda/text-generation-webui-docker


## run text-generation-webui on ming's docker images(within tiny-vicuna-1b.q4_k_m.gguf model)

1.  CLIs=>
```
#User root's password is root, user app's password is app;
git pull mingli512/ming-text-generation-webui:latest
docker run -itd -p 7860:7860 --entrypoint /bin/bash --name textgen mingli512/ming-text-generation-webui:latest
docker exec --user app --workdir /home/app/text-generation-webui -it textgen /bin/bash 
conda activate textgen
python3 server.py --model tiny-vicuna-1b.q4_k_m.gguf --api --public-api


#conda activate textgen step could be fix by refer:https://stackoverflow.com/questions/54429210/how-do-i-prevent-conda-from-activating-the-base-environment-by-default
#conda config --set auto_activate_base true  


```



### Testing CLI
```

http://192.168.0.232:7861
#refer: https://everything.curl.dev/usingcurl/telnet
curl telnet://192.168.0.232:7860
curl telnet://127.0.0.1:7861
curl telnet://127.0.0.1:11434
wget https://huggingface.co/afrideva/Tiny-Vicuna-1B-GGUF/resolve/main/tiny-vicuna-1b.q4_k_m.gguf

```

## Others



###  CLI Installation order of text-generation-webui with python docker image, instuction refer:https://github.com/oobabooga/text-generation-webui?tab=readme-ov-file#manual-installation-using-conda

```
docker run -it --user root --entrypoint /bin/bash 21bcd961157e
adduser app
usermod -aG sudo app
apt-get update && apt-get install sudo net-tools
#Here need to figure out your local $arch
curl -sL "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh" > "Miniconda3.sh"
bash Miniconda3.sh
export PATH="/home/app/miniconda3/bin:$PATH"
#refer:https://stackoverflow.com/questions/55507519/python-activate-conda-env-through-shell-script
source ~/miniconda3/etc/profile.d/conda.sh
conda create -n textgen python=3.11
conda activate textgen
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
cat /proc/cpuinfo | grep avx2
pip install -r requirements_cpu_only_noavx2.txt
cd models && wget https://huggingface.co/afrideva/Tiny-Vicuna-1B-GGUF/resolve/main/tiny-vicuna-1b.q4_k_m.gguf

#python server.py
python3 server.py --model tiny-vicuna-1b.q4_k_m.gguf --api --public-api

#Got some exception refer:  https://github.com/abetlen/llama-cpp-python#installation-from-pypi => https://github.com/oobabooga/text-generation-webui/discussions/4098 
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
pip install -r extensions/openai/requirements.txt --upgrade

#relogin the docker expose the port
docker start 4ac646a2f4bd
docker exec -it e815cca33f0d /bin/bash
docker run -itd -p 7861:7860 --entrypoint /bin/bash --name textgen mingli512/ming-text-generation-webui
```








### Installation history of exception

```
Fianlly fixed, please refer:  https://github.com/abetlen/llama-cpp-python#installation-from-pypi => https://github.com/oobabooga/text-generation-webui/discussions/4098 
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
pip install -r extensions/openai/requirements.txt --upgrade

======Got Error=> 
(textgen) app@e815cca33f0d:~/text-generation-webui$ python3 server.py --model tiny-vicuna-1b.q4_k_m.gguf --api --public-api
16:42:31-209141 INFO     Starting Text generation web UI
16:42:31-240428 INFO     Loading tiny-vicuna-1b.q4_k_m.gguf
16:42:31-268654 INFO     llama.cpp weights detected: models/tiny-vicuna-1b.q4_k_m.gguf
╭────────────────────────────────────────────────────────────────────── Traceback (most recent call last) ───────────────────────────────────────────────────────────────────────╮
│ /home/app/text-generation-webui/server.py:241 in <module>                                                                                                                      │
│                                                                                                                                                                                │
│   240         # Load the model                                                                                                                                                 │
│ ❱ 241         shared.model, shared.tokenizer = load_model(model_name)                                                                                                          │
│   242         if shared.args.lora:                                                                                                                                             │
│                                                                                                                                                                                │
│ /home/app/text-generation-webui/modules/models.py:87 in load_model                                                                                                             │
│                                                                                                                                                                                │
│    86     shared.args.loader = loader                                                                                                                                          │
│ ❱  87     output = load_func_map[loader](model_name)                                                                                                                           │
│    88     if type(output) is tuple:                                                                                                                                            │
│                                                                                                                                                                                │
│ /home/app/text-generation-webui/modules/models.py:250 in llamacpp_loader                                                                                                       │
│                                                                                                                                                                                │
│   249     logger.info(f"llama.cpp weights detected: {model_file}")                                                                                                             │
│ ❱ 250     model, tokenizer = LlamaCppModel.from_pretrained(model_file)                                                                                                         │
│   251     return model, tokenizer                                                                                                                                              │
│                                                                                                                                                                                │
│ /home/app/text-generation-webui/modules/llamacpp_model.py:63 in from_pretrained                                                                                                │
│                                                                                                                                                                                │
│    62                                                                                                                                                                          │
│ ❱  63         Llama = llama_cpp_lib().Llama                                                                                                                                    │
│    64         LlamaCache = llama_cpp_lib().LlamaCache  






======Got Error=> 
$ python3 server.py --share --model tiny-vicuna-1b.q4_k_m.gguf --n-gpu-layers 128 --load-in-4bit --use_double_quant --api --public-api
<jemalloc>: MADV_DONTNEED does not work (memset will be used instead)
<jemalloc>: (This is the expected behaviour if you are running under QEMU)
15:07:33-695228 INFO     Starting Text generation web UI
15:07:33-719131 WARNING  The gradio "share link" feature uses a proprietary executable to create a reverse tunnel. Use it with care.
15:07:33-723875 WARNING
                         You are potentially exposing the web UI to the entire internet without any access password.
                         You can create one with the "--gradio-auth" flag like this:

                         --gradio-auth username:password

                         Make sure to replace username:password with your own.
15:07:34-043495 INFO     Loading tiny-vicuna-1b.q4_k_m.gguf
qemu: uncaught target signal 4 (Illegal instruction) - core dumped
Illegal instruction
$ python3 server.py --model tiny-vicuna-1b.q4_k_m.gguf --n-gpu-layers 128 --load-in-4bit --use_double_quant --api --public-api

<jemalloc>: MADV_DONTNEED does not work (memset will be used instead)
<jemalloc>: (This is the expected behaviour if you are running under QEMU)
15:08:08-401976 INFO     Starting Text generation web UI
15:08:08-722182 INFO     Loading tiny-vicuna-1b.q4_k_m.gguf
qemu: uncaught target signal 4 (Illegal instruction) - core dumped
Illegal instruction



======Got Error=> 
Traceback (most recent call last):
  File "/home/app/text-generation-webui/server.py", line 4, in <module>
    from modules import shared
  File "/home/app/text-generation-webui/modules/shared.py", line 8, in <module>
    import yaml
ModuleNotFoundError: No module named 'yaml'





======Got Error=>
"WARNING: The requested image's platform (linux/amd64) does not match the detected host platform (linux/arm64/v8) and no specific platform was requested"


======Got Error=>
Maybe try Manual installation using Conda refer:https://github.com/oobabooga/text-generation-webui?tab=readme-ov-file#manual-installation-using-conda

```



### Previous docker installation of images as atinoda/text-generation-webui and  arbidev/textgen-webui(PS:all the images can't to run text-generation-webui)

```
#AMD64-
docker run -d -p 7860:7860 --name textgen_atinoda atinoda/text-generation-webui
docker run -d -p 7861:7860 --name textgen_arbidev arbidev/textgen-webui


docker start textgen_atinoda && docker exec -it textgen_atinoda /bin/bash
source /venv/bin/activate
python3 server.py --share --model tiny-vicuna-1b.q4_k_m.gguf --n-gpu-layers 128 --load-in-4bit --use_double_quant --api --public-api
python3 server.py --model tiny-vicuna-1b.q4_k_m.gguf --n-gpu-layers 128 --load-in-4bit --use_double_quant --api --public-api

docker start textgen_arbidev && docker exec -it textgen_arbidev /bin/bash
docker run -it --user root --entrypoint /bin/bash $your_images_id
apt update 
apt install curl net-tools


docker push mingli512/arbidev_text-generation-webui:default


```