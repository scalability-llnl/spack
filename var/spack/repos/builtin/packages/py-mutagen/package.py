# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMutagen(PythonPackage):
    """Read and write audio tags for many formats."""

    homepage = "https://github.com/quodlibet/mutagen"
    pypi = "mutagen/mutagen-1.45.1.tar.gz"

    license("GPL-2.0-or-later")

    version("1.45.1", sha256="6397602efb3c2d7baebd2166ed85731ae1c1d475abca22090b7141ff5034b3e1")

    depends_on("python@3.5:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
