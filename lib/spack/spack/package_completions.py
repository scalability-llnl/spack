# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from pathlib import Path
from typing import Union

"""Functions relating to shell autocompletion scripts for packages."""


def bash_completion_path(root: Union[str, Path]) -> Path:
    """
    Return standard path for bash completion scripts under root.

    Args:
        root: The prefix root under which to generate the path.

    Returns:
        Standard path for bash completion scripts under root.
    """
    return Path(root) / "share" / "bash-completion" / "completions"


def zsh_completion_path(root: Union[str, Path]) -> Path:
    """
    Return standard path for zsh completion scripts under root.

    Args:
        root: The prefix root under which to generate the path.

    Returns:
        Standard path for zsh completion scripts under root.
    """
    return Path(root) / "share" / "zsh" / "site-functions"


def fish_completion_path(root: Union[str, Path]) -> Path:
    """
    Return standard path for fish completion scripts under root.

    Args:
        root: The prefix root under which to generate the path.

    Returns:
        Standard path for fish completion scripts under root.
    """
    return Path(root) / "share" / "fish" / "vendor_completions.d"
