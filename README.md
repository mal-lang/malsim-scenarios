# malsim-scenarios
A collection of scenarios to be run using the mal-simulator[1] which can be installed with pip.

[1]https://github.com/mal-lang/mal-simulator


## Run scenario
To run a scenario (from ./scenarios), use the cli of MAL Simulator (`malsim`):

`malsim <scenario_file>`

Run `malsim -h` for more info.

This is useful when debugging or using the KeyboardAgent for either the attacker or defender to step through the attackgraph.

If you like to run more custom simulation where observations are extracted, you should load the scenarios with the mal-simulator scenarios python module. Read more in the [readme](https://github.com/mal-lang/mal-simulator/?tab=readme-ov-file#loading-a-scenario-from-a-python-script) of mal-simulator.


## Scenario format
The scenario format was upgraded in mal-simulator 0.3.0. Rewards are not given as full names but instead 'by_asset_name' or 'by_asset_type'.

```yml
by_asset_name:
    ap01:
        read: 2
        fullAccess: 3
        notPresent: 5.0
```

Use this script to convert old scenarios to the new rewards format: https://github.com/mal-lang/mal-simulator/blob/main/scripts/convert_scenario_rewards_to_0.3.0.py
