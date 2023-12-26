* checkout from https://github.com/microsoft/autogen/tree/main/test  move the sample to main/test folder


** got error 
========

Traceback (most recent call last):
  File "/Users/ming/Documents/work/repo/autogen/test/ming.py", line 62, in <module>
    user_proxy.initiate_chat(assistant, message="Plot a chart of NVDA and TESLA stock price change YTD.")
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/autogen/agentchat/conversable_agent.py", line 550, in initiate_chat
    self.send(self.generate_init_message(**context), recipient, silent=silent)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/autogen/agentchat/conversable_agent.py", line 348, in send
    recipient.receive(message, self, request_reply, silent)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/autogen/agentchat/conversable_agent.py", line 481, in receive
    reply = self.generate_reply(messages=self.chat_messages[sender], sender=sender)
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/autogen/agentchat/conversable_agent.py", line 906, in generate_reply
    final, reply = reply_func(self, messages=messages, sender=sender, config=reply_func_tuple["config"])
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/autogen/agentchat/conversable_agent.py", line 628, in generate_oai_reply
    return True, client.extract_text_or_function_call(response)[0]
  File "/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages/autogen/oai/client.py", line 343, in extract_text_or_function_call
    return [
TypeError: 'NoneType' object is not iterable


========

