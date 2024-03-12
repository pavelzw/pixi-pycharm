# pixi-pycharm

Add Pixi support to PyCharm.

## How to use

1. Run `pixi add pixi-pycharm` in your project.
2. Configure PyCharm: In the *Add Python Interpreter* dialog, select *Conda Environment* and set *Conda executable* to the full path of the `conda` file: `/path-to-project/.pixi/envs/default/libexec/conda`.

## Debugging

Logs are written to `~/.cache/pixi-pycharm.log`.
You can use them to debug problems.
Please attach the logs when filing a bug report.
