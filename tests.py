import json
import locale
import os
import subprocess
import sys
from pathlib import Path

import pytest


def run_conda(args):
    return (
        subprocess.check_output(
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
        .decode(locale.getpreferredencoding())
        .rstrip()
    )


def test_self_check():
    run_conda(["self-check"])


def test_info_envs_json():
    result = run_conda(["info", "--envs", "--json"])
    data = json.loads(result)
    assert isinstance(data, dict)
    assert set(data.keys()) == {"envs_dirs", "conda_prefix", "envs"}
    assert data["envs_dirs"] == [f"{os.getcwd()}/.pixi"]
    assert data["conda_prefix"] == f"{os.getcwd()}/.pixi"
    assert data["envs"] == [
        f"{os.getcwd()}/.pixi/envs/{env}" for env in ["default", "py39", "py310", "py311", "py312"]
    ]


@pytest.mark.skip("Not implemented yet")
def test_list_old():
    result = run_conda(["list", "-n", "base"])
    result_e = run_conda(["list", "-n", "base", "-e"])
    ref = subprocess.check_output(["micromamba", "list", "-n", "base"]).strip()
    ref = "\n".join(line.strip() for line in ref.splitlines()[4:])
    assert result == ref
    assert result_e == "\n".join("=".join(line.split()[:-1]) for line in ref.splitlines())


@pytest.mark.parametrize("env", ["default", "py39", "py310", "py311", "py312"])
def test_list(env: str):
    result = run_conda(["list", "-p", f"{os.getcwd()}/.pixi/envs/{env}"])
    assert isinstance(result, str)


@pytest.mark.parametrize("env", ["default", "py39", "py310", "py311", "py312"])
def test_run(env: str):
    assert (
        run_conda(
            [
                "run",
                "-p",
                f"{os.getcwd()}/.pixi/envs/{env}",
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
