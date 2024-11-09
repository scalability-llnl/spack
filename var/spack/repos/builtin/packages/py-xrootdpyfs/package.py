# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXrootdpyfs(PythonPackage):
    """XRootDPyFS is a PyFilesystem interface to XRootD."""

    homepage = "https://github.com/inveniosoftware/xrootdpyfs/"
    pypi = "xrootdpyfs/xrootdpyfs-0.2.2.tar.gz"

    version("0.2.2", sha256="43698c260f3ec52320c6bfac8dd3e7c2be7d28e9e9f58edf4f916578114e82bf")

    depends_on("py-setuptools", type="build")
    depends_on("py-fs@0.5.4:1", type=("build", "run"))
    depends_on("xrootd@4.8.4:4 +python", type=("build", "run"))
