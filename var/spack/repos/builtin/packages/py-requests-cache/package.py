# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyRequestsCache(PythonPackage):
    """A persistent HTTP cache that provides an easy way
    to get better performance with the python requests library.
    """

    homepage = "https://github.com/requests-cache/requests-cache"
    pypi = "requests-cache/requests_cache-0.9.7.tar.gz"

    license("BSD-2-Clause")

    version("0.9.7", sha256="b7c26ea98143bac7058fad6e773d56c3442eabc0da9ea7480af5edfc134ff515")

    depends_on("python@3.7:3", type=("build", "run"))
    depends_on("py-poetry-core@1.0.0:", type="build")

    depends_on("py-requests@2.22:", type=("build", "run"))
    depends_on("py-urllib3@1.25.5:", type=("build", "run"))
    depends_on("py-attrs@21.2:", type=("build", "run"))
    depends_on("py-cattrs@22.2:", type=("build", "run"))
    # depends_on("py-platformdirs@2.5:", type=("build", "run"))  # will be in future versions
    depends_on("py-url-normalize@1.4:", type=("build", "run"))
    depends_on("py-appdirs@1.4.4:", type=("build", "run"))
