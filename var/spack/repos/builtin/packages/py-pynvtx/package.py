# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPynvtx(PythonPackage):
    """A thin python wrapper for the nvToolsExt (NVTX) library, using
    pybind11. This wrapper is meant to be as thin as possible -- so
    only provides minimal support. Currently supported features are:

    NVTX annotations: nvtxRangePushA and nvtxRangePop
    Function decorator: PyNVTX.annotate
    Automatic decorator generation PyNVTX.annotate_all_methods()"""

    homepage = "https://github.com/JBlaschke/PyNVTX"
    pypi = "PyNVTX/PyNVTX-0.3.3.tar.gz"

    maintainers("DaxLynch")

    version("0.3.3", sha256="8877b2d90bbf9d279d517a80a8f35a0a0a8179ebabf0729e806798a84bee6c72")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@40.8:", type="build")
    depends_on("py-pybind11", type=("build", "link", "run"))
