# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWincertstore(PythonPackage):
    """wincertstore provides an interface to access Windows' CA and CRL certificates.
    It uses ctypes and Windows's sytem cert store API through crypt32.dll."""

    homepage = "https://github.com/tiran/wincertstore"
    pypi = "wincertstore/wincertstore-0.2.zip"

    license("PSF-2.0")

    version("0.2", sha256="780bd1557c9185c15d9f4221ea7f905cb20b93f7151ca8ccaed9714dce4b327a")

    depends_on("py-setuptools", type="build")
