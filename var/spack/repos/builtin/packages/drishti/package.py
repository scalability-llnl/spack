# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Drishti(PythonPackage):
    """
    Drishti is a command-line tool to guide end-users in optimizing I/O in their applications
    by detecting typical I/O performance pitfalls and providing a set of recommendations.
    """

    homepage = "https://github.com/hpc-io/drishti-io"
    git = "https://github.com/hpc-io/drishti-io"
    pypi = "drishti-io/drishti-io-0.4.tar.gz"

    maintainers("jeanbez", "sbyna")

    license("BSD-3-Clause-LBNL")

    version("master", branch="master")

    version("0.4", sha256="bbbb272b4f6f44ae762f6cba28a2c589e15608691c559af0cc2f552590335d7b")

    depends_on("c", type="build")  # generated

    depends_on("darshan-util", type=("run"))

    depends_on("python@3.6:", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-rich@12.5.1", type=("build", "run"))
    depends_on("py-darshan", type=("build", "run"))
