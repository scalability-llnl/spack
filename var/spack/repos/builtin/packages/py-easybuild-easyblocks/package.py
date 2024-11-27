# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEasybuildEasyblocks(PythonPackage):
    """Collection of easyblocks for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = "https://easybuilders.github.io/easybuild"
    pypi = "easybuild-easyblocks/easybuild-easyblocks-4.0.0.tar.gz"
    maintainers("boegel")

    license("GPL-2.0-only")

    version("4.7.0", sha256="c23e81cbaa3e4fa5ab1bb8b2db759332867d61110bf4ec34763ea170780f0655")
    version("4.0.0", sha256="a0fdef6c33c786e323bde1b28bab942fd8e535c26842877d705e692e85b31b07")

    depends_on("python@3.5:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")

    for v in ["@4.0.0", "@4.7.0"]:
        depends_on("py-easybuild-framework" + v, when=v, type="run")
