# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyVcstools(PythonPackage):
    """VCS/SCM source control library for svn, git, hg, and bzr."""

    homepage = "https://wiki.ros.org/vcstools"
    pypi = "vcstools/vcstools-0.1.42.tar.gz"

    version("0.1.42", sha256="9e48d8ed8b0fdda739af56e05bf10da1a509cb7d4950a19c73264c770802777a")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-python-dateutil", type=("build", "run"))
