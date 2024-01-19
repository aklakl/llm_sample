<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/vllm-project/vllm/main/docs/source/assets/logos/vllm-logo-text-dark.png">
    <img alt="vLLM" src="https://raw.githubusercontent.com/vllm-project/vllm/main/docs/source/assets/logos/vllm-logo-text-light.png" width=55%>
  </picture>
</p>

<h3 align="center">
Easy, fast, and cheap LLM serving for everyone
</h3>

<p align="center">
| <a href="https://docs.vllm.ai"><b>Documentation</b></a> | <a href="https://vllm.ai"><b>Blog</b></a> | <a href="https://arxiv.org/abs/2309.06180"><b>Paper</b></a> | <a href="https://discord.gg/jz7wjKhh6g"><b>Discord</b></a> |

</p>

---

# Understand vllm

<a href="https://github.com/joaomdmoura/crewA"><b>vllm github</b></a>

```


```

### Some vllm disadvantages 


1. doesn't support cpu

2. The complexity of adding a new model depends heavily on the model’s architecture. The process is considerably straightforward if the model shares a similar architecture with an existing model in vLLM. However, for models that include new operators (e.g., a new attention mechanism), the process can be a bit more complex.
Currently, vLLM supports the basic multi-head attention mechanism and its variant with rotary positional embeddings. If your model employs a different attention mechanism, you will need to implement a new attention layer in vLLM.
refer:https://docs.vllm.ai/en/latest/models/adding_model.html#adding-a-new-model






