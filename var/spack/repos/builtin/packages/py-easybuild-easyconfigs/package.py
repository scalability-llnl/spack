# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEasybuildEasyconfigs(PythonPackage):
    """Collection of easyconfig files for EasyBuild, a software build and
    installation framework for (scientific) software on HPC systems.
    """

    homepage = "https://easybuilders.github.io/easybuild"
    pypi = "easybuild-easyconfigs/easybuild-easyconfigs-4.0.0.tar.gz"
    maintainers("boegel")

    license("GPL-2.0-only")

    version("4.7.0", sha256="c688f14a3b0dce45c6cc90d746f05127dbf7368bd9b5873ce50757992d8e6261")
    version("4.0.0", sha256="90d4e8f8abb11e7ae2265745bbd1241cd69d02570e9b4530175c4b2e2aba754e")

    depends_on("python@3.5:", type=("build", "run"))
    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")

    for v in ["@4.0.0", "@4.7.0"]:
        depends_on("py-easybuild-framework{0}:".format(v), when=v + ":", type="run")
        depends_on("py-easybuild-easyblocks{0}:".format(v), when=v, type="run")
