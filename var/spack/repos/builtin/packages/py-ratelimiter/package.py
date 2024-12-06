# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRatelimiter(PythonPackage):
    """Simple Python module providing rate limiting."""

    homepage = "https://github.com/RazerM/ratelimiter"
    pypi = "ratelimiter/ratelimiter-1.2.0.post0.tar.gz"

    maintainers("marcusboden")

    license("Apache-2.0")

    version(
        "1.2.0.post0", sha256="5c395dcabdbbde2e5178ef3f89b568a3066454a6ddc223b76473dac22f89b4f7"
    )

    depends_on("py-setuptools", type="build")
