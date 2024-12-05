# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHeapdict(PythonPackage):
    """A heap with decrease-key and increase-key operations"""

    homepage = "http://stutzbachenterprises.com/"
    pypi = "HeapDict/HeapDict-1.0.1.tar.gz"

    version("1.0.1", sha256="8495f57b3e03d8e46d5f1b2cc62ca881aca392fd5cc048dc0aa2e1a6d23ecdb6")
    version("1.0.0", sha256="40c9e3680616cfdf942f77429a3a9e0a76f31ce965d62f4ffbe63a83a5ef1b5a")

    depends_on("python@2.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
