# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAppdirs(PythonPackage):
    """A small Python module for determining appropriate platform-specific
    dirs, e.g. a "user data dir"."""

    homepage = "https://github.com/ActiveState/appdirs"
    pypi = "appdirs/appdirs-1.4.3.tar.gz"

    license("MIT")

    version("1.4.4", sha256="7d5d0167b2b1ba821647616af46a749d1c653740dd0d2415100fe26e27afdf41")
    version("1.4.3", sha256="9e5896d1372858f8dd3344faf4e5014d21849c756c8d5701f78f8a103b372d92")
    version("1.4.0", sha256="8fc245efb4387a4e3e0ac8ebcc704582df7d72ff6a42a53f5600bbb18fdaadc5")

    patch("setuptools-import.patch", when="@:1.4.0")
    patch("decode-appdirs.patch", when="@1.4.4")
    depends_on("py-setuptools", type="build")
