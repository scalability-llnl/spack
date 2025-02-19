# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.environment as ev
import spack.scripts.checkpoint as checkpoint
from spack.main import SpackCommand

pytestmark = [
    pytest.mark.usefixtures("mutable_mock_env_path", "config", "mutable_mock_repo"),
    pytest.mark.maybeslow,
    pytest.mark.not_on_windows("Envs unsupported on Window"),
]

config = SpackCommand("config")


def test_checkpoint():
    e = ev.create("test")
    e.add("mpileaks")
    e.concretize()
    e.write()

    with e:
        checkpoint.update_checkpoint(e)
        assert checkpoint.check_checkpoint(e) == "equal"

    e.add("dt-diamond")
    e.write()

    with e:
        assert checkpoint.check_checkpoint(e) == "unequal"
        checkpoint.update_checkpoint(e)
        assert checkpoint.check_checkpoint(e) == "equal"

    with e:
        config("add", "packages:mpileaks:require:'@2.2'")
        e.write()
        assert checkpoint.check_checkpoint(e) == "unequal"
        checkpoint.update_checkpoint(e)
        assert checkpoint.check_checkpoint(e) == "equal"
