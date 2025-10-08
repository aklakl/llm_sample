# Computer Use Preview


## Quick Start

This section will guide Ming through setting up and running the Computer Use Preview model. Follow these steps to get started. Ming fork from https://github.com/google/computer-use-preview on 20251008

* For Ming's CLI

```bash

conda activate google-computer

```



### 1. Installation & Configuration

**Clone the Repository & Set up Python Virtual Environment and Install Dependencies**

```bash
git clone https://github.com/aklakl/llm_sample
cd llm_sample\computer-use-preview

conda create --name google-computer python=3.11
conda activate google-computer
#conda deactivate
pip install -r requirements.txt

# Install system dependencies required by Playwright for Chrome
playwright install-deps chrome

# Install the Chrome browser for Playwright
playwright install chrome

 
# A. If using the Gemini Developer API:
#You need a Gemini API key to use the agent:

export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"



```



**Local Playwright**

Runs the agent using a Chrome browser instance controlled locally by Playwright.


```bash
python main.py --query="Please help me finish the sign up the student workflow use this url=>https://www.widdyup.com/v2/home/sign_up, with fake user(The student email logic like anonymous.2025XXXXXX@tafmail.com, 2025XXXXXX is the current time only with digitial number from EAST timezone.), if you face any 'reCAPTCHA challenge' please help me go head verify the reCAPTCHA challenge.And help me skip the 'Safety service'  and also accept all consent and agreement dialogs." --env="playwright"  --skip_safety_confirmation
```


```bash
python main.py --query="Go to Google and type 'Hello World' into the search bar" --env="playwright"
```


You can also specify an initial URL for the Playwright environment:
```bash
python main.py --query="Go to Google and type 'Hello World' into the search bar" --env="playwright" --initial_url="https://www.google.com/search?q=latest+AI+news"
```






### 项目总体概览
这个项目是一个AI浏览器代理。它的核心功能是：接收用户的自然语言指令（例如“去谷歌搜索最新的AI新闻”），然后利用大型语言模型（LLM，这里是Google Gemini）来理解这个指令，并将其分解成一系列可以在浏览器中执行的具体操作（如点击、输入、滚动等），最终自动完成用户指定的任务。

该项目在架构上分为三个主要部分：

入口和环境配置 (main.py)
代理核心逻辑 (agent.py)
计算机/浏览器操作接口 (computers/computer.py)
技术依赖 (requirements.txt)
项目主要依赖以下几个关键库：

google-genai: Google Gemini 的官方 Python SDK，用于与语言模型进行交互。
playwright: 一个强大的浏览器自动化工具，用于在本地实际执行点击、输入等操作并截图。
browserbase: 一个云端浏览器服务，可以作为 playwright 的替代方案。
rich / termcolor: 用于在命令行中输出美观、带颜色的文本，提升用户体验。
pydantic: 用于数据结构定义和验证，确保模块间数据传输的规范性。
核心文件分析
1. main.py - 项目入口
这个文件是整个程序的起点。它的作用是：

解析命令行参数：通过 argparse 库，它接收用户输入的 --query（要执行的任务）、--env（选择使用 playwright 还是 browserbase）等参数。
创建“计算机”实例：根据用户的选择，它会初始化一个 PlaywrightComputer 或 BrowserbaseComputer 的实例。这个实例代表了AI可以操作的浏览器环境。
创建代理实例：它将上一步创建的“计算机”实例和用户的指令 query 一起传递给 BrowserAgent。
启动代理：调用 agent.agent_loop() 方法，开始执行任务。
2. computers/computer.py - 行为抽象接口
这个文件定义了一个名为 Computer 的抽象基类 (ABC)。这是一个非常好的设计，它起到了“接口”的作用，规定了一个“可操作的计算机”应该具备哪些能力。

定义标准操作：它定义了所有浏览器环境都必须实现的方法，例如 click_at, type_text_at, scroll_document, navigate 等。
统一返回类型：它规定了所有操作都必须返回一个 EnvState 对象，该对象包含操作后的屏幕截图 (screenshot) 和当前页面的URL (url)。这为AI模型提供了决策所需的上下文。
解耦：通过这个接口，agent.py 中的核心逻辑不需要关心底层是用 Playwright 还是 Browserbase 实现的，只需要调用这个接口定义的方法即可。
3. agent.py - 代理的大脑
这是整个项目最核心的部分，是AI代理的“大脑”。它的工作流程是一个循环（agent_loop），在每次循环中（run_one_iteration）：

准备上下文：将用户的原始指令、之前的操作历史、以及最新的屏幕截图等信息打包，准备发送给Gemini模型。为了节省Token，它只会保留最近几次操作的截图。

调用模型 (Tool-use/Function Calling)：它向Gemini模型发送请求。这里的关键是，它不仅是让模型生成文本，而是利用了模型的**Tool-use（工具使用）**能力。它告诉模型，你可以调用一系列预定义的函数（如 click_at, type_text_at 等）。

获取模型决策：Gemini模型会返回它的“思考过程”（一段文本）以及一个或多个函数调用 (Function Call)。例如，模型可能会决定调用 type_text_at(x: 500, y: 300, text: 'Hello World')。

执行决策：agent.py 中的 handle_action 方法会解析模型返回的函数调用，并执行对应的 computer 实例的方法（例如 self._browser_computer.type_text_at(...)）。

反馈与循环：computer 执行操作后，会返回一个新的 EnvState（包含新的截图和URL）。agent.py 将这个结果再次打包到上下文中，然后开始下一次循环，直到模型认为任务已经完成（不再返回函数调用）为止。

总结
这个项目是多模态AI代理的一个经典实现。它的工作流可以概括为 “观察 -> 思考 -> 行动” 的循环：

观察 (Observe)：通过 computer 模块获取浏览器截图和URL。
思考 (Think)：agent 模块将观察到的信息和任务目标发送给Gemini模型，模型决策出下一步要调用的工具（函数）。
行动 (Act)：agent 模块解析模型的决策，并调用 computer 模块执行具体操作，然后回到“观察”步骤。
这个架构清晰、可扩展性强，通过 computer.py 的抽象接口，可以方便地接入更多不同类型的“计算机”环境。

如果您想了解某个特定文件或功能的更多细节，请随时告诉我。