# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIlluminaUtils(PythonPackage):
    """A library and collection of scripts to work with Illumina paired-end
    data (for CASAVA 1.8+)."""

    homepage = "https://github.com/meren/illumina-utils"
    pypi = "illumina-utils/illumina-utils-2.2.tar.gz"

    license("GPL-2.0-or-later")

    version("2.3", sha256="0e8407b91d530d9a53d8ec3c83e60f25e7f8f80d06ce17b8e4f57a02d3262441")
    version("2.2", sha256="6039c72d077c101710fe4fdbfeaa30caa1c3c2c84ffa6295456927d82def8e6d")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-python-levenshtein", type=("build", "run"))
