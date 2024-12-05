# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTextwrap3(PythonPackage):
    """textwrap from Python 3.6 backport (plus a few tweaks)."""

    homepage = "https://github.com/jonathaneunice/textwrap3"
    pypi = "textwrap3/textwrap3-0.9.2.zip"

    version("0.9.2", sha256="5008eeebdb236f6303dcd68f18b856d355f6197511d952ba74bc75e40e0c3414")

    depends_on("py-setuptools", type="build")
