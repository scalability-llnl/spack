# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAdbEnhanced(PythonPackage):
    """ADB-Enhanced is a Swiss-army knife for Android testing and
    development. A command-line interface to trigger various scenarios
    like screen rotation, battery saver mode, data saver mode, doze
    mode, permission grant/revocation."""

    homepage = "https://opencollective.com/ashishb"
    url = "https://github.com/ashishb/adb-enhanced/archive/2.5.4.tar.gz"

    license("Apache-2.0")

    version("2.5.10", sha256="9e913d09814ce99974c455a766c5b616a92bca551e657517d6e079882eb19bdb")
    version("2.5.4", sha256="329ee2e0cfceaa41c591398b365d9acdfd45ffe913c64ac06e1538041986fffb")
    version("2.5.3", sha256="5a1d5182d1a073b440e862e5481c7a21073eccc3cda7a4774a2aa311fee9bbdc")
    version("2.5.2", sha256="055676156c1566b8d952b9fdfdd89fc09f2d5d1e3b90b4cdf40858ce9947e2ca")

    depends_on("python@3:", type=("build", "run"))
    depends_on("python@3.4:", when="@2.5.10:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-docopt", type=("build", "run"))
    depends_on("py-future", when="@:2.5.4", type=("build", "run"))
    depends_on("py-psutil", type=("build", "run"))
    depends_on("py-asyncio", when="@:2.5.4", type=("build", "run"))
