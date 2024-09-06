# malsim-scenarios
A collection of scenarios to be run using the mal-simulator[1] which can be installed with pip.

[1]https://github.com/mal-lang/mal-simulator


## Run scenario
To run a scenario (from ./scenarios), use the cli of MAL Simulator (`malsim`):

`malsim <scenario_file>`

Run `malsim -h` for more info.

This is useful when debugging or using the KeyboardAgent for either the attacker or defender to step through the attackgraph.

If you like to run more custom simulation where observations are extracted, you should load the scenarios with the mal-simulator scenarios python module. Read more in the [readme](https://github.com/mal-lang/mal-simulator/?tab=readme-ov-file#loading-a-scenario-from-a-python-script) of mal-simulator.
