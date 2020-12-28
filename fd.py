"""Fast-downward planner.
http://www.fast-downward.org/ObtainingAndRunningFastDownward
"""

import re
import os
import sys
import subprocess
import tempfile
from pddlgym_planners.pddl_planner import PDDLPlanner
from pddlgym_planners.planner import PlanningFailure

FD_URL = "https://github.com/ronuchit/downward.git"


class FD(PDDLPlanner):
    """Fast-downward planner.
    """
    def __init__(self, alias_flag="--alias seq-opt-lmcut", final_flags=""):
        super().__init__()
        dirname = os.path.dirname(os.path.realpath(__file__))
        self._exec = os.path.join(dirname, "FD/fast-downward.py")
        print("Instantiating FD", end=' ')
        if alias_flag:
            print("with", alias_flag, end=' ')
        if final_flags:
            print("with", final_flags, end=' ')
        print()
        self._alias_flag = alias_flag
        self._final_flags = final_flags
        if not os.path.exists(self._exec):
            self._install_fd()

    def _get_cmd_str(self, dom_file, prob_file, timeout):
        sas_file = tempfile.NamedTemporaryFile(delete=False).name
        timeout_cmd = "gtimeout" if sys.platform == "darwin" else "timeout"
        cmd_str = "{} {} {} {} --sas-file {} {} {} {}".format(
            timeout_cmd, timeout, self._exec, self._alias_flag, sas_file,
            dom_file, prob_file, self._final_flags)
        return cmd_str

    def _cleanup(self):
        """Run FD cleanup
        """
        cmd_str = "{} --cleanup".format(self._exec)
        subprocess.getoutput(cmd_str)

    def _output_to_plan(self, output):
        # Technically this is number of evaluated states which is always
        # 1+number of expanded states, but we report evaluated for consistency
        # with FF.
        num_node_expansions = re.findall(
            r"evaluated (\d+) state", output.lower())
        if "num_node_expansions" not in self._statistics:
            self._statistics["num_node_expansions"] = 0
        if len(num_node_expansions) == 1:
            assert int(num_node_expansions[0]) == float(num_node_expansions[0])
            self._statistics["num_node_expansions"] += int(
                num_node_expansions[0])
        if "Solution found!" not in output:
            raise PlanningFailure("Plan not found with FD! Error: {}".format(
                output))
        if "Plan length: 0 step" in output:
            return []
        fd_plan = re.findall(r"(.+) \(\d+?\)", output.lower())
        if not fd_plan:
            raise PlanningFailure("Plan not found with FD! Error: {}".format(
                output))
        return fd_plan

    def _install_fd(self):
        loc = os.path.dirname(self._exec)
        # Install and compile FD.
        os.system("git clone {} {}".format(FD_URL, loc))
        os.system("cd {} && ./build.py && cd -".format(loc))
        assert os.path.exists(self._exec)
