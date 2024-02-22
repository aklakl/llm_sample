#Ming made changes for autogen, refer: https://github.com/microsoft/autogen/issues/842#issuecomment-1880056796
import logging
import random
import re
import sys
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union, Tuple


from ..code_utils import content_str
from .agent import Agent
from .conversable_agent import ConversableAgent
from ..graph_utils import check_graph_validity, invert_disallowed_to_allowed


logger = logging.getLogger(__name__)


class NoEligibleSpeakerException(Exception):
    """Exception raised for early termination of a GroupChat."""

    def __init__(self, message="No eligible speakers."):
        self.message = message
        super().__init__(self.message)


@dataclass
class GroupChat:
    """(In preview) A group chat class that contains the following data fields:
    - agents: a list of participating agents.
    - messages: a list of messages in the group chat.
    - max_round: the maximum number of rounds.
    - admin_name: the name of the admin agent if there is one. Default is "Admin".
        KeyBoardInterrupt will make the admin agent take over.
    - func_call_filter: whether to enforce function call filter. Default is True.
        When set to True and when a message is a function call suggestion,
        the next speaker will be chosen from an agent which contains the corresponding function name
        in its `function_map`.
    - speaker_selection_method: the method for selecting the next speaker. Default is "auto".
        Could be any of the following (case insensitive), will raise ValueError if not recognized:
        - "auto": the next speaker is selected automatically by LLM.
        - "manual": the next speaker is selected manually by user input.
        - "random": the next speaker is selected randomly.
        - "round_robin": the next speaker is selected in a round robin fashion, i.e., iterating in the same order as provided in `agents`.

    - allow_repeat_speaker: whether to allow the same speaker to speak consecutively.
        Default is True, in which case all speakers are allowed to speak consecutively.
        If `allow_repeat_speaker` is a list of Agents, then only those listed agents are allowed to repeat.
        If set to False, then no speakers are allowed to repeat.
        `allow_repeat_speaker` and `allowed_or_disallowed_speaker_transitions` are mutually exclusive.
    - allowed_or_disallowed_speaker_transitions: dict.
        The keys are source agents, and the values are agents that the key agent can/can't transit to,
        depending on speaker_transitions_type. Default is None, which means all agents can transit to all other agents.
        `allow_repeat_speaker` and `allowed_or_disallowed_speaker_transitions` are mutually exclusive.
    - speaker_transitions_type: whether the speaker_transitions_type is a dictionary containing lists of allowed agents or disallowed agents.
        "allowed" means the `allowed_or_disallowed_speaker_transitions` is a dictionary containing lists of allowed agents.
        If set to "disallowed", then the `allowed_or_disallowed_speaker_transitions` is a dictionary containing lists of disallowed agents.
        Must be supplied if `allowed_or_disallowed_speaker_transitions` is not None.
    - enable_clear_history: enable possibility to clear history of messages for agents manually by providing
        "clear history" phrase in user prompt. This is experimental feature.
        See description of `GroupChatManager.clear_agents_history` function for more info.
    """

    agents: List[Agent]
    messages: List[Dict]
    max_round: Optional[int] = 10
    admin_name: Optional[str] = "Admin"
    func_call_filter: Optional[bool] = True
    speaker_selection_method: Optional[str] = "auto"
    allow_repeat_speaker: Optional[Union[bool, List[Agent]]] = None
    allowed_or_disallowed_speaker_transitions: Optional[Dict] = None
    speaker_transitions_type: Optional[str] = None
    enable_clear_history: Optional[bool] = False

    _VALID_SPEAKER_SELECTION_METHODS = ["auto", "manual", "random", "round_robin"]
    _VALID_SPEAKER_TRANSITIONS_TYPE = ["allowed", "disallowed", None]

    allowed_speaker_transitions_dict: Dict = field(init=False)

    def __post_init__(self):
        # Post init steers clears of the automatically generated __init__ method from dataclass

        if self.allow_repeat_speaker is not None and not isinstance(self.allow_repeat_speaker, (bool, list)):
            raise ValueError("GroupChat allow_repeat_speaker should be a bool or a list of Agents.")

        # Here, we create allowed_speaker_transitions_dict from the supplied allowed_or_disallowed_speaker_transitions and speaker_transitions_type, and lastly checks for validity.

        # Check input
        if self.speaker_transitions_type is not None:
            self.speaker_transitions_type = self.speaker_transitions_type.lower()

        if self.speaker_transitions_type not in self._VALID_SPEAKER_TRANSITIONS_TYPE:
            raise ValueError(
                f"GroupChat speaker_transitions_type is set to '{self.speaker_transitions_type}'. "
                f"It should be one of {self._VALID_SPEAKER_TRANSITIONS_TYPE} (case insensitive). "
            )

        # If both self.allowed_or_disallowed_speaker_transitions is None and self.allow_repeat_speaker is None, set allow_repeat_speaker to True to ensure backward compatibility
        # Discussed in https://github.com/microsoft/autogen/pull/857#discussion_r1451541204
        if self.allowed_or_disallowed_speaker_transitions is None and self.allow_repeat_speaker is None:
            self.allow_repeat_speaker = True

        # self.allowed_or_disallowed_speaker_transitions and self.allow_repeat_speaker are mutually exclusive parameters.
        # Discussed in https://github.com/microsoft/autogen/pull/857#discussion_r1451266661
        if self.allowed_or_disallowed_speaker_transitions is not None and self.allow_repeat_speaker is not None:
            raise ValueError(
                "Don't provide both allowed_or_disallowed_speaker_transitions and allow_repeat_speaker in group chat. "
                "Please set one of them to None."
            )

        # Asks the user to specify whether the speaker_transitions_type is allowed or disallowed if speaker_transitions_type is supplied
        # Discussed in https://github.com/microsoft/autogen/pull/857#discussion_r1451259524
        if self.allowed_or_disallowed_speaker_transitions is not None and self.speaker_transitions_type is None:
            raise ValueError(
                "GroupChat allowed_or_disallowed_speaker_transitions is not None, but speaker_transitions_type is None. "
                "Please set speaker_transitions_type to either 'allowed' or 'disallowed'."
            )

        # Inferring self.allowed_speaker_transitions_dict
        # Create self.allowed_speaker_transitions_dict if allowed_or_disallowed_speaker_transitions is None, using allow_repeat_speaker
        if self.allowed_or_disallowed_speaker_transitions is None:
            self.allowed_speaker_transitions_dict = {}

            # Create a fully connected allowed_speaker_transitions_dict not including self loops
            for agent in self.agents:
                self.allowed_speaker_transitions_dict[agent] = [
                    other_agent for other_agent in self.agents if other_agent != agent
                ]

            # If self.allow_repeat_speaker is True, add self loops to all agents
            if self.allow_repeat_speaker is True:
                for agent in self.agents:
                    self.allowed_speaker_transitions_dict[agent].append(agent)

            # Else if self.allow_repeat_speaker is a list of Agents, add self loops to the agents in the list
            elif isinstance(self.allow_repeat_speaker, list):
                for agent in self.allow_repeat_speaker:
                    self.allowed_speaker_transitions_dict[agent].append(agent)

        # Create self.allowed_speaker_transitions_dict if allowed_or_disallowed_speaker_transitions is not None, using allowed_or_disallowed_speaker_transitions
        else:
            # Process based on speaker_transitions_type
            if self.speaker_transitions_type == "allowed":
                self.allowed_speaker_transitions_dict = self.allowed_or_disallowed_speaker_transitions
            else:
                # Logic for processing disallowed allowed_or_disallowed_speaker_transitions to allowed_speaker_transitions_dict
                self.allowed_speaker_transitions_dict = invert_disallowed_to_allowed(
                    self.allowed_or_disallowed_speaker_transitions, self.agents
                )

        # Check for validity
        check_graph_validity(
            allowed_speaker_transitions_dict=self.allowed_speaker_transitions_dict,
            agents=self.agents,
        )

    @property
    def agent_names(self) -> List[str]:
        """Return the names of the agents in the group chat."""
        return [agent.name for agent in self.agents]

    def reset(self):
        """Reset the group chat."""
        self.messages.clear()

    def append(self, message: Dict, speaker: Agent):
        """Append a message to the group chat.
        We cast the content to str here so that it can be managed by text-based
        model.
        """
        # set the name to speaker's name if the role is not function
        # if the role is tool, it is OK to modify the name
        if message["role"] != "function":
            message["name"] = speaker.name
        message["content"] = content_str(message["content"])
        self.messages.append(message)

    def agent_by_name(self, name: str) -> Agent:
        """Returns the agent with a given name."""
        return self.agents[self.agent_names.index(name)]

    def next_agent(self, agent: Agent, agents: Optional[List[Agent]] = None) -> Agent:
        """Return the next agent in the list."""
        if agents is None:
            agents = self.agents

        # What index is the agent? (-1 if not present)
        idx = self.agent_names.index(agent.name) if agent.name in self.agent_names else -1

        # Return the next agent
        if agents == self.agents:
            return agents[(idx + 1) % len(agents)]
        else:
            offset = idx + 1
            for i in range(len(self.agents)):
                if self.agents[(offset + i) % len(self.agents)] in agents:
                    return self.agents[(offset + i) % len(self.agents)]

    def select_speaker_msg(self, agents: Optional[List[Agent]] = None) -> str:
        """Return the system message for selecting the next speaker. This is always the *first* message in the context."""
        if agents is None:
            agents = self.agents
        return f"""You are in a role play game. The following roles are available:
{self._participant_roles(agents)}.

Read the following conversation.
Then select the next role from {[agent.name for agent in agents]} to play. Only return the role."""

    def select_speaker_prompt(self, agents: Optional[List[Agent]] = None) -> str:
        """Return the floating system prompt selecting the next speaker. This is always the *last* message in the context."""
        if agents is None:
            agents = self.agents
        return f"Read the above conversation. Then select the next role from {[agent.name for agent in agents]} to play. Only return the role."

    def manual_select_speaker(self, agents: Optional[List[Agent]] = None) -> Union[Agent, None]:
        """Manually select the next speaker."""
        if agents is None:
            agents = self.agents

        print("Please select the next speaker from the following list:")
        _n_agents = len(agents)
        for i in range(_n_agents):
            print(f"{i+1}: {agents[i].name}")
        try_count = 0
        # Assume the user will enter a valid number within 3 tries, otherwise use auto selection to avoid blocking.
        while try_count <= 3:
            try_count += 1
            if try_count >= 3:
                print(f"You have tried {try_count} times. The next speaker will be selected automatically.")
                break
            try:
                i = input("Enter the number of the next speaker (enter nothing or `q` to use auto selection): ")
                if i == "" or i == "q":
                    break
                i = int(i)
                if i > 0 and i <= _n_agents:
                    return agents[i - 1]
                else:
                    raise ValueError
            except ValueError:
                print(f"Invalid input. Please enter a number between 1 and {_n_agents}.")
        return None

    def random_select_speaker(self, agents: Optional[List[Agent]] = None) -> Union[Agent, None]:
        """Randomly select the next speaker."""
        if agents is None:
            agents = self.agents
        return random.choice(agents)

    def _prepare_and_select_agents(
        self, last_speaker: Agent
    ) -> Tuple[Optional[Agent], List[Agent], Optional[List[Dict]]]:
        if self.speaker_selection_method.lower() not in self._VALID_SPEAKER_SELECTION_METHODS:
            raise ValueError(
                f"GroupChat speaker_selection_method is set to '{self.speaker_selection_method}'. "
                f"It should be one of {self._VALID_SPEAKER_SELECTION_METHODS} (case insensitive). "
            )

        # If provided a list, make sure the agent is in the list
        allow_repeat_speaker = (
            self.allow_repeat_speaker
            if isinstance(self.allow_repeat_speaker, bool) or self.allow_repeat_speaker is None
            else last_speaker in self.allow_repeat_speaker
        )

        agents = self.agents
        n_agents = len(agents)
        # Warn if GroupChat is underpopulated
        if n_agents < 2:
            raise ValueError(
                f"GroupChat is underpopulated with {n_agents} agents. "
                "Please add more agents to the GroupChat or use direct communication instead."
            )
        elif n_agents == 2 and self.speaker_selection_method.lower() != "round_robin" and allow_repeat_speaker:
            logger.warning(
                f"GroupChat is underpopulated with {n_agents} agents. "
                "Consider setting speaker_selection_method to 'round_robin' or allow_repeat_speaker to False, "
                "or use direct communication, unless repeated speaker is desired."
            )

        if (
            self.func_call_filter
            and self.messages
            and ("function_call" in self.messages[-1] or "tool_calls" in self.messages[-1])
        ):
            funcs = []
            if "function_call" in self.messages[-1]:
                funcs += [self.messages[-1]["function_call"]["name"]]
            if "tool_calls" in self.messages[-1]:
                funcs += [
                    tool["function"]["name"] for tool in self.messages[-1]["tool_calls"] if tool["type"] == "function"
                ]

            # find agents with the right function_map which contains the function name
            agents = [agent for agent in self.agents if agent.can_execute_function(funcs)]
            if len(agents) == 1:
                # only one agent can execute the function
                return agents[0], agents, None
            elif not agents:
                # find all the agents with function_map
                agents = [agent for agent in self.agents if agent.function_map]
                if len(agents) == 1:
                    return agents[0], agents, None
                elif not agents:
                    raise ValueError(
                        f"No agent can execute the function {', '.join(funcs)}. "
                        "Please check the function_map of the agents."
                    )
        # remove the last speaker from the list to avoid selecting the same speaker if allow_repeat_speaker is False
        agents = [agent for agent in agents if agent != last_speaker] if allow_repeat_speaker is False else agents

        # Filter agents with allowed_speaker_transitions_dict

        is_last_speaker_in_group = last_speaker in self.agents

        # this condition means last_speaker is a sink in the graph, then no agents are eligible
        if last_speaker not in self.allowed_speaker_transitions_dict and is_last_speaker_in_group:
            raise NoEligibleSpeakerException(
                f"Last speaker {last_speaker.name} is not in the allowed_speaker_transitions_dict."
            )
        # last_speaker is not in the group, so all agents are eligible
        elif last_speaker not in self.allowed_speaker_transitions_dict and not is_last_speaker_in_group:
            graph_eligible_agents = []
        else:
            # Extract agent names from the list of agents
            graph_eligible_agents = [
                agent for agent in agents if agent in self.allowed_speaker_transitions_dict[last_speaker]
            ]

        # If there is only one eligible agent, just return it to avoid the speaker selection prompt
        if len(graph_eligible_agents) == 1:
            return graph_eligible_agents[0], graph_eligible_agents, None

        # If there are no eligible agents, return None, which means all agents will be taken into consideration in the next step
        if len(graph_eligible_agents) == 0:
            graph_eligible_agents = None

        # Use the selected speaker selection method
        select_speaker_messages = None
        if self.speaker_selection_method.lower() == "manual":
            selected_agent = self.manual_select_speaker(graph_eligible_agents)
        elif self.speaker_selection_method.lower() == "round_robin":
            selected_agent = self.next_agent(last_speaker, graph_eligible_agents)
        elif self.speaker_selection_method.lower() == "random":
            selected_agent = self.random_select_speaker(graph_eligible_agents)
        else:
            selected_agent = None
            select_speaker_messages = self.messages.copy()
            # If last message is a tool call or function call, blank the call so the api doesn't throw
            if select_speaker_messages[-1].get("function_call", False):
                select_speaker_messages[-1] = dict(select_speaker_messages[-1], function_call=None)
            if select_speaker_messages[-1].get("tool_calls", False):
                select_speaker_messages[-1] = dict(select_speaker_messages[-1], tool_calls=None)
            select_speaker_messages = select_speaker_messages + [
                {"role": "system", "content": self.select_speaker_prompt(graph_eligible_agents)}
            ]
        return selected_agent, graph_eligible_agents, select_speaker_messages

    def select_speaker(self, last_speaker: Agent, selector: ConversableAgent) -> Agent:
        """Select the next speaker."""
        selected_agent, agents, messages = self._prepare_and_select_agents(last_speaker)
        if selected_agent:
            return selected_agent
        # auto speaker selection
        selector.update_system_message(self.select_speaker_msg(agents))
        print("=======mingdebug====>before groupchat.py 366|messages=>",messages)
        messages = clear_up_message_with_empty_content(messages)
        final, name = selector.generate_oai_reply(messages)
        print("=======mingdebug====>after groupchat.py 366=>final=",final,"|name=",name)
        return self._finalize_speaker(last_speaker, final, name, agents)

    async def a_select_speaker(self, last_speaker: Agent, selector: ConversableAgent) -> Agent:
        """Select the next speaker."""
        selected_agent, agents, messages = self._prepare_and_select_agents(last_speaker)
        if selected_agent:
            return selected_agent
        # auto speaker selection
        selector.update_system_message(self.select_speaker_msg(agents))
        final, name = await selector.a_generate_oai_reply(messages)
        return self._finalize_speaker(last_speaker, final, name, agents)

    def _finalize_speaker(self, last_speaker: Agent, final: bool, name: str, agents: Optional[List[Agent]]) -> Agent:
        if not final:
            # the LLM client is None, thus no reply is generated. Use round robin instead.
            return self.next_agent(last_speaker, agents)

        # If exactly one agent is mentioned, use it. Otherwise, leave the OAI response unmodified
        mentions = self._mentioned_agents(name, agents)
        if len(mentions) == 1:
            name = next(iter(mentions))
        else:
            logger.warning(
                f"GroupChat select_speaker failed to resolve the next speaker's name. This is because the speaker selection OAI call returned:\n{name}"
            )

        # Return the result
        try:
            return self.agent_by_name(name)
        except ValueError:
            return self.next_agent(last_speaker, agents)

    def _participant_roles(self, agents: List[Agent] = None) -> str:
        # Default to all agents registered
        if agents is None:
            agents = self.agents

        roles = []
        for agent in agents:
            if agent.description.strip() == "":
                logger.warning(
                    f"The agent '{agent.name}' has an empty description, and may not work well with GroupChat."
                )
            roles.append(f"{agent.name}: {agent.description}".strip())
        return "\n".join(roles)

    def _mentioned_agents(self, message_content: Union[str, List], agents: Optional[List[Agent]]) -> Dict:
        """Counts the number of times each agent is mentioned in the provided message content.

        Args:
            message_content (Union[str, List]): The content of the message, either as a single string or a list of strings.
            agents (List[Agent]): A list of Agent objects, each having a 'name' attribute to be searched in the message content.

        Returns:
            Dict: a counter for mentioned agents.
        """
        if agents is None:
            agents = self.agents

        # Cast message content to str
        if isinstance(message_content, dict):
            message_content = message_content["content"]
        message_content = content_str(message_content)

        mentions = dict()
        for agent in agents:
            regex = (
                r"(?<=\W)" + re.escape(agent.name) + r"(?=\W)"
            )  # Finds agent mentions, taking word boundaries into account
            count = len(re.findall(regex, f" {message_content} "))  # Pad the message to help with matching
            if count > 0:
                mentions[agent.name] = count
        return mentions


class GroupChatManager(ConversableAgent):
    """(In preview) A chat manager agent that can manage a group chat of multiple agents."""

    def __init__(
        self,
        groupchat: GroupChat,
        name: Optional[str] = "chat_manager",
        # unlimited consecutive auto reply by default
        max_consecutive_auto_reply: Optional[int] = sys.maxsize,
        human_input_mode: Optional[str] = "NEVER",
        system_message: Optional[Union[str, List]] = "Group chat manager.",
        **kwargs,
    ):
        if kwargs.get("llm_config") and (kwargs["llm_config"].get("functions") or kwargs["llm_config"].get("tools")):
            raise ValueError(
                "GroupChatManager is not allowed to make function/tool calls. Please remove the 'functions' or 'tools' config in 'llm_config' you passed in."
            )

        super().__init__(
            name=name,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            human_input_mode=human_input_mode,
            system_message=system_message,
            **kwargs,
        )
        # Store groupchat
        self._groupchat = groupchat

        # Order of register_reply is important.
        # Allow sync chat if initiated using initiate_chat
        self.register_reply(Agent, GroupChatManager.run_chat, config=groupchat, reset_config=GroupChat.reset)
        # Allow async chat if initiated using a_initiate_chat
        self.register_reply(
            Agent,
            GroupChatManager.a_run_chat,
            config=groupchat,
            reset_config=GroupChat.reset,
            ignore_async_in_sync_chat=True,
        )

    def chat_messages_for_summary(self, agent: Agent) -> List[Dict]:
        """The list of messages in the group chat as a conversation to summarize.
        The agent is ignored.
        """
        return self._groupchat.messages

    def _prepare_chat(self, recipient: ConversableAgent, clear_history: bool, prepare_recipient: bool = True) -> None:
        super()._prepare_chat(recipient, clear_history, prepare_recipient)

        if clear_history:
            self._groupchat.reset()

        for agent in self._groupchat.agents:
            if (recipient != agent or prepare_recipient) and isinstance(agent, ConversableAgent):
                agent._prepare_chat(self, clear_history, False)

    def run_chat(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[GroupChat] = None,
    ) -> Tuple[bool, Optional[str]]:
        """Run a group chat."""
        if messages is None:
            messages = self._oai_messages[sender]
        message = messages[-1]
        speaker = sender
        groupchat = config
        print("=======mingdebug512====>message=>",message)
        if self.client_cache is not None:
            for a in groupchat.agents:
                a.previous_cache = a.client_cache
                a.client_cache = self.client_cache
        for i in range(groupchat.max_round):
            groupchat.append(message, speaker)
            # broadcast the message to all agents except the speaker
            print("=======mingdebug520====>message=>",message)
            if message["content"] != "":
                for agent in groupchat.agents:
                    if agent != speaker:
                        self.send(message, agent, request_reply=False, silent=True)
            if self._is_termination_msg(message) or i == groupchat.max_round - 1:
                # The conversation is over or it's the last round
                break
            try:
                print("=======mingdebug530====>speaker=>",speaker,"|message=>",message)
                # select the next speaker
                speaker = groupchat.select_speaker(speaker, self)
                print("=======mingdebug533====>speaker=>",speaker)
                # let the speaker speak
                reply = speaker.generate_reply(sender=self)
            except KeyboardInterrupt:
                # let the admin agent speak if interrupted
                if groupchat.admin_name in groupchat.agent_names:
                    # admin agent is one of the participants
                    speaker = groupchat.agent_by_name(groupchat.admin_name)
                    reply = speaker.generate_reply(sender=self)
                else:
                    # admin agent is not found in the participants
                    raise
            except NoEligibleSpeakerException:
                # No eligible speaker, terminate the conversation
                break
            print("=======mingdebug====>547 line,repy=>",reply)
            if reply is None:
                # no reply is generated, exit the chat
                break

            # check for "clear history" phrase in reply and activate clear history function if found
            if (
                groupchat.enable_clear_history
                and isinstance(reply, dict)
                and "CLEAR HISTORY" in reply["content"].upper()
            ):
                reply["content"] = self.clear_agents_history(reply["content"], groupchat)
            # The speaker sends the message without requesting a reply
            speaker.send(reply, self, request_reply=False)
            message = self.last_message(speaker)
        if self.client_cache is not None:
            for a in groupchat.agents:
                a.client_cache = a.previous_cache
                a.previous_cache = None
        return True, None

    async def a_run_chat(
        self,
        messages: Optional[List[Dict]] = None,
        sender: Optional[Agent] = None,
        config: Optional[GroupChat] = None,
    ):
        """Run a group chat asynchronously."""
        if messages is None:
            messages = self._oai_messages[sender]
        message = messages[-1]
        speaker = sender
        groupchat = config
        if self.client_cache is not None:
            for a in groupchat.agents:
                a.previous_cache = a.client_cache
                a.client_cache = self.client_cache
        for i in range(groupchat.max_round):
            groupchat.append(message, speaker)

            if self._is_termination_msg(message):
                # The conversation is over
                break

            # broadcast the message to all agents except the speaker
            print("=======mingdebug592====>message[content]=>",message["content"])
            if message["content"] != "":
                for agent in groupchat.agents:
                    if agent != speaker:
                        await self.a_send(message, agent, request_reply=False, silent=True)
            if i == groupchat.max_round - 1:
                # the last round
                break
            try:
                # select the next speaker
                speaker = await groupchat.a_select_speaker(speaker, self)
                # let the speaker speak
                reply = await speaker.a_generate_reply(sender=self)
            except KeyboardInterrupt:
                # let the admin agent speak if interrupted
                if groupchat.admin_name in groupchat.agent_names:
                    # admin agent is one of the participants
                    speaker = groupchat.agent_by_name(groupchat.admin_name)
                    reply = await speaker.a_generate_reply(sender=self)
                else:
                    # admin agent is not found in the participants
                    raise
            if reply is None:
                break
            # The speaker sends the message without requesting a reply
            await speaker.a_send(reply, self, request_reply=False)
            message = self.last_message(speaker)
        if self.client_cache is not None:
            for a in groupchat.agents:
                a.client_cache = a.previous_cache
                a.previous_cache = None
        return True, None

    def _raise_exception_on_async_reply_functions(self) -> None:
        """Raise an exception if any async reply functions are registered.

        Raises:
            RuntimeError: if any async reply functions are registered.
        """
        super()._raise_exception_on_async_reply_functions()

        for agent in self._groupchat.agents:
            agent._raise_exception_on_async_reply_functions()

    def clear_agents_history(self, reply: str, groupchat: GroupChat) -> str:
        """Clears history of messages for all agents or selected one. Can preserve selected number of last messages.
        That function is called when user manually provide "clear history" phrase in his reply.
        When "clear history" is provided, the history of messages for all agents is cleared.
        When "clear history <agent_name>" is provided, the history of messages for selected agent is cleared.
        When "clear history <nr_of_messages_to_preserve>" is provided, the history of messages for all agents is cleared
        except last <nr_of_messages_to_preserve> messages.
        When "clear history <agent_name> <nr_of_messages_to_preserve>" is provided, the history of messages for selected
        agent is cleared except last <nr_of_messages_to_preserve> messages.
        Phrase "clear history" and optional arguments are cut out from the reply before it passed to the chat.

        Args:
            reply (str): Admin reply to analyse.
            groupchat (GroupChat): GroupChat object.
        """
        # Split the reply into words
        words = reply.split()
        # Find the position of "clear" to determine where to start processing
        clear_word_index = next(i for i in reversed(range(len(words))) if words[i].upper() == "CLEAR")
        # Extract potential agent name and steps
        words_to_check = words[clear_word_index + 2 : clear_word_index + 4]
        nr_messages_to_preserve = None
        agent_to_memory_clear = None

        for word in words_to_check:
            if word.isdigit():
                nr_messages_to_preserve = int(word)
            elif word[:-1].isdigit():  # for the case when number of messages is followed by dot or other sign
                nr_messages_to_preserve = int(word[:-1])
            else:
                for agent in groupchat.agents:
                    if agent.name == word:
                        agent_to_memory_clear = agent
                        break
                    elif agent.name == word[:-1]:  # for the case when agent name is followed by dot or other sign
                        agent_to_memory_clear = agent
                        break
        # clear history
        if agent_to_memory_clear:
            if nr_messages_to_preserve:
                print(
                    f"Clearing history for {agent_to_memory_clear.name} except last {nr_messages_to_preserve} messages."
                )
            else:
                print(f"Clearing history for {agent_to_memory_clear.name}.")
            agent_to_memory_clear.clear_history(nr_messages_to_preserve=nr_messages_to_preserve)
        else:
            if nr_messages_to_preserve:
                print(f"Clearing history for all agents except last {nr_messages_to_preserve} messages.")
                # clearing history for groupchat here
                temp = groupchat.messages[-nr_messages_to_preserve:]
                groupchat.messages.clear()
                groupchat.messages.extend(temp)
            else:
                print("Clearing history for all agents.")
                # clearing history for groupchat here
                groupchat.messages.clear()
            # clearing history for agents
            for agent in groupchat.agents:
                agent.clear_history(nr_messages_to_preserve=nr_messages_to_preserve)

        # Reconstruct the reply without the "clear history" command and parameters
        skip_words_number = 2 + int(bool(agent_to_memory_clear)) + int(bool(nr_messages_to_preserve))
        reply = " ".join(words[:clear_word_index] + words[clear_word_index + skip_words_number :])

        return reply

def clear_up_message_with_empty_content(list_message_content):
    print("=======before clear_up_message_with_empty_content|messages=>",list_message_content,"|list_message_content.length=>",len(list_message_content))
    #filtered_list = [item for item in list_message_content if list_message_content["content"] != '']
    filtered_list = []
    for message in list_message_content:
        if message["content"] != '':
            filtered_list.append(message)
    print("=======after clear_up_message_with_empty_content|messages=>",filtered_list,"|filtered_list.length=>",len(filtered_list))
    return filtered_list