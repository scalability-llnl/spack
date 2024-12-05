# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyrect(PythonPackage):
    """PyRect is a simple module with a Rect class for
    Pygame-like rectangular areas."""

    homepage = "https://github.com/asweigart/pyrect"
    pypi = "PyRect/PyRect-0.1.4.tar.gz"

    version("0.1.4", sha256="3b2fa7353ce32a11aa6b0a15495968d2a763423c8947ae248b92c037def4e202")

    depends_on("py-setuptools", type="build")
