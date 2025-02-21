# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyee(PythonPackage):
    """A rough port of Node.js's EventEmitter to Python
    with a few tricks of its own."""

    homepage = "https://github.com/jfhbrook/pyee"
    pypi = "pyee/pyee-12.0.0.tar.gz"

    license("MIT", checked_by="wdconinc")

    version("12.0.0", sha256="c480603f4aa2927d4766eb41fa82793fe60a82cbfdb8d688e0d08c55a534e145")
    version("11.1.1", sha256="82e1eb1853f8497c4ff1a0c7fa26b9cd2f1253e2b6ffb93b4700fda907017302")

    depends_on("python@3.8:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-typing-extensions", type=("build", "run"))
