# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

from spack.package import *


class PyDotnetcore2(PythonPackage):
    """.Net Core 2.1 runtime."""

    homepage = "https://github.com/dotnet/core"

    skip_version_audit = ["platform=windows"]

    if sys.platform == "darwin":
        version(
            "2.1.14",
            sha256="68182f4b704db401b2012c10ed8a19561f8d487063632f8731c2e58960ca9242",
            url="https://pypi.io/packages/py3/d/dotnetcore2/dotnetcore2-2.1.14-py3-none-macosx_10_9_x86_64.whl",
        )
    elif sys.platform.startswith("linux"):
        version(
            "2.1.14",
            sha256="d8d83ac30c22a0e48a9a881e117d98da17f95c4098cb9500a35e323b8e4ab737",
            url="https://pypi.io/packages/py3/d/dotnetcore2/dotnetcore2-2.1.14-py3-none-manylinux1_x86_64.whl",
        )

    conflicts("target=ppc64:", msg="py-dotnetcore2 is only available for x86_64")
    conflicts("target=ppc64le:", msg="py-dotnetcore2 is only available for x86_64")
    conflicts("target=aarch64:", msg="py-dotnetcore2 is only available for x86_64")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-distro@1.2.0:", type=("build", "run"))
