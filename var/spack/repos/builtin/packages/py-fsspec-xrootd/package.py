# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFsspecXrootd(PythonPackage):
    """An XRootD implementation for fsspec."""

    homepage = "https://coffeateam.github.io/fsspec-xrootd/"
    pypi = "fsspec_xrootd/fsspec_xrootd-0.4.0.tar.gz"

    maintainers("wdconinc")

    license("BSD-3-Clause", checked_by="wdconinc")

    version("0.4.0", sha256="d7f124430d26ab9139d33bc50fa8abfde3624db5dcaa5c18f56af9bf17f16f13")

    depends_on("python@3.8:", type=("build", "run"))

    depends_on("py-setuptools@42:", type="build")
    depends_on("py-setuptools-scm@3.4:+toml", type="build")

    depends_on("py-fsspec", type=("build", "run"))
