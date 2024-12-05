# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySend2trash(PythonPackage):
    """Python library to send files to Trash/Recycle on all platforms."""

    homepage = "https://github.com/hsoft/send2trash"
    url = "https://github.com/hsoft/send2trash/archive/1.5.0.tar.gz"

    license("BSD-3-Clause")

    version("1.8.3", sha256="90bcdf2ed2a18b687040c0f58bfccd6ad2e1b7ec495a9903119dc3c47c615052")
    version("1.8.0", sha256="937b038abd9f1e7b8c5d7a116be5dc4663beb71df74dcccffe56cacf992c7a9c")
    version("1.5.0", sha256="7cebc0ffc8b6d6e553bce9c6bb915614610ba2dec17c2f0643b1b97251da2a41")

    depends_on("py-setuptools", type="build")
