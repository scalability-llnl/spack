# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyCpuinfo(PythonPackage):
    """Get CPU info with pure Python 2 & 3"""

    homepage = "https://github.com/workhorsy/py-cpuinfo"
    pypi = "py-cpuinfo/py-cpuinfo-0.2.3.tar.gz"

    license("MIT")

    version("9.0.0", sha256="3cdbbf3fac90dc6f118bfd64384f309edeadd902d7c8fb17f02ffa1fc3f49690")
    version("8.0.0", sha256="5f269be0e08e33fd959de96b34cd4aeeeacac014dd8305f70eb28d06de2345c5")
    version("6.0.0", sha256="7ffb31dea845b9f359b99bd5f7eea72dc70f852e0e34547d261a630f2b8c9c61")
    version("0.2.3", sha256="f6a016fdbc4e7fadf2d519090fcb4fa9d0831bad4e85245d938e5c2fe7623ca6")

    depends_on("py-setuptools", type="build")
