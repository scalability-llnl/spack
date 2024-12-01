# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Easybuild(PythonPackage):
    """EasyBuild is a software build and installation framework
    for (scientific) software on HPC systems.
    """

    homepage = "https://easybuilders.github.io/easybuild/"
    pypi = "easybuild/easybuild-4.0.0.tar.gz"
    maintainers("boegel")

    license("GPL-2.0-or-later")

    version("4.7.0", sha256="e68c280e3a508965aefbdf234872919f777f739cf4787cb11bb97a56e0cf74a6")
    version("4.0.0", sha256="21bcc1048525ad6219667cc97a7421b5388068c670cabba356712e474896de40")

    depends_on("python@3.5:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")

    for v in ["@4.0.0", "@4.7.0"]:
        depends_on("py-easybuild-framework" + v, when=v, type="run")
        depends_on("py-easybuild-easyblocks" + v, when=v, type="run")
        depends_on("py-easybuild-easyconfigs" + v, when=v, type="run")
