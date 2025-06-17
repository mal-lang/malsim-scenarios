"""Create variants with different number of APs"""

from argparse import ArgumentParser
import os
import copy

from maltoolbox.model import Model, ModelAsset
from maltoolbox.language import LanguageGraph
from malsim.scenario import path_relative_to_file_dir

import yaml

def get_creds_for_app(app: ModelAsset) -> set[ModelAsset]:
    """Get all credentials connected to an identity on the given app"""
    identities = get_identities_for_asset(app)
    creds = set()
    for identity in identities:
        creds |= identity.associated_assets.get('credentials', set())
    return creds


def get_identities_for_asset(asset: ModelAsset) -> set[ModelAsset]:
    """Get all identities connected to asset"""
    identities = set()
    if asset.type == 'Application':
        identities.update(
            asset.associated_assets.get('executionPrivIAMs', set())
        )
        identities.update(
            asset.associated_assets.get('highPrivAppIAMs', set())
        )
        identities.update(
            asset.associated_assets.get('lowPrivAppIAMs', set())
        )
    return identities


def get_connection_rules_for_asset(asset: ModelAsset) -> set[ModelAsset]:
    """Return all connection rules leading from or to asset"""

    # Possible field_names to ConnectionRule in association
    connection_rule_field_names = [
        "interNetConnections",
        "netConnections",
        "ingoingNetConnections",
        "outgoingNetConnections",
        "appConnections",
        "interAppConnections",
        "ingoingAppConnections",
        "outgoingAppConnections",
    ]

    associated_crs = set()
    for field_name in connection_rule_field_names:
        associated_crs |= asset.associated_assets.get(field_name, set())
    return associated_crs


def save_scenario_to_folder(
        scenario: dict, model: Model, dir: str
    ):
    """Save scenario and model to a directory"""
    if not os.path.exists(dir):
        os.makedirs(dir)

    scenario_path = f"{dir}/scenario.yml"
    model_path = f"{dir}/model.yml"
    scenario['lang_file'] = "../" + scenario['lang_file']

    with open(scenario_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(scenario, f, sort_keys=False)

    model.save_to_file(model_path)


def alter_scenario(
        scenario: dict, model: Model, num_aps: int
    ):
    """Remove APs until the number of APs is as expected"""

    new_scenario = copy.deepcopy(scenario)

    all_ap_assets = [
        asset for asset in model.assets.values()
        if asset.name.startswith("ap")
    ]
    removed_assets = []
    while len(all_ap_assets) > num_aps:
        ap_to_remove = all_ap_assets.pop()
        assets_to_remove = [ap_to_remove]
        assets_to_remove += get_connection_rules_for_asset(ap_to_remove)
        assets_to_remove += get_identities_for_asset(ap_to_remove)
        assets_to_remove += get_creds_for_app(ap_to_remove)
        assets_to_remove += ap_to_remove.associated_assets.get(
            'vulnerabilities', set()
        )

        for asset in assets_to_remove:
            model.remove_asset(asset)
            removed_assets.append(asset.name)

    new_rewards = {}
    for attackstep_full_name, reward in new_scenario['rewards'].items():
        asset_name = attackstep_full_name.split(':')[0]
        if asset_name not in removed_assets:
            new_rewards[attackstep_full_name] = reward

    new_scenario['rewards'] = new_rewards
    return new_scenario, model

def get_scenario(scenario_file: str) -> tuple[dict, str, str]:
    """Return scenario dict and lang/model file paths"""
    with open(scenario_file, 'r', encoding='utf-8') as s_file:
        scenario = yaml.safe_load(s_file)
        lang_file = path_relative_to_file_dir(scenario['lang_file'], s_file)
        model_file = path_relative_to_file_dir(scenario['model_file'], s_file)
    return scenario, lang_file, model_file

def create_scenario_variants(
    scenario_file: str,
    min_aps: int,
    max_aps: int
):
    """Alter scenarios and save them to folders"""
    scenario, lang_file, model_file = get_scenario(scenario_file)
    lang_graph = LanguageGraph.load_from_file(lang_file)

    variants = list(range(min_aps, max_aps + 1))
    for num_aps in variants:
        # Reload model for each new scenario so we can alter it freely
        model = Model.load_from_file(model_file, lang_graph)
        new_scenario, model = alter_scenario(scenario, model, num_aps)
        save_scenario_to_folder(
            new_scenario, model, f"scenario-{num_aps}-aps"
        )


def main():
    parser = ArgumentParser()

    parser.add_argument(
        "scenario_file", type=str
    )
    parser.add_argument(
        "--max_aps", type=int, default=16
    )
    parser.add_argument(
        "--min_aps", type=int, default=0
    )
    
    args = parser.parse_args()
    create_scenario_variants(
        args.scenario_file,
        args.min_aps,
        args.max_aps
    )

if __name__ == "__main__":
    main()
