# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyomo(PythonPackage):
    """Pyomo is a Python-based open-source software package that supports a
    diverse set of optimization capabilities for formulating and analyzing
    optimization models."""

    homepage = "https://www.pyomo.org/"
    pypi = "Pyomo/Pyomo-5.6.6.tar.gz"
    git = "https://github.com/Pyomo/pyomo.git"

    # Maintainer accurate as of 2024-02-21
    maintainers("mrmundt")

    version("6.7.2", sha256="53bef766854f7607ca1fcfe3f218594ab382f137a275cee3d925d2b2f96876bf")
    version("6.7.1", sha256="735b66c45937f1caa43f073d8218a4918b6de658914a699397d38d5b8c219a40")
    version("6.7.0", sha256="a245ec609ef2fd907269f0b8e0923f74d5bf868b2ec0e62bf2a30b3f253bd17b")
    version("6.6.2", sha256="c8ad55213ff8b1a2c4e469110db8079722d5a6f364c6c46a42e2f750fc9e4d26")
    version("6.6.1", sha256="3fb0aba7b0f4120e6ce0f242502c0e61478d61e326bc90b7dc392bbefd114b34")
    version("6.6.0", sha256="8766c08041b8d91fbc5166d220c9e723fed6057d18be1178bae3b6583376c65e")
    version("6.5.0", sha256="5a23e775bba9fdbad22698fa1a841e662482edc979f2dea41cc6c54b1bb4b968")
    version("6.4.4", sha256="922dd8e6e3e421550acf884bd27f74cab2fe6552cdde36715d116b0c8345c367")
    version("6.4.3", sha256="7f3f67f61a6e5c2dd9c4dd930356d3176bad1572f1abee780592e725d6445288")
    version("6.4.2", sha256="6f5a867e77bdd6ac2ba0da5d4a251e38543ae05eba5a0c5cf8ab39e7fa8e1ea9")
    version("6.4.1", sha256="a636a3a1c8314b8be85899cb6fac5d6a9a78fc75c6d58b74d3ec106ae5ed8f59")
    version("6.4.0", sha256="b548825301b6bd4073a0620a8265d956153d53c12fca37cc7184fa54fce96222")
    version("6.3.0", sha256="b4df6305438a2b6ec75bd2e1588b919feb97089ed179a944b334432723781f81")
    version("6.2", sha256="89bc69a9a0afe10f5d229abe508b04ebbd3d2e213aa6c8ec2db2562798fa0400")
    version("6.1.2", sha256="f2a58977c3c72e706aef7ab7d016bdf66df85df8ea5b25cc0ba387e2cef880bb")
    version("6.1.1", sha256="32f378fda748ff299b4492b12b04ed1d8b11c857117fa0e5e6b609aa322fcade")
    version("6.1", sha256="7d087b186a43b2ffd032bc4db87cdbcf2fdc187607211f3e6cdc0f54b6f516f4")
    version("6.0.1", sha256="4b27bc917b12a6011e7eb3442a54619f0f42f1087d4defa14b903dd985fdbe7c")
    version("6.0", sha256="3dbfb1c7a8ef76dfd99d82c211845cdba9bf31a179269b57b6b28ad635ae34f9")
    version("5.7.3", sha256="2c4697107477a1b9cc9dad534d8f9c2dc6ee397c47ad44113e257732b83cfc8f")
    version("5.7.2", sha256="f10ada18ade84b16225dc519ef1788dd6d5f22cb22d0ea44db64c96d14cb7bb0")
    version("5.7.1", sha256="1228204d7eb4cdd217fed6323a7434de68e89a2aaa74085ea47f1b42fb64d8cd")
    version("5.7", sha256="27e3a3c8411de9bc52e5e6aa88e9a0de0dd7369126bc905996e23057775905d7")
    version("5.6.9", sha256="17bc3c15b405e3ba3a3b7cf9bf3867f6b8e57b611c8ecfdd43fd802587ee8bc6")
    version("5.6.8", sha256="28cbe034b06a477053616a3ce5ef43149bfd7d025cac490c2a3dd006c388b60d")
    version("5.6.7", sha256="fc97cc9d5a55c5185358ba65c1f9530c9af17e67a9aae7b36c3414f159030ae0")
    version("5.6.6", sha256="813e14a604b9d3ac63bdd0880c07f5f4e1b8f0a8a10345f1b42bee762219c001")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("cython", default=False, description="Enable cythonization of Pyomo.")
    variant("tests", default=False, description="Install testing dependencies.", when="@6.1:")
    variant(
        "docs", default=False, description="Install docs generation dependencies.", when="@6.1:"
    )
    variant("optional", default=False, description="Install optional dependencies.", when="@6.1:")

    ############################
    # UPDATE THESE AS REQUIRED
    ############################

    # python_requires
    depends_on("python@3.8:3.12", when="@6.7:", type=("build", "run"))
    depends_on("python@3.7:3.11", when="@6.4:6.6", type=("build", "run"))
    depends_on("python@3.6:3.10", when="@6.3", type=("build", "run"))
    depends_on("python@3.6:3.9", when="@6.0:6.2", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:3.9", when="@5.7", type=("build", "run"))
    depends_on("python@2.7:2.8,3.4:3.8", when="@5.6", type=("build", "run"))

    # universally required
    depends_on("py-setuptools@39.2:", type="build")
    depends_on("py-ply", type=("build", "run"))

    # required for pre-6 series
    depends_on("py-pyutilib@6.0.0", when="@5", type=("build", "run"))
    depends_on("py-six@1.4:", when="@5", type=("build", "run"))
    depends_on("py-appdirs", when="@5.6:5.7.0", type=("build", "run"))

    # when cython is requested
    depends_on("py-cython", when="+cython", type="build")

    # when tests is requested
    depends_on("py-coverage", when="@6.1:+tests", type=("run"))
    depends_on("py-nose", when="@6.1:6.2+tests", type=("run"))
    depends_on("py-pytest", when="@6.3:+tests", type=("run"))
    depends_on("py-pytest-parallel", when="@6.3:+tests", type=("run"))
    depends_on("py-parameterized", when="@6.1:+tests", type=("run"))
    depends_on("py-pybind11", when="@6.1:+tests", type=("run"))

    # when docs is requested
    depends_on("py-sphinx@3:", when="@:6.6+docs", type=("run"))
    depends_on("py-sphinx@5:", when="@6.7:+docs", type=("run"))
    depends_on("py-sphinx-copybutton", when="@6.1:+docs", type=("run"))
    depends_on("py-sphinx-rtd-theme@0.6:", when="@6.1:+docs", type=("run"))
    depends_on("py-sphinxcontrib-jsmath", when="@6.1:+docs", type=("run"))
    depends_on("py-sphinxcontrib-napoleon", when="@6.1:+docs", type=("run"))
    depends_on("py-sphinx-toolbox@2.16:", when="@6.7.1:+docs", type=("run"))
    depends_on("py-sphinx-jinja2-compat@0.1.1:", when="@6.7.1:+docs", type=("run"))
    depends_on("py-enum-tools", when="@6.7.1:+docs", type=("run"))
    # Pyomo does not support NumPy2 (May 9, 2024)
    depends_on("py-numpy@1", when="@6.1:+docs", type=("run"))
    depends_on("py-scipy", when="@6.4.2:+docs", type=("run"))

    # when optional is requested
    depends_on("py-dill", when="@6.1:+optional", type=("run"))
    depends_on("py-ipython", when="@6.1:+optional", type=("run"))
    depends_on("py-matplotlib@:3.6.0,3.6.2:", when="@6.1:+optional", type=("run"))
    depends_on("py-networkx", when="@6.1:+optional", type=("run"))
    # Pyomo does not support NumPy2 (May 9, 2024)
    depends_on("py-numpy@1", when="@6.1:+optional", type=("run"))
    depends_on("py-openpyxl", when="@6.1:+optional", type=("run"))
    depends_on("py-pint", when="@6.1:+optional", type=("run"))
    depends_on("py-plotly", when="@6.6:+optional", type=("run"))
    depends_on("py-python-louvain", when="@6.1:+optional", type=("run"))
    depends_on("py-pyyaml", when="@6.1:+optional", type=("run"))
    depends_on("py-qtconsole", when="@6.7.1:+optional", type=("run"))
    depends_on("py-scipy", when="@6.1:+optional", type=("run"))
    depends_on("py-sympy", when="@6.1:+optional", type=("run"))
    depends_on("py-xlrd", when="@6.1:+optional", type=("run"))
    depends_on("py-z3-solver", when="@6.1:+optional", type=("run"))
    depends_on("py-pywin32", when="@6.1:+optional platform=windows", type=("run"))
    depends_on("py-casadi", when="@6.1:+optional", type=("run"))
    depends_on("py-numdifftools", when="@6.1:+optional", type=("run"))
    depends_on("py-pandas", when="@6.1:+optional", type=("run"))
    depends_on("py-seaborn", when="@6.1:+optional", type=("run"))

    def global_options(self, spec, prefix):
        options = []
        if "+cython" in self.spec:
            options.append("--with-cython")
        return options
