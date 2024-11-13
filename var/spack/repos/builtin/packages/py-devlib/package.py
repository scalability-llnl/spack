# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDevlib(PythonPackage):
    """Library for interaction with and instrumentation of remote devices."""

    homepage = "https://github.com/ARM-software/devlib"
    url = "https://github.com/ARM-software/devlib/archive/v1.2.tar.gz"

    license("Apache-2.0")

    version("1.2", sha256="4cdb6767a9430b49eecffe34e2b9fcbcfc7e65328122d909aa71c3d11a86503d")
    version("1.1.2", sha256="c900420cb97239b4642f5e333e43884fb09507b530edb55466e7b82103b4deaa")
    version("1.1.1", sha256="eceb7a2721197a6023bbc2bbf346663fc117e4f54e1eb8334a3085dead9c8036")
    version("1.1.0", sha256="317e9be2303ebb6aebac9a2ec398c622ea16d6e46079dc9e37253b37d739ca9d")
    version("1.0.0", sha256="2f78278bdc9731a4fa13c41c74f08e0b8c5143de5fa1e1bdb2302673aec45862")
    version("0.0.4", sha256="0f55e684d43fab759d0e74bd8f0d0260d9546a8b8d853d286acfe5e00c86da05")
    version("0.0.3", sha256="29ec5f1de481783ab0b9efc111dfeb67c890187d56fca8592b25ee756ff32902")
    version("0.0.2", sha256="972f33be16a06572a19b67d909ee0ed6cb6f21f9a9da3c43fd0ff5851421051d")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil", type=("build", "run"))
    depends_on("py-pexpect@3.3:", type=("build", "run"))
    depends_on("py-pyserial", type=("build", "run"))
    depends_on("py-wrapt", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
