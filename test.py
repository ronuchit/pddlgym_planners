"""Tests that planners run and succeed
"""

import pddlgym
from pddlgym_planners.ff import FF  # FastForward
from pddlgym_planners.fd import FD  # FastDownward

def test_planners():
    """Make sure that the plans found by the planners
    succeed in the environments
    """
    planners = [FF(), FD(), FD(alias_flag="--alias lama-first")]
    env_names = ["PDDLEnvBlocks-v0", "PDDLEnvBlocks_operator_actions-v0"]

    for planner in planners:
        for env_name in env_names:
            env = pddlgym.make(env_name)
            state, _ = env.reset()
            plan = planner(env.domain, state)
            for act in plan:
                _, reward, done, _, _ = env.step(act)
            assert reward == 1.
            assert done

def test_readme_example():
    """Make sure that the README example runs
    """
    # Planning with FastForward
    ff_planner = FF()
    env = pddlgym.make("PDDLEnvBlocks-v0")
    state, _ = env.reset()
    print("Plan:", ff_planner(env.domain, state))
    print("Statistics:", ff_planner.get_statistics())

    # Planning with FastDownward (--alias seq-opt-lmcut)
    fd_planner = FD()
    env = pddlgym.make("PDDLEnvBlocks-v0")
    state, _ = env.reset()
    print("Plan:", fd_planner(env.domain, state))
    print("Statistics:", fd_planner.get_statistics())

    # Planning with FastDownward (--alias lama-first)
    lama_first_planner = FD(alias_flag="--alias lama-first")
    env = pddlgym.make("PDDLEnvBlocks-v0")
    state, _ = env.reset()
    print("Plan:", lama_first_planner(env.domain, state))
    print("Statistics:", lama_first_planner.get_statistics())


if __name__ == "__main__":
    test_planners()
    test_readme_example()
