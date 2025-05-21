import math
import random

import pandas as pd

MACHINE_TYPES = {
    "Excavator": 2,
    "Forklift": 2,
    "Generator": 2,
    "Conveyor Belt": 2,
}

# OLD COMPONENT VALUES
# Each component has: base_lifespan and service_impact (as percentage extension per maintenance)
# "Excavator": {
#     "Hydraulic Pump": {"lifespan": 10000, "service_impact": 0.1},
#     "Brake System": {"lifespan": 8000, "service_impact": 0.2},
#     "Engine": {"lifespan": 15000, "service_impact": 0.15},
# },
# "Forklift": {
#     "Battery": {"lifespan": 12000, "service_impact": 0.05},
#     "Brake System": {"lifespan": 8000, "service_impact": 0.1},
#     "Wiring Harness": {"lifespan": 14000, "service_impact": 0.0},
# },
# "Generator": {
#     "Alternator": {"lifespan": 13000, "service_impact": 0.08},
#     "Cooling System": {"lifespan": 11000, "service_impact": 0.2},
#     "Wiring Harness": {"lifespan": 14000, "service_impact": 0.1},
# },
# "Conveyor Belt": {
#     "Motor": {"lifespan": 9000, "service_impact": 0.07},
#     "Belt": {"lifespan": 7000, "service_impact": 0.1},
#     "Sensors": {"lifespan": 5000, "service_impact": 0.12},
# },

COMPONENTS = {
    "Excavator": {
        "Hydraulic Pump": {"lifespan": 10000, "service_impact": 0.03},
        "Brake System": {"lifespan": 8000, "service_impact": 0.05},
        "Engine": {"lifespan": 15000, "service_impact": 0.09},
    },
    "Forklift": {
        "Battery": {"lifespan": 12000, "service_impact": 0.04},
        "Brake System": {"lifespan": 8000, "service_impact": 0.1},
        "Wiring Harness": {"lifespan": 14000, "service_impact": 0.02},
    },
    "Generator": {
        "Alternator": {"lifespan": 13000, "service_impact": 0.03},
        "Cooling System": {"lifespan": 11000, "service_impact": 0.09},
        "Wiring Harness": {"lifespan": 14000, "service_impact": 0.06},
    },
    "Conveyor Belt": {
        "Motor": {"lifespan": 9000, "service_impact": 0.04},
        "Belt": {"lifespan": 7000, "service_impact": 0.1},
        "Sensors": {"lifespan": 5000, "service_impact": 0.07},
    },
}

COSTS = {
    "Hydraulic Pump": 500,
    "Brake System": 200,
    "Engine": 1000,
    "Battery": 150,
    "Wiring Harness": 300,
    "Alternator": 700,
    "Cooling System": 400,
    "Motor": 600,
    "Belt": 250,
    "Sensors": 180,
}

# a +/-10% variability in the lifespan for each component
VARIABILITY = 0.10
MAX_RECORDS = 500
# fixed interval between machine maintenance services
SERVICE_INTERVAL = 3000


def sample_lifespan(base):
    # variation is anywhere between 0 and 10% of the full lifespan
    variation = base * VARIABILITY * random.random()
    # random either add or subtract the variability
    return round(random.uniform(base - variation, base + variation))


def generate_machine_data(machine_id, machine_type):
    components_base = COMPONENTS[machine_type]
    component_states = {}
    records = []
    active_time = 0
    service_times = []

    # initialize the first failure
    for comp, props in components_base.items():
        lifespan = sample_lifespan(props["lifespan"])
        component_states[comp] = {
            "next_failure": active_time + lifespan,
            "lifespan": lifespan,
            "install_time": active_time,
            "failure_count": 0,
        }

    while len(records) < MAX_RECORDS:
        # determine next component to fail
        next_events = {
            comp: state["next_failure"] for comp, state in component_states.items()
        }
        failed_component = min(next_events, key=next_events.get)
        failure_time = math.floor(next_events[failed_component])

        # insert the services between the current and the next failure
        while (
            len(service_times) == 0
            or service_times[-1] + SERVICE_INTERVAL < failure_time
        ):
            service_time = math.floor(
                (service_times[-1] + SERVICE_INTERVAL)
                if service_times
                else SERVICE_INTERVAL
            )
            service_times.append(service_time)
            records.append(
                {
                    "machine_id": machine_id,
                    "machine_type": machine_type,
                    "active_time": service_time,
                    "fault_type": "",  # No component failed
                    "repair/replace_type": "Maintenance Service",
                    "cost": 50,
                    "event_type": "Service",
                }
            )

        # count the amount of services between last failure (install event for the component) and the next failure
        services_since_install = [
            t
            for t in service_times
            if component_states[failed_component]["install_time"] < t < failure_time
        ]
        service_boost = (
            len(services_since_install)
            * components_base[failed_component]["service_impact"]
        )
        adjusted_lifespan = sample_lifespan(
            components_base[failed_component]["lifespan"]
        ) * (1 + service_boost / 2)

        # insert the next failure event
        records.append(
            {
                "machine_id": machine_id,
                "machine_type": machine_type,
                "active_time": failure_time,
                "fault_type": failed_component,
                "repair/replace_type": f"Replaced {failed_component}",
                "cost": COSTS[failed_component],
                "event_type": "Failure",
            }
        )

        # reset component states back so it acts like a new component
        component_states[failed_component]["install_time"] = failure_time
        component_states[failed_component]["lifespan"] = adjusted_lifespan
        component_states[failed_component]["next_failure"] = (
            failure_time + adjusted_lifespan
        )
        component_states[failed_component]["failure_count"] += 1

        # random preemptive replacement events, mocking real life
        if random.random() < 0.1:
            preempt_comp = random.choice(list(component_states.keys()))
            now = failure_time + 500
            records.append(
                {
                    "machine_id": machine_id,
                    "machine_type": machine_type,
                    "active_time": now,
                    "fault_type": preempt_comp,
                    "repair/replace_type": f"Preemptive Replacement of {preempt_comp}",
                    "cost": COSTS[preempt_comp],
                    "event_type": "Preemptive Replacement",
                }
            )
            component_states[preempt_comp]["install_time"] = now
            component_states[preempt_comp]["lifespan"] = sample_lifespan(
                components_base[preempt_comp]["lifespan"]
            )
            component_states[preempt_comp]["next_failure"] = (
                now + component_states[preempt_comp]["lifespan"]
            )

    return records


def generate_dataset():
    dataset = []
    machine_id = 1
    for machine_type, count in MACHINE_TYPES.items():
        for _ in range(count):
            machine_records = generate_machine_data(machine_id, machine_type)
            dataset.extend(machine_records)
            machine_id += 1

    df = pd.DataFrame(dataset)
    df.sort_values(by=["machine_id", "active_time"], inplace=True)
    return df


df = generate_dataset()
df.to_csv("synthetic_failure_and_service_data.csv", index=False)
print(df.head(10))
