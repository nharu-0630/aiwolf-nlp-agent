from __future__ import annotations

from core.agent import Agent


class Villager(Agent):

    def __init__(self) -> None:
        super().__init__()

    @Agent.timeout
    @Agent.logging
    def talk(self) -> str:
        super().talk()
        return "a"
