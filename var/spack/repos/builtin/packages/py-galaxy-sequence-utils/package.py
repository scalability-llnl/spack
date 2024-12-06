# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxySequenceUtils(PythonPackage):
    """Galaxy utilities for manipulating sequences Galaxy project."""

    homepage = "https://github.com/galaxyproject/sequence_utils"
    pypi = "galaxy-sequence-utils/galaxy_sequence_utils-1.1.5.tar.gz"

    license("CC-BY-3.0")

    version("1.1.5", sha256="c32bd91f6ff11ad6e8b62f8de309d695ef5c33a782afbf5122c1db7144ef1162")

    depends_on("python@3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
