# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySeaborn(PythonPackage):
    """Seaborn: statistical data visualization.

    Seaborn is a library for making attractive and informative statistical
    graphics in Python. It is built on top of matplotlib and tightly
    integrated with the PyData stack, including support for numpy and pandas
    data structures and statistical routines from scipy and statsmodels."""

    homepage = "https://seaborn.pydata.org/"
    pypi = "seaborn/seaborn-0.7.1.tar.gz"

    license("BSD-2-Clause")

    version("0.13.2", sha256="93e60a40988f4d65e9f4885df477e2fdaff6b73a9ded434c1ab356dd57eefff7")
    version("0.12.2", sha256="374645f36509d0dcab895cba5b47daf0586f77bfe3b36c97c607db7da5be0139")
    version("0.12.0", sha256="893f17292d8baca616c1578ddb58eb25c72d622f54fc5ee329c8207dc9b57b23")
    version("0.11.2", sha256="cf45e9286d40826864be0e3c066f98536982baf701a7caa386511792d61ff4f6")
    version("0.11.1", sha256="44e78eaed937c5a87fc7a892c329a7cc091060b67ebd1d0d306b446a74ba01ad")
    version("0.9.0", sha256="76c83f794ca320fb6b23a7c6192d5e185a5fcf4758966a0c0a54baee46d41e2f")
    version("0.7.1", sha256="fa274344b1ee72f723bab751c40a5c671801d47a29ee9b5e69fcf63a18ce5c5d")

    variant("stats", default=False, description="Optional statistical dependencies", when="@0.12:")

    depends_on("python@3.6:", when="@0.10:", type="build")
    depends_on("python@3.7:", when="@0.12:", type="build")
    depends_on("py-setuptools", when="@:0.11.2", type="build")
    depends_on("py-flit-core@3.2:3", when="@0.12.0:", type="build")

    depends_on("py-numpy@1.17:1.23,1.24.1:", when="@0.12.2:", type=("build", "run"))
    depends_on("py-numpy@1.17:", when="@0.12:", type=("build", "run"))
    depends_on("py-numpy@1.15:", when="@0.11:", type=("build", "run"))
    depends_on("py-numpy@1.9.3:", when="@0.9:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    # https://github.com/mwaskom/seaborn/pull/3683
    depends_on("py-numpy@:1", when="@:0.13.1", type=("build", "run"))
    depends_on("py-pandas@0.25:", when="@0.12:", type=("build", "run"))
    depends_on("py-pandas@0.23:", when="@0.11:", type=("build", "run"))
    depends_on("py-pandas@0.22:", when="@0.10:", type=("build", "run"))
    depends_on("py-pandas@0.15.2:", when="@0.9:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-matplotlib@3.1:3.6.0,3.6.2:", when="@0.12.2:", type=("build", "run"))
    depends_on("py-matplotlib@3.1:", when="@0.12:", type=("build", "run"))
    depends_on("py-matplotlib@2.2:", when="@0.11:", type=("build", "run"))
    depends_on("py-matplotlib@2.1.2:", when="@0.10:", type=("build", "run"))
    depends_on("py-matplotlib@1.4.3:", when="@0.9:", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))

    depends_on("py-scipy@1.3:", when="@0.12.2: +stats", type=("build", "run"))
    depends_on("py-scipy@1:", when="@0.12: +stats", type=("build", "run"))
    depends_on("py-scipy@1:", when="@0.11", type=("build", "run"))
    depends_on("py-scipy@1.0.1:", when="@0.10:0.11", type=("build", "run"))
    depends_on("py-scipy@0.14:", when="@0.9.0:0.11", type=("build", "run"))
    depends_on("py-scipy", when="@:0.11", type=("build", "run"))

    depends_on("py-statsmodels@0.10:", when="@0.12: +stats", type=("build", "run"))

    depends_on("py-typing-extensions", when="@0.12: ^python@:3.7", type=("build", "run"))
