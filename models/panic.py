"""
A model to simulate the spread of panic in a crowd.
"""
import math
from APIServer import model_singleton

import lib.actions as acts
import lib.model as mdl


MODEL_NAME = "panic"
PANICKED = "panicked"

DEF_DIM = 10
DEF_NUM_PEOPLE = DEF_DIM * DEF_DIM
DEF_NUM_PANIC = 0
DEF_NUM_CALM = int(0.7 * DEF_NUM_PEOPLE)
DEF_NUM_PANIC = int(0.3 * DEF_NUM_PEOPLE)

AGENT_PREFIX = "Agent"
PANIC_THRESHHOLD = 0.2
CALM_THRESHHOLD = 0.7

CALM = "Calm"
PANIC = "Panic"

additional_group_info = {
    CALM: {
        "next_state": PANIC,
        "threshold_prop": "panic_thresh",
        "threshold_const": PANIC_THRESHHOLD,
    },
    PANIC: {
        "next_state": CALM,
        "threshold_prop": "calm_thresh",
        "threshold_const": CALM_THRESHHOLD,
    },
}


def env_action(env, **kwargs):
    if acts.get_periods(env) == 0:
        calm_grp = acts.get_group(env, CALM)
        switch_to_panic = calm_grp.rand_subset(panic_grps[PANIC][PANICKED])
        for agt_nm in switch_to_panic:
            acts.add_switch(
                acts.get_agent(agt_nm),
                old_group=CALM,
                new_group=PANIC,
            )
    for group_name in additional_group_info:
        group = acts.get_group(env, group_name)
        members = group.get_members()
        current_group = group.name
        next_group = additional_group_info[current_group]["next_state"]
        threshold_prop = additional_group_info[current_group]["threshold_prop"]
        threshold_const = additional_group_info[current_group][
            "threshold_const"
        ]
        for agt_nm in members:
            agent = acts.get_agent(agt_nm)
            mdl = model_singleton.instance
            ratio = acts.neighbor_ratio(
                agent, lambda agent: agent.group_name() == next_group
            )
            transition_threshold = mdl.get_prop(
                threshold_prop, threshold_const
            )
            if ratio > transition_threshold:
                agent.has_acted = True
                acts.add_switch(
                    agent, old_group=current_group, new_group=next_group
                )


panic_grps = {
    CALM: {
        mdl.NUM_MBRS: DEF_NUM_CALM,
        mdl.COLOR: acts.GREEN,
    },
    PANIC: {
        mdl.NUM_MBRS: 0,
        PANICKED: DEF_NUM_PANIC,
        mdl.COLOR: acts.RED,
    },
}


class Panic(mdl.Model):
    """
    Subclass Model to override handle_props().
    """

    def handle_props(self, props):
        super().handle_props(props)
        num_agents = self.height * self.width
        ratio_panic = self.props.get("pct_panic") / 100
        self.num_panic = math.floor(ratio_panic * num_agents)
        self.grp_struct[CALM][mdl.NUM_MBRS] = int(num_agents)
        self.grp_struct[PANIC][PANICKED] = int(ratio_panic * num_agents)


def create_model(serial_obj=None, props=None):
    """
    This is for the sake of the API server; main *could* just
    call Panic() directly.
    """
    if serial_obj is not None:
        return Panic(serial_obj=serial_obj)
    else:
        return Panic(
            MODEL_NAME,
            grp_struct=panic_grps,
            env_action=env_action,
            props=props,
            random_placing=False,
        )


def main():
    model = create_model()
    model.run()
    return 0


if __name__ == "__main__":
    main()
