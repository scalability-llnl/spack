# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyKrb5(PythonPackage):
    """Kerberos API bindings for Python."""

    homepage = "https://github.com/jborean93/pykrb5"
    pypi = "krb5/krb5-0.6.0.tar.gz"

    maintainers("wdconinc")

    license("MIT", checked_by="wdconinc")

    version("0.7.0", sha256="6a308f2e17d151c395b24e6aec7bdff6a56fe3627a32042fc86d412398a92ddd")
    version("0.6.0", sha256="712ba092fbe3a28ec18820bb1b1ed2cc1037b75c5c7033f970c6a8c97bbd1209")

    depends_on("python@3.8:", type=("build", "run"), when="@0.7.0:")
    depends_on("py-setuptools@42:", type="build")
    depends_on("py-cython@0.29.32:3", type=("build", "run"))
    depends_on("krb5", type=("build", "run"))
