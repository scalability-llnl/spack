# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDisbatch(PythonPackage):
    """Dynamically distribute a list of tasks over a pool of compute resources."""

    homepage = "https://github.com/flatironinstitute/disBatch"
    pypi = "disbatch/disbatch-3.0.tar.gz"

    maintainers("lgarrison")

    license("Apache-2.0", checked_by="lgarrison")

    version("3.0", sha256="c7396319bfadfcc11dca578386725373e16acb653c76042d1ceb304255efa5ef")

    depends_on("python@3.9:", type=("build", "run"))

    depends_on("py-hatchling", type="build")
    depends_on("py-hatch-vcs", type="build")
