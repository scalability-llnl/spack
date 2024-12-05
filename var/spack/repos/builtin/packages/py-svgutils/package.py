# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySvgutils(PythonPackage):
    """Python tools to create and manipulate SVG files."""

    homepage = "https://github.com/btel/svg_utils"
    pypi = "svgutils/svgutils-0.3.4.tar.gz"

    license("MIT")

    version("0.3.4", sha256="9ef48f44cb1d460a7747dd02694200fda25eb9faf6dea392118def2695e0e053")
    version("0.3.1", sha256="cd52474765fd460ad2389947f77589de96142f6f0ce3f61e08ccfabeac2ff8af")

    depends_on("py-setuptools", type="build")
    depends_on("py-lxml", type=("build", "run"))
