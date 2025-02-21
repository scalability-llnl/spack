# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Exprtk(Package):
    """ExprTk - C++ Mathematical Expression Toolkit Library"""

    homepage = "https://www.partow.net/programming/exprtk/index.html"
    url = "https://github.com/ArashPartow/exprtk/archive/refs/tags/0.0.3.tar.gz"
    git = "https://github.com/ArashPartow/exprtk.git"

    maintainers("arashpartow")

    license("MIT")

    depends_on("cxx", type="build")  # generated

    version("0.0.3", sha256="f9dec6975e86c702033d6a65ba9a0368eba31a61b89d74f2b5d24457c02c8439")
    version("0.0.2", sha256="7e8de4a0bfc9855c1316d8b8bc422061aef9a307c2f42d2e66298980463195c1")
    version("0.0.1", sha256="fb72791c88ae3b3426e14fdad630027715682584daf56b973569718c56e33f28")

    def install(self, prec, prefix):
        mkdirp(prefix.include.exprtk)
        install("exprtk.hpp", prefix.include.exprtk)
