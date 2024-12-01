# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJinja2Time(PythonPackage):
    """Jinja2 Extension for Dates and Times"""

    homepage = "https://github.com/hackebrot/jinja2-time"
    url = "https://github.com/hackebrot/jinja2-time/archive/0.2.0.tar.gz"

    license("MIT")

    version("0.2.0", sha256="0e647e525ba47523fa400a58fdec090b1cc6dcec4afbf095ee01e9e589e5a5ef")

    depends_on("py-setuptools", type="build")
    depends_on("py-arrow")
    depends_on("py-jinja2")
