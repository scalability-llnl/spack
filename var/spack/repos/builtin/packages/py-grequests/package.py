# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGrequests(PythonPackage):
    """GRequests allows you to use Requests with Gevent to make asynchronous
    HTTP Requests easily.

    Note: You should probably use requests-threads or requests-futures instead.
    """

    homepage = "https://github.com/spyoungtech/grequests"
    pypi = "grequests/grequests-0.4.0.tar.gz"

    version("0.4.0", sha256="8aeccc15e60ec65c7e67ee32e9c596ab2196979815497f85cf863465a1626490")
    version("0.3.0", sha256="0f41c4eee83bab39f5543af49665c08681637a0562a5704a3f7b2e4a996531c9")

    depends_on("py-setuptools", type="build")
    depends_on("py-gevent", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
