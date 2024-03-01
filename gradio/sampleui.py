# flake8: noqa: E402
import os
import logging
#import re_matching
#from tools.sentence import split_by_language

logging.getLogger("numba").setLevel(logging.WARNING)
logging.getLogger("markdown_it").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("matplotlib").setLevel(logging.WARNING)

logging.basicConfig(
    level=logging.INFO, format="| %(name)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

#import torch
#import utils
#from infer import infer, latest_version, get_net_g, infer_multilang
import gradio as gr
import webbrowser
import numpy as np
#from config import config
#import librosa

net_g = None

# device = config.webui_config.device
# if device == "mps":
#     os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"


def greet(name):
    return "Hello " + name + "!"

demo = gr.Interface(fn=greet, inputs="textbox", outputs="textbox")
    
if __name__ == "__main__":
    print("推理页面已开启!")
    webbrowser.open(f"http://127.0.0.1:8888")
    demo.launch(share=True, server_port=9999)








