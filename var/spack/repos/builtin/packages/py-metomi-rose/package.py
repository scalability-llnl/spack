# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetomiRose(PythonPackage):
    """Rose, a framework for meteorological suites."""

    homepage = "https://metomi.github.io/rose/doc/html/index.html"
    pypi = "metomi-rose/metomi-rose-2.1.0.tar.gz"

    maintainers("LydDeb")

    license("GPL-3.0-only")

    version("2.1.0", sha256="1b60135a434fe4325d364a57e8f5e81e90f39b373b9d68733458c1adc2513c05")

    depends_on("fortran", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-aiofiles", type=("build", "run"))
    depends_on("py-jinja2@2.10.1:", type=("build", "run"))
    depends_on("py-keyring@23", type=("build", "run"))
    depends_on("py-ldap3", type=("build", "run"))
    depends_on("py-metomi-isodatetime@3", type=("build", "run"))
    depends_on("py-psutil@5.6.0:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-sqlalchemy@1", type=("build", "run"))
