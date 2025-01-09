# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLinkchecker(PythonPackage):
    """Check for broken links in web sites."""

    homepage = "https://linkchecker.github.io/linkchecker/"
    pypi = "LinkChecker/LinkChecker-10.5.0.tar.gz"

    maintainers("rbberger")

    license("GPL-2.0")

    version("10.5.0", sha256="978b42b803e58b7a8f6ffae1ff88fa7fd1e87b944403b5dc82380dd59f516bb9")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-requests@2.20:", type=("build", "run"))
    depends_on("py-dnspython@2:", type=("build", "run"))
    depends_on("py-beautifulsoup4@4.8.1:", type=("build", "run"))
    depends_on("py-hatchling@1.8.0:", type="build")
    depends_on("py-hatch-vcs", type="build")
    depends_on("py-setuptools-scm@7.1.0:", type="build")
