import json
import locale
import os
import shutil
import subprocess
from pathlib import Path

import pytest


@pytest.fixture(scope="module", params=["pyproject_toml", "pixi_toml"])
def pixi_project(tmp_path_factory, request):
    tmpdir = tmp_path_factory.mktemp(request.param)
    manifest_file = "pyproject.toml" if request.param == "pyproject_toml" else "pixi.toml"
    shutil.copyfile(
        Path.cwd() / "tests" / "data" / request.param / manifest_file,
        tmpdir / manifest_file,
    )
    shutil.copyfile(
        Path.cwd() / "tests" / "data" / request.param / "pixi.lock",
        tmpdir / "pixi.lock",
    )
    subprocess.run(
        ["pixi", "install", "--locked", "--no-progress"], cwd=tmpdir, env=environ(), check=True
    )
    return tmpdir


def environ():
    env = os.environ
    # PATH would need to be removed as well we need pixi from PATH
    for var in [
        "CONDA_DEFAULT_ENV",
        "CONDA_PREFIX",
        "PIXI_ENVIRONMENT_NAME",
        "PIXI_ENVIRONMENT_PLATFORMS",
        "PIXI_EXE",
        "PIXI_IN_SHELL",
        "PIXI_PROJECT_MANIFEST",
        "PIXI_PROJECT_NAME",
        "PIXI_PROJECT_ROOT",
        "PIXI_PROJECT_VERSION",
        "PIXI_PROMPT",
    ]:
        if var in env:
            del env[var]
    return env


@pytest.fixture()
def libexec_conda(pixi_project):
    libexec = pixi_project / ".pixi" / "envs" / "default" / "libexec"
    Path.mkdir(libexec, parents=True, exist_ok=True)

    if os.name == "nt":
        shutil.copyfile(Path.cwd() / "conda", libexec / "conda.py")
        shutil.copyfile(Path.cwd() / "conda.bat", libexec / "conda.bat")
        return libexec / "conda.bat"

    # replace shebang with conda env python
    python = pixi_project / ".pixi" / "envs" / "default" / "bin" / "python"
    with Path.open(Path.cwd() / "conda") as f:
        lines = f.readlines()
    lines[0] = f"#!{python}\n"
    with Path.open(libexec / "conda", "w") as f:
        f.writelines(lines)
    Path.chmod(libexec / "conda", 0o755)
    return libexec / "conda"


def run_conda(libexec_conda, *args):
    return (
        subprocess.check_output(
            [
                libexec_conda,
                *args,
            ],
            env=environ(),
        )
        .decode(locale.getpreferredencoding())
        .rstrip()
    )


def test_self_check(libexec_conda):
    run_conda(libexec_conda, "self-check")


def test_info_envs_json(libexec_conda, pixi_project):
    result = run_conda(libexec_conda, "info", "--envs", "--json")
    data = json.loads(result)
    assert isinstance(data, dict)
    assert set(data.keys()) == {"envs_dirs", "conda_prefix", "envs"}
    assert data["envs_dirs"] == [str(pixi_project / ".pixi" / "envs")]
    assert data["conda_prefix"] == str(pixi_project / ".pixi" / "envs")
    assert data["envs"] == [
        str(pixi_project / ".pixi" / "envs" / env)
        for env in ["default", "py39", "py310", "py311", "py312"]
    ]


@pytest.mark.parametrize("env", ["default", "py39", "py310", "py311", "py312"])
@pytest.mark.parametrize("use_prefix", [True, False])
@pytest.mark.parametrize("use_export_format", [True, False])
def test_list(libexec_conda, pixi_project, env: str, use_prefix: bool, use_export_format: bool):
    env_args = ["-p", str(pixi_project / ".pixi" / "envs" / env)] if use_prefix else ["-n", env]
    result = run_conda(libexec_conda, "list", *env_args, *(["-e"] if use_export_format else []))
    assert isinstance(result, str)


@pytest.mark.parametrize("env", ["default", "py39", "py310", "py311", "py312"])
@pytest.mark.parametrize("use_prefix", [True, False])
def test_run(libexec_conda, pixi_project, env: str, use_prefix: bool):
    env_args = ["-p", str(pixi_project / ".pixi" / "envs" / env)] if use_prefix else ["-n", env]
    assert (
        run_conda(
            libexec_conda,
            "run",
            *env_args,
            "--no-capture-output",
            "echo",
            "42",
        )
        == "42"
    )
    assert run_conda(
        libexec_conda,
        "run",
        *env_args,
        "--no-capture-output",
        "python",
        "-c",
        "import sys; print(sys.executable)",
    ).endswith(f"python{'.EXE' if os.name == 'nt' else ''}")


def test_not_implemented(libexec_conda, tmp_path):
    def run_conda_fail_stderr(libexec_conda, *args):
        proc = subprocess.run(
            [
                libexec_conda,
                *args,
            ],
            env=environ(),
            stderr=subprocess.PIPE,
            check=False,
        )
        assert proc.returncode == 1
        return proc.stderr.decode(locale.getpreferredencoding())

    assert "NotImplementedError" in run_conda_fail_stderr(
        libexec_conda, "create", "-p", str(tmp_path / "env")
    )
    assert "NotImplementedError" in run_conda_fail_stderr(
        libexec_conda, "install", "-p", str(tmp_path / "env"), "xtensor"
    )
    activate_output = run_conda_fail_stderr(libexec_conda, "activate", "py39")
    assert "NotImplementedError" in activate_output
    assert "PyCharm will fallback to" in activate_output
