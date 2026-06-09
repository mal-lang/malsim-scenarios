#!/usr/bin/env python3
"""Move root-level scenario settings into the agent blocks in scenario YAML files."""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

import yaml


def update_file(path: Path) -> bool:
    """Update a single scenario file in place."""
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        return False

    agents = data.get("agents")
    if not isinstance(agents, dict):
        return False

    root_rewards = data.get("rewards")
    root_actionable = data.get("actionable_steps")
    root_observable = data.get("observable_steps")

    updated = False

    for agent_name, agent_data in agents.items():
        if not isinstance(agent_data, dict):
            continue

        if root_rewards is not None and "rewards" not in agent_data:
            agent_data["rewards"] = deepcopy(root_rewards)
            updated = True

        if root_actionable is not None and "actionable_steps" not in agent_data:
            agent_data["actionable_steps"] = deepcopy(root_actionable)
            updated = True

        is_defender = str(agent_data.get("type", "")).lower() == "defender"
        if (
            root_observable is not None
            and "observable_steps" not in agent_data
            and is_defender
        ):
            agent_data["observable_steps"] = deepcopy(root_observable)
            updated = True

    if updated:
        data.pop("rewards", None)
        data.pop("actionable_steps", None)
        data.pop("observable_steps", None)
        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True)
            f.write("\n")
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        default="scenarios",
        help="Root directory to scan for scenario.yml files",
    )
    args = parser.parse_args()

    root = Path(args.root)
    changed = []

    for path in root.rglob("*.yml"):
        if "scenario" in path.name.lower() and update_file(path):
            changed.append(str(path))

    print(f"Updated {len(changed)} file(s):")
    for path in changed:
        print(path)


if __name__ == "__main__":
    main()
