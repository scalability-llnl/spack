# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyProfilehooks(PythonPackage):
    """Python decorators for profiling/tracing/timing a single function"""

    homepage = "https://mg.pov.lt/profilehooks/"
    pypi = "profilehooks/profilehooks-1.11.2.tar.gz"

    git = "https://github.com/mgedmin/profilehooks.git"

    license("MIT")

    version("1.11.2", sha256="41a74c1abdc5eeaf7dec024e9e89627f70e158374d263a3098bef31a06d38ab2")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
