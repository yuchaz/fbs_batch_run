# Update the new `sims_featurescheduler`
1. `git clone https://yuchaz@bitbucket.org/yuchaz/sims_featurescheduler.git`
1. Mount this new repo onto docker

# Docker setup
Be sure to run the following commands when starting the docker image each time so that the script can be run without being stopped.
```
git config --global user.email "EMAIL"
git config --global user.name "USER"
```


# Path setup
1. run `cp setup.py.tpl setup.py`
1. Edit the `run_dir` and `sims_fbs` path
1. run `python setup.py` for setting up `path.cfg`

# Prepare weights JSON files
1. Prepare a json files contains the weights that need to be run in batch
1. The json file template can be found in here.
```
[
  [3.0, 0.5, 3.0, 5.0, 3.0, 3.0],
  [3.0, 2.7, 1.0, 3.1, 3.0, 3.0],
  ...
  [1.1, 2.7, 1.0, 3.1, 3.0, 3.0]
]
```
1. The length of the outer list is the total number of runs.
1. Each weight list has length of six, each weight correspond to
```
M5_diff_basis_function
Target_map_basis_function
MeridianStripeBasisFunction
Slewtime_basis_function
Strict_filter_basis_function
Avoid_Fast_Revists
```
respectively.


# CLI
1. Use `python run_batch.py --help` for seeing instructions.
1. `--weights-list-path`: path to the weights JSON file
1. `--opsim-flags`: flags for opsim4. Use `opsim4 --help` to see all the flags that can be set. Need to be included in quote
1. `--run-dir`: If one wants to use a different `run_dir` other than the one set as default before.

## Example commands
`python run_batch.py --weights-list-path weights.json --opsim-flags '--frac-duration 0.003 -v'`

# TODO
- [X] What if `session.db` does not exist? This correspond to the first run.  
- [X] Add the functions of chaning `${OPSIM_HOSTNAME}` in CLI
- [ ] Flexible changes for weights JSON files?
