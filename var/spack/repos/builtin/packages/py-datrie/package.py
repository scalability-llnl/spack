# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDatrie(PythonPackage):
    """Super-fast, efficiently stored Trie for Python (2.x and 3.x). Uses libdatrie."""

    pypi = "datrie/datrie-0.8.2.tar.gz"
    maintainers("marcusboden")

    license("LGPL-2.1-or-later")

    version("0.8.2", sha256="525b08f638d5cf6115df6ccd818e5a01298cd230b2dac91c8ff2e6499d18765d")

    depends_on("c", type="build")  # generated

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools@40.8:", type=("build"))
    depends_on("py-cython@0.28:", type="build")
    depends_on("py-pytest-runner", type="build")

    @when("@:0.8.2")
    def patch(self):
        # fix failure to compile on gcc-14, https://github.com/pytries/datrie/pull/99
        filter_file(r"(\s*)(struct AlphaMap:)", r"\1ctypedef \2", "src/cdatrie.pxd")
