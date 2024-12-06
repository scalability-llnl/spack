# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyperf(PythonPackage):
    """The Python perf module is a toolkit to write, run and
    analyze benchmarks.
    """

    homepage = "https://github.com/vstinner/pyperf"
    url = "https://github.com/vstinner/pyperf/archive/1.5.1.tar.gz"

    license("MIT")

    version("1.6.1", sha256="fbe793f6f2e036ab4dcca105b5c5aa34fd331dd881e7a3e158e5e218c63cfc32")
    version("1.6.0", sha256="7af7b9cfd9d26548ab7127f8e51791357ecd78cda46aad5b2d9664a70fc58878")
    version("1.5.1", sha256="9c271862bc2911be8eb01031a4a86cbc3f5bb615971514383802d3dcf46f18ed")

    depends_on("py-setuptools", type="build")
    depends_on("py-six", type=("build", "run"))
