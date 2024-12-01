# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRbtools(PythonPackage):
    """RBTools is a set of command line tools and a rich Python API for
    use with Review Board."""

    homepage = "https://github.com/reviewboard/rbtools"
    url = "https://github.com/reviewboard/rbtools/archive/release-1.0.2.tar.gz"

    license("MIT")

    version("1.0.2", sha256="dd7aa95691be91f394d085120e44bcec3dc440b01a8f7e2742e09a8d756c831c")
    version("1.0.1", sha256="bc5e3c511a2273ec61c43a82f56b4cef0b23beae81e277cecbb37ce6761edf29")
    version("1.0", sha256="dbab2cc89d798462c7e74952d43ba1ff1c97eb9c8f92876e600c6520f72454c9")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))
    depends_on("py-colorama", type=("build", "run"))
    depends_on("py-texttable", type=("build", "run"))
    depends_on("py-tqdm", type=("build", "run"))
    depends_on("py-six@1.8.0:", type=("build", "run"))
