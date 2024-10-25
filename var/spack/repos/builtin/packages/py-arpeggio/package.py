# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyArpeggio(PythonPackage):
    """Packrat parser interpreter."""

    homepage = "https://github.com/textX/Arpeggio"
    pypi = "Arpeggio/Arpeggio-2.0.2.tar.gz"

    license("MIT")

    version("2.0.2", sha256="c790b2b06e226d2dd468e4fbfb5b7f506cec66416031fde1441cf1de2a0ba700")

    depends_on("py-setuptools", type="build")
