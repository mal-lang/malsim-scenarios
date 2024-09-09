from pathlib import Path
from malsim.scenario import load_scenario


def dot_entry(node_id, node_data) -> str:
    label = (
        f'{node_id}\\n reward={node_data["extras"]["reward"]}'
        if "extras" in node_data
        else node_id
    )

    compromised = len(node_data["compromised_by"]) > 0

    fillcolor = "grey" if compromised else "white"

    color = "blue" if node_data["type"] == "defense" else "red"

    return f'"{node_id}" [label="{label}", shape="box", color="{color}", fillcolor="{fillcolor}", style="filled"]'


def dot_edges(node_id, node_data) -> str:
    node_type: str = node_data["type"]
    edgestyle = "solid" if node_type == "or" else "dotted"
    parents: dict = node_data["parents"]
    return "\n".join(
        [
            f'"{parent}" -> "{node_id}" [style="{edgestyle}"]'
            for parent in parents.values()
        ]
    )


def dot_content(attack_steps: dict) -> str:
    return "\n".join(
        [
            dot_entry(node_id, node_data) + dot_edges(node_id, node_data)
            for node_id, node_data in attack_steps.items()
        ]
    )


def generate_dot(scenario_file) -> str:
    attack_graph, _ = load_scenario(scenario_file)

    attack_graph_dict = attack_graph._to_dict()

    attack_steps: dict = attack_graph_dict["attack_steps"]

    data = "\n".join(["digraph G {", dot_content(attack_steps), "}"])

    return data


if __name__ == "__main__":
    scenario_dir = Path("scenarios")

    # An alternative way to get all scenario files
    # subdirs = [f for f in scenario_dir.iterdir() if f.is_dir()]
    # scenario_dirs = chain(*[[c for c in d.iterdir() if c.is_dir()] for d in subdirs])
    # scenario_files = [d / "scenario.yml" for d in scenario_dirs]

    scenario_files = scenario_dir.glob("**/*scenario.yml")

    for scenario_file in scenario_files:
        data = generate_dot(scenario_file)
        scenario_dir = scenario_file.parent
        dot_output = scenario_dir / f"{scenario_file.stem}.dot"
        with open(dot_output, "w") as f:
            f.write(data)
