# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBoomBootManager(PythonPackage):
    """Boom is a boot manager for Linux systems using boot loaders
    that support the BootLoader Specification for boot entry
    configuration."""

    homepage = "https://github.com/snapshotmanager/boom"
    url = "https://github.com/snapshotmanager/boom/archive/1.2.tar.gz"

    license("GPL-2.0-or-later")

    version("1.2", sha256="7e066caad5c91e7dd8475a5034e88bd0e8e6735aec412f904c0e93029b43ae47")
    version("1.1", sha256="0ddbfa914c1d997fae64833585eb6d781100ef32974c894ce2558cda6ce66d23")
    version("1.0", sha256="13f757e247f26959a9e64a0fbfcbf145881f299f892b164637b160089ae66a87")
    version("0.9", sha256="5876fe3d891547e61e059deaf5d2b7fe82e616087c6e5fcb28fe49ee79c68a2f")
    version("0.8.5", sha256="3137d59e1de1f026906ccc57f7510d6ea9e8092dc293da4ac5746e9b37fe35b8")

    depends_on("py-setuptools", type="build")
