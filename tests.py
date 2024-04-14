import json
import locale
import os
import subprocess
import sys
from pathlib import Path

import pytest


def run_conda(args):
    if os.name == "nt":
        output = subprocess.check_output(
            [
                Path.cwd()
                / ".pixi"
                / "envs"
                / os.environ["PIXI_ENVIRONMENT_NAME"]
                / "libexec"
                / "conda.bat",
                *args,
            ],
        )
    else:
        output = subprocess.check_output(
            [
                sys.executable,
                Path.cwd()
                / ".pixi"
                / "envs"
                / os.environ["PIXI_ENVIRONMENT_NAME"]
                / "libexec"
                / "conda",
                *args,
            ],
        )
    return output.decode(locale.getpreferredencoding()).rstrip()


def test_self_check():
    run_conda(["self-check"])


def test_info_envs_json():
    result = run_conda(["info", "--envs", "--json"])
    data = json.loads(result)
    assert isinstance(data, dict)
    assert set(data.keys()) == {"envs_dirs", "conda_prefix", "envs"}
    assert data["envs_dirs"] == [str(Path.cwd() / ".pixi" / "envs")]
    assert data["conda_prefix"] == str(Path.cwd() / ".pixi" / "envs")
    assert data["envs"] == [
        str(Path.cwd() / ".pixi" / "envs" / env)
        for env in ["default", "py39", "py310", "py311", "py312"]
    ]


@pytest.mark.parametrize("env", ["default", "py39", "py310", "py311", "py312"])
@pytest.mark.parametrize("use_prefix", [True, False])
@pytest.mark.parametrize("use_export_format", [True, False])
def test_list(env: str, use_prefix: bool, use_export_format: bool):
    env_args = ["-p", str(Path.cwd() / ".pixi" / "envs" / env)] if use_prefix else ["-n", env]
    result = run_conda(["list", *env_args, *(["-e"] if use_export_format else [])])
    assert isinstance(result, str)


@pytest.mark.parametrize("env", ["default", "py39", "py310", "py311", "py312"])
@pytest.mark.parametrize("use_prefix", [True, False])
def test_run(env: str, use_prefix: bool):
    env_args = ["-p", str(Path.cwd() / ".pixi" / "envs" / env)] if use_prefix else ["-n", env]
    assert (
        run_conda(
            [
                "run",
                *env_args,
                "--no-capture-output",
                "echo",
                "42",
            ],
        )
        == "42"
    )


@pytest.mark.skip("Not implemented yet")
def test_create(tmp_path):
    run_conda(["create", "-p", str(tmp_path / "env")])
    run_conda(["install", "-p", str(tmp_path / "env"), "xtensor"])
