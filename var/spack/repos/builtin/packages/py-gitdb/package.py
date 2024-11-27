# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGitdb(PythonPackage):
    """The GitDB project implements interfaces to allow read and write access
    to git repositories."""

    homepage = "https://gitdb.readthedocs.io"
    pypi = "gitdb/gitdb-4.0.5.tar.gz"

    license("BSD-3-Clause")

    version("4.0.9", sha256="bac2fd45c0a1c9cf619e63a90d62bdc63892ef92387424b855792a6cabe789aa")
    version("4.0.8", sha256="858966a9310649cb24a387c101429bb5a1110068a312517722b0281077e78bc6")
    version("4.0.7", sha256="96bf5c08b157a666fec41129e6d327235284cca4c81e92109260f353ba138005")
    version("4.0.6", sha256="42535bb16b5db8983e2c4f6a714d29a8feba7165a12addc63e08fc672dfeccb9")
    version("4.0.5", sha256="c9e1f2d0db7ddb9a704c2a0217be31214e91a4fe1dea1efad19ae42ba0c285c9")

    depends_on("python@3.4:", type=("build", "run"))
    depends_on("python@3.6:", type=("build", "run"), when="@4.0.8:")
    depends_on("py-setuptools", type="build")
    depends_on("py-smmap@3.0.1:3", type=("build", "run"), when="@:4.0.5")
    depends_on("py-smmap@3.0.1:4", type=("build", "run"), when="@4.0.6:4.0.7")
    depends_on("py-smmap@3.0.1:5", type=("build", "run"), when="@4.0.8:")
