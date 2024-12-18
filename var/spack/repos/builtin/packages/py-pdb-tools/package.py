# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPdbTools(PythonPackage):
    """A swiss army knife for manipulating and editing PDB files."""

    homepage = "https://haddocking.github.io/pdb-tools/"
    pypi = "pdb-tools/pdb-tools-2.5.0.tar.gz"

    license("Apache 2.0")

    version("2.5.0", sha256="b76c4cd6304a15e545eff2737a76b71db31b881573e5ba3a93dba9a71a79653b")

    depends_on("py-setuptools", type="build")
