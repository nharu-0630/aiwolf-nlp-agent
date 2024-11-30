import re

from aiwolf_nlp_common.role import RoleInfo

import core


def set_role(
    prev_agent: core.agent.Agent,
) -> core.agent.Agent:
    agent: core.agent.Agent
    if RoleInfo.is_villager(role=prev_agent.agent_role):
        agent = core.villager.Villager()
    elif RoleInfo.is_werewolf(role=prev_agent.agent_role):
        agent = core.werewolf.Werewolf()
    elif RoleInfo.is_seer(role=prev_agent.agent_role):
        agent = core.seer.Seer()
    elif RoleInfo.is_possessed(role=prev_agent.agent_role):
        agent = core.possessed.Possessed()
    else:
        raise ValueError(prev_agent.agent_role, "Role is not defined")
    agent.transfer_state(prev_agent=prev_agent)
    return agent


def agent_name_to_idx(name: str) -> int:
    match = re.search(r"\d+", name)
    if match is None:
        raise ValueError(name, "No number found in agent name")
    return int(match.group())


def agent_idx_to_agent(idx: int) -> str:
    return f"Agent[{idx:0>2d}]"
