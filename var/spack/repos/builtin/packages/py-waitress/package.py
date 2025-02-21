# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWaitress(PythonPackage):
    """Waitress: a production-quality pure-Python WSGI server with very acceptable performance."""

    homepage = "https://github.com/Pylons/waitress/"
    pypi = "waitress/waitress-2.1.2.tar.gz"

    license("ZPL-2.1")

    version("3.0.1", sha256="ef0c1f020d9f12a515c4ec65c07920a702613afcad1dbfdc3bcec256b6c072b3")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2024-49769
        version("2.1.2", sha256="780a4082c5fbc0fde6a2fcfe5e26e6efc1e8f425730863c04085769781f51eba")

    depends_on("python@3.8:", type=("build", "run"), when="@3:")

    depends_on("py-setuptools@41:", type="build")
