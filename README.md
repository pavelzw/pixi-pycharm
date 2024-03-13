<h1 align="center">

[![License][license-badge]][license]
[![CI][ci-badge]][ci]
[![Latest release][latest-release-badge]][releases]
[![Project Chat][chat-badge]][chat-url]
[![Pixi Badge][pixi-badge]][pixi]


[license-badge]: https://img.shields.io/github/license/pavelzw/pixi-pycharm?style=flat-square
[license]: ./LICENSE
[ci-badge]: https://img.shields.io/github/actions/workflow/status/pavelzw/pixi-pycharm/ci.yml?style=flat-square
[ci]: https://github.com/pavelzw/pixi-pycharm/actions/
[latest-release-badge]: https://img.shields.io/github/v/tag/pavelzw/pixi-pycharm?style=flat-square&label=latest&sort=semver
[releases]: https://github.com/pavelzw/pixi-pycharm/releases
[chat-badge]: https://img.shields.io/discord/1082332781146800168.svg?label=&logo=discord&logoColor=ffffff&color=7389D8&labelColor=6A7EC2&style=flat-square
[chat-url]: https://discord.gg/kKV8ZxyzY4
[pixi-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json&style=flat-square
[pixi]: https://pixi.sh

</h1>

# pixi-pycharm

Add [pixi](https://github.com/prefix-dev/pixi) support to PyCharm.

> [!WARNING]
> This package does not support Windows as of now, see [#5](https://github.com/pavelzw/pixi-pycharm/issues/5).

## How to use

To get started, add `pixi-pycharm` to your pixi project.

```bash
❯ pixi add pixi-pycharm
```

This will ensure that the conda shim is installed in your project's environment.

> [!TIP]
> If you get the error `could not determine any available versions for pixi-pycharm on win-64` when running `pixi add pixi-pycharm` (even when you're not on Windows),
> this is because the package is not available on Windows and pixi tries to solve the environment for all platforms.
> If you still want to use it in your pixi project (and are on Linux/macOS), you can add the following to your `pixi.toml`:
>
> ```toml
> [target.osx-arm64.dependencies] # or [target.linux-64.dependencies]
> pixi-pycharm = "*"
> ```
>
> This will tell pixi to only use this dependency on a specific platform.

Having `pixi-pycharm` installed, you can now configure PyCharm to use your pixi environments.
Go to the *Add Python Interpreter* dialog (bottom right corner of the PyCharm window) and select *Conda Environment*.
Set *Conda Executable* to the full path of the `conda` file in your pixi environment.
You can get the path using the following command:

```bash
❯ pixi run 'echo $CONDA_PREFIX/libexec/conda'
```

This is an executable that tricks PyCharm into thinking it's the proper `conda` executable.
Under the hood it redirects all calls to the corresponding `pixi` equivalent.

> [!WARNING]
> Please make sure that this is the `conda` shim from this pixi project and not another one.
> If you use multiple pixi projects, you might have to adjust the path accordingly as PyCharm remembers the path to the conda executable.

![Add Python Interpreter](./.github/assets/add-conda-environment-light.png#gh-light-mode-only)
![Add Python Interpreter](./.github/assets/add-conda-environment-dark.png#gh-dark-mode-only)

Having selected the environment, PyCharm will now use the Python interpreter from your pixi environment.

PyCharm should now be able to show you the installed packages as well.

![PyCharm package list](./.github/assets/dependency-list-light.png#gh-light-mode-only)
![PyCharm package list](./.github/assets/dependency-list-dark.png#gh-dark-mode-only)

You can now run your programs and tests as usual.

![PyCharm run tests](./.github/assets/tests-light.png#gh-light-mode-only)
![PyCharm run tests](./.github/assets/tests-dark.png#gh-dark-mode-only)

### Multiple environments

If your project uses [multiple environments](https://pixi.sh/latest/environment) to tests different Python versions or dependencies, you can add multiple environments to PyCharm
by specifying *Use existing environment* in the *Add Python Interpreter* dialog.

![Multiple pixi environments](./.github/assets/python-interpreters-multi-env-light.png#gh-light-mode-only)
![Multiple pixi environments](./.github/assets/python-interpreters-multi-env-dark.png#gh-dark-mode-only)

You can then specify the corresponding environment in the bottom right corner of the PyCharm window.

![Specify environment](./.github/assets/specify-interpreter-light.png#gh-light-mode-only)
![Specify environment](./.github/assets/specify-interpreter-dark.png#gh-dark-mode-only)

### Multiple pixi projects

When using multiple pixi projects, remember to select the correct *Conda Executable* for each project as mentioned above.
It also might come up that you have multiple environments it might come up that you have multiple environments with the same name.

![Multiple default environments](./.github/assets/multiple-default-envs-light.png#gh-light-mode-only)
![Multiple default environments](./.github/assets/multiple-default-envs-dark.png#gh-dark-mode-only)

It is recommended to rename the environments to something unique.

## Debugging

Logs are written to `~/.cache/pixi-pycharm.log`.
You can use them to debug problems.
Please attach the logs when [filing a bug report](https://github.com/pavelzw/pixi-pycharm/issues/new?template=bug-report.md).
