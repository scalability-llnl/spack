# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRadicalSaga(PythonPackage):
    """RADICAL-SAGA (RS) implements the interface specification of the Open
    Grid Forum (OGF) Simple API for Grid Applications (SAGA) standard. RS works
    as a light-weight access layer for distributed computing infrastructures,
    providing adaptors for different middleware systems and services."""

    homepage = "https://radical-cybertools.github.io"
    git = "https://github.com/radical-cybertools/radical.saga.git"
    pypi = "radical_saga/radical_saga-1.90.0.tar.gz"

    maintainers("andre-merzky")

    license("MIT")

    version("develop", branch="devel")
    version("1.90.0", sha256="55758339f58087477574ed598e5a34cb99d045a540a74ba9e11b34eead4af78d")

    version(
        "1.47.0",
        sha256="fc9a8fc060e708852ce6c40b08a65111f8d72b9ad5f8afef9ceaa866c1351233",
        deprecated=True,
    )
    version(
        "1.39.0",
        sha256="0fea8103d3f96c821c977bcb55ff1c6a9844de727539b182dda4cbc2570df791",
        deprecated=True,
    )

    depends_on("py-radical-utils@1.90:1.99", type=("build", "run"), when="@1.90:")
    depends_on("py-radical-utils@1.40:1.52", type=("build", "run"), when="@1.40:1.52")
    depends_on("py-radical-utils@1.39", type=("build", "run"), when="@1.39")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@:1.52")

    depends_on("py-apache-libcloud", type=("build", "run"), when="@:1.60")
    depends_on("py-parse", type=("build", "run"))
    depends_on("py-setuptools", type="build")
