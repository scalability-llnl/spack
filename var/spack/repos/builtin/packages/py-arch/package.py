# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArch(PythonPackage):
    """Autoregressive Conditional Heteroskedasticity (ARCH) and other tools
    for financial econometrics, written in Python (with Cython and/or Numba
    used to improve performance)"""

    homepage = "https://pypi.org/project/arch"
    pypi = "arch/arch-7.0.0.tar.gz"
    git = "https://github.com/bashtage/arch.git"

    maintainers("climbfuji")

    license("NCSA", checked_by="climbfuji")

    version("7.0.0", sha256="353c0dba5242287b8b6b587a70250d788436630bf3b7ef6106f577e45d1ec247")

    variant("numba", default=False, description="Enable numba backend")
    variant("tutorial", default=True, description="Include dependencies for online tutorials")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools@0.61:", type="build")
    depends_on("py-setuptools-scm@8.0.3:8 +toml", type="build")
    depends_on("py-cython@3.0.10:", type="build")
    # https://github.com/bashtage/arch/blob/9ced09e2566c0ebcad962d2441b1e79e2aaa7c9f/pyproject.toml#L59
    # "numpy>=2.0.0rc1,<3" ???
    # https://github.com/bashtage/arch/blob/9ced09e2566c0ebcad962d2441b1e79e2aaa7c9f/requirements.txt#L1
    # numpy>=1.22.3 ???
    depends_on("py-numpy@1.22.3", type=("build", "run"))

    depends_on("py-scipy@1.8:", type="run")
    depends_on("py-pandas@1.4:", type="run")
    depends_on("py-statsmodels@0.12:", type="run")
    depends_on("py-matplotlib@3:", type="run")
    depends_on("py-numba@0.49:", type="run", when="+numba")

    # Note. py-arch does not depend on py-pandas-datareader,
    # but all examples in the py-arch documentation use it.
    depends_on("py-pandas-datareader@0.10:", type="run", when="+tutorial")
