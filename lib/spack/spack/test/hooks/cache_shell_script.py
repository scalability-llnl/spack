# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest
import sys

from spack.main import SpackCommand
from spack.spec import Spec

install = SpackCommand("install")


@pytest.mark.parametrize(
    "shell,set_command",
    (
        [("bat", 'set "%s=%s"')]
        if sys.platform == "win32"
        else [("sh", "export %s=%s"), ("csh", "setenv %s %s")]
    ),
)
def test_install_shell_cached(
    shell, set_command, install_mockery, mock_fetch, mock_archive, mock_packages
    ):
    os.environ["SPACK_SHELL"] = shell

    spec = Spec("mpileaks")
    spec.concretize()

    install(spec.name)

    for pkg in spec.traverse():
        path_to_shell = os.path.join(pkg.prefix, ".spack", f"{pkg.name}_shell.{shell}")
    
        assert os.path.isfile(path_to_shell)