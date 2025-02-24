# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEventlet(PythonPackage):
    """Concurrent networking library for Python"""

    homepage = "https://github.com/eventlet/eventlet"
    url = "https://github.com/eventlet/eventlet/archive/refs/tags/v0.22.0.tar.gz"

    license("MIT")

    version("0.22.0", sha256="c4cc92268b82eb94d5e0de0592159157d68122d394f480e3f9a9d6ddb695655e")

    depends_on("py-setuptools", type="build")
    depends_on("py-greenlet@0.3:")
