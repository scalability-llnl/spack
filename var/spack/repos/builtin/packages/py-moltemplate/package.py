# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMoltemplate(PythonPackage):
    """Moltemplate is a general cross-platform text-based molecule builder for
    LAMMPS."""

    homepage = "https://moltemplate.org"
    url = "https://github.com/jewettaij/moltemplate/archive/v2.5.8.tar.gz"

    license("MIT")

    version("2.5.8", sha256="f1e2d52249e996d85f5b1b7b50f50037da9e4b9c252cdfc622b21e79aa21162f")

    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
