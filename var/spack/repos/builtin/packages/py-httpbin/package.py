# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHttpbin(PythonPackage):
    """HTTP Request and Response Service"""

    homepage = "https://github.com/Runscope/httpbin"
    pypi = "httpbin/httpbin-0.7.0.tar.gz"

    license("0BSD")

    version("0.7.0", sha256="cbb37790c91575f4f15757f42ad41d9f729eb227d5edbe89e4ec175486db8dfa")
    version("0.5.0", sha256="79fbc5d27e4194ea908b0fa18e09a59d95d287c91667aa69bcd010342d1589b5")

    depends_on("py-setuptools", type="build")
    depends_on("py-flask", type=("build", "run"))
    depends_on("py-markupsafe", type=("build", "run"))
    depends_on("py-decorator", type=("build", "run"))
    depends_on("py-itsdangerous", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-brotlipy", type=("build", "run"))
    depends_on("py-raven+flask", type=("build", "run"))
    depends_on("py-werkzeug@0.14.1:", type=("build", "run"))
