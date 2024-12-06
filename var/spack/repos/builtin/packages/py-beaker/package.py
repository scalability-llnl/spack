# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyBeaker(PythonPackage):
    """Beaker is a web session and general caching library
    that includes WSGI middleware for use in web applications.
    """

    homepage = "https://beaker.readthedocs.io"
    pypi = "Beaker/Beaker-1.12.0.tar.gz"

    license("BSD-3-Clause")

    version("1.12.0", sha256="2d5f427e3b13259c98c934cab0e428fc1c18a4c4b94acbdae930df7e7f51d1ec")
    version("1.11.0", sha256="ad5d1c05027ee3be3a482ea39f8cb70339b41e5d6ace0cb861382754076d187e")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
