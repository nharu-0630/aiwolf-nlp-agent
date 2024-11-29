from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING

from utils import agent_util

if TYPE_CHECKING:
    import configparser

    from aiwolf_nlp_common.protocol.info import Info
    from aiwolf_nlp_common.protocol.list.talk_list import TalkList
    from aiwolf_nlp_common.protocol.list.whisper_list import WhisperList
    from aiwolf_nlp_common.protocol.setting import Setting
    from aiwolf_nlp_common.role import Role

    from utils.agent_log import AgentLogger

import random
from threading import Thread
from typing import Callable

from aiwolf_nlp_common import Action
from aiwolf_nlp_common.protocol import Packet
from aiwolf_nlp_common.role import RoleInfo


class Agent:
    def __init__(
        self,
        config: configparser.ConfigParser | None = None,
        name: str | None = None,
        agent_logger: AgentLogger | None = None,
    ) -> None:
        self.name: str = name if name is not None else ""
        self.index: int = -1
        self.received: list[str] = []
        self.comments: list[str] = []
        self.role: Role = RoleInfo.VILLAGER.value
        self.action_timeout: int = 0
        self.packet: Packet | None = None
        self.info: Info | None = None
        self.setting: Setting | None = None
        self.talk_history: TalkList | None = None
        self.whisper_history: WhisperList | None = None
        self.agent_logger = agent_logger
        self.alive_agents: list[str] = []
        self.running: bool = True
        if config is not None:
            with Path.open(
                Path(config.get("path", "random_talk")),
                encoding="utf-8",
            ) as f:
                self.comments = f.read().splitlines()

    @staticmethod
    def timeout(func: Callable) -> Callable:
        def _wrapper(self, *args, **kwargs) -> None:  # noqa: ANN001, ANN002, ANN003
            res = None

            def execute_with_timeout() -> None:
                nonlocal res
                try:
                    res = func(self, *args, **kwargs)
                except Exception as e:  # noqa: BLE001
                    res = e

            thread = Thread(target=execute_with_timeout, daemon=True)
            thread.start()
            if self.action_timeout > 0:
                thread.join(timeout=self.action_timeout)
            else:
                thread.join()

            if isinstance(res, Exception):
                raise res

            return res

        return _wrapper

    @staticmethod
    def logging(func: Callable) -> Callable:
        def _wrapper(self, *args, **kwargs) -> None:  # noqa: ANN001, ANN002, ANN003
            if self.agent_logger is not None:
                self.agent_logger.info("Called %s", func.__name__)
            res = func(self, *args, **kwargs)
            if self.agent_logger is not None:
                self.agent_logger.info("Return %s", res)
            return res

        return _wrapper

    @staticmethod
    def send_agent_idx(func: Callable) -> Callable:
        def _wrapper(self, *args, **kwargs) -> str:  # noqa: ANN001, ANN002, ANN003
            res = func(self, *args, **kwargs)
            if type(res) is not int:
                raise ValueError(res, "is not int")
            return agent_util.agent_idx_to_agent(idx=res)

        return _wrapper

    def append_recv(self, recv: str | list[str]) -> None:
        if type(recv) is str:
            self.received.append(recv)
        elif type(recv) is list:
            self.received.extend(recv)

    def set_packet(self) -> None:
        value = json.loads(self.received.pop(0))
        if self.packet is None:
            self.packet = Packet(
                value=value,
            )
        else:
            self.packet.update(value=value)

    @logging
    def initialize(self) -> None:
        if self.packet is not None:
            self.info = self.packet.info
            self.setting = self.packet.setting

        if self.info is None or self.setting is None:
            return
        self.index = agent_util.agent_name_to_idx(name=self.info.agent)
        self.action_timeout = self.setting.action_timeout
        self.role = self.info.role_map.get_role(agent=self.info.agent)

    @logging
    def daily_initialize(self) -> None:
        if self.packet is not None:
            self.info = self.packet.info
            self.setting = self.packet.setting

        if self.info is None or self.setting is None:
            return
        self.alive_agents = self.info.status_map.get_alive_agent_list()

    @logging
    def daily_finish(self) -> None:
        if self.packet is not None:
            if self.talk_history is None:
                self.talk_history = self.packet.talk_history
            elif self.packet.talk_history is not None:
                self.talk_history.extend(self.packet.talk_history)
            if self.whisper_history is None:
                self.whisper_history = self.packet.whisper_history
            elif self.packet.whisper_history is not None:
                self.whisper_history.extend(self.packet.whisper_history)

    @timeout
    @logging
    def get_name(self) -> str:
        return self.name

    @timeout
    @logging
    def get_role(self) -> Role:
        return self.role

    @timeout
    @logging
    def talk(self) -> str:
        if self.packet is not None:
            if self.talk_history is None:
                self.talk_history = self.packet.talk_history
            elif self.packet.talk_history is not None:
                self.talk_history.extend(self.packet.talk_history)

        return random.choice(self.comments)  # noqa: S311

    @timeout
    @logging
    @send_agent_idx
    def vote(self) -> int:
        target: int = agent_util.agent_name_to_idx(
            name=random.choice(self.alive_agents),  # noqa: S311
        )
        return target

    @timeout
    @logging
    def whisper(self) -> None:
        if self.packet is not None:
            if self.whisper_history is None:
                self.whisper_history = self.packet.whisper_history
            elif self.packet.whisper_history is not None:
                self.whisper_history.extend(self.packet.whisper_history)

    @logging
    def finish(self) -> None:
        if self.packet is not None:
            self.info = self.packet.info
        self.running = False

    def action(self) -> str:  # noqa: C901
        if self.packet is None:
            return ""
        if Action.is_initialize(request=self.packet.request):
            self.initialize()
        elif Action.is_name(request=self.packet.request):
            return self.get_name()
        elif Action.is_role(request=self.packet.request):
            return self.get_role()
        elif Action.is_daily_initialize(request=self.packet.request):
            self.daily_initialize()
        elif Action.is_daily_finish(request=self.packet.request):
            self.daily_finish()
        elif Action.is_talk(request=self.packet.request):
            return self.talk()
        elif Action.is_vote(request=self.packet.request):
            return self.vote()
        elif Action.is_whisper(request=self.packet.request):
            self.whisper()
        elif Action.is_finish(request=self.packet.request):
            self.finish()
        return ""

    def transfer_state(self, prev_agent: Agent) -> None:
        self.name = prev_agent.name
        self.index = prev_agent.index
        self.received = prev_agent.received
        self.comments = prev_agent.comments
        self.role = prev_agent.role
        self.action_timeout = prev_agent.action_timeout
        self.packet = prev_agent.packet
        self.info = prev_agent.info
        self.setting = prev_agent.setting
        self.talk_history = prev_agent.talk_history
        self.whisper_history = prev_agent.whisper_history
        self.agent_logger = prev_agent.agent_logger
        self.alive_agents = prev_agent.alive_agents
        self.running = prev_agent.running
