# pixi-pycharm

Add Pixi support to PyCharm.

## How to use

1. Clone this repo.
2. Use `./conda self-check` to see if pixi is properly installed.
3. Move `conda` file from this repo to `/path/to/project/.pixi/envs/<env>/libexec/conda` (the path must match exactly) (a symlink is sufficient as well).
4. Configure PyCharm: In the *Add Python Interpreter* dialog, select *Conda Environment* and set *Conda executable* to the full path of the `conda` file of the cloned repo.

## Debugging

Logs are written to `~/.cache/pixi-pycharm.log`.
You can use them to debug problems.
Please attach the logs when filing a bug report.
