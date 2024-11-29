from __future__ import annotations

import random

from aiwolf_nlp_common import Action

from player.agent import Agent
from utils import agent_util


class Werewolf(Agent):

    def __init__(self) -> None:
        super().__init__()

    @Agent.timeout
    @Agent.logging
    @Agent.send_agent_idx
    def attack(self) -> int:
        target: int = agent_util.agent_name_to_idx(
            random.choice(self.alive_agents),  # noqa: S311
        )
        return target

    def action(self) -> str:
        if self.packet is not None and Action.is_attack(request=self.packet.request):
            return self.attack()
        return super().action()
