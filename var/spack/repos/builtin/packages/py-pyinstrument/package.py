# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyinstrument(PythonPackage):
    """Call stack profiler for Python. Shows you why your code is slow!"""

    homepage = "https://github.com/joerick/pyinstrument"
    pypi = "pyinstrument/pyinstrument-4.0.3.tar.gz"

    license("BSD-3-Clause")

    version("4.4.0", sha256="be34a2e8118c14a616a64538e02430d9099d5d67d8a370f2888e4ac71e52bbb7")
    version("4.0.3", sha256="08caf41d21ae8f24afe79c664a34af1ed1e17aa5d4441cd9b1dc15f87bbbac95")
    version("3.1.3", sha256="353c7000a6563b16c0be0c6a04104d42b3154c5cd7c1979ab66efa5fdc5f5571")
    version("3.1.0", sha256="10c1fed4996a72c3e1e2bac1940334756894dbd116df3cc3b2d9743f2ae43016")

    depends_on("c", type="build")  # generated

    variant("jupyter", default=False, description="Support Jupyter/IPython magic", when="@4.1:")

    depends_on("py-setuptools", type="build")
    depends_on("py-ipython", when="+jupyter", type=("build", "run"))

    # Historical dependencies
    with when("@3"):
        depends_on("py-pytest-runner", type="build")
        depends_on("npm", type="build")
        depends_on("py-pyinstrument-cext@0.2.2:", type=("build", "run"))

    @property
    def skip_modules(self):
        if self.spec.satisfies("~jupyter"):
            return ["pyinstrument.magic"]
        return []
