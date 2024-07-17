"""
   Note: depends on maltoolbox 0.1.3 (not yet released)
   and malsim adapted to that (not released)
"""

import argparse

from malsim.scenario import load_scenario


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Run scenarios in MAL simulator"
        )
    )

    parser.add_argument(
        'scenario_file', type=str,
        help='The scenario file to run'
    )

    parser.add_argument(
        'outfile', type=str,
        help='The file to save the attack graph in'
    )

    args = parser.parse_args()

    # Load scenario and save resulting AttackGraph
    attack_graph = load_scenario(args.scenario_file)
    attack_graph.save_to_file(args.outfile)
    breakpoint()
