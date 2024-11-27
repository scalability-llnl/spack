# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySvgwrite(PythonPackage):
    """A Python library to create SVG drawings."""

    pypi = "svgwrite/svgwrite-1.1.12.zip"

    version("1.1.12", sha256="968c99f193f34f0fa7f0b3e82f49b93789c7c45cd89ce190480f16020d41ab79")

    depends_on("py-setuptools", type="build")
    depends_on("py-pyparsing@2.0.1:", type=("build", "run"))
