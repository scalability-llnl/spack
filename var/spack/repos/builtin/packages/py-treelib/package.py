# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTreelib(PythonPackage):
    """A Python implementation of tree structure."""

    homepage = "https://github.com/caesar0301/treelib"
    pypi = "treelib/treelib-1.7.0.tar.gz"

    license("Apache-2.0")

    version("1.7.0", sha256="9bff1af416b9e642a6cd0e0431d15edf26a24b8d0c8ae68afbd3801b5e30fb61")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
