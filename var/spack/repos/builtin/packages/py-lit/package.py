# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLit(PythonPackage):
    """lit is a portable tool for executing LLVM and Clang style test suites,
    summarizing their results, and providing indication of failures. lit is
    designed to be a lightweight testing tool with as simple a user
    interface as possible."""

    pypi = "lit/lit-0.5.0.tar.gz"

    version("0.7.1", sha256="ecef2833aef7f411cb923dac109c7c9dcc7dbe7cafce0650c1e8d19c243d955f")
    version("0.5.0", sha256="3ea4251e78ebeb2e07be2feb33243d1f8931d956efc96ccc2b0846ced212b58c")

    depends_on("py-setuptools", type="build")
