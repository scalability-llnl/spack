# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBcolz(PythonPackage):
    """bcolz provides columnar and compressed data containers. Column
    storage allows for efficiently querying tables with a large number
    of columns. It also allows for cheap addition and removal of column.
    In addition, bcolz objects are compressed by default for reducing
    memory/disk I/O needs. The compression process is carried out internally
    by Blosc, a high-performance compressor that is optimized for binary data.
    """

    homepage = "https://github.com/Blosc/bcolz"
    pypi = "bcolz/bcolz-1.2.1.tar.gz"

    version("1.2.1", sha256="c017d09bb0cb5bbb07f2ae223a3f3638285be3b574cb328e91525b2880300bd1")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-setuptools@18.1:", type="build")
    depends_on("py-setuptools-scm@1.5.5:", type="build")
    depends_on("py-cython@0.22:", type="build")
