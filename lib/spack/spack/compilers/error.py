# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from ..error import SpackError


class CompilerAccessError(SpackError):
    def __init__(self, compiler, paths):
        super().__init__(
            f"Compiler '{compiler.spec}' has executables that are missing"
            f" or are not executable: {paths}"
        )


class UnsupportedCompilerFlag(SpackError):
    """Raised when a compiler does not support a flag type (e.g. a flag to enforce a
    language standard).
    """
