# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDefusedxml(PythonPackage):
    """defusing XML bombs and other exploits"""

    homepage = "https://github.com/tiran/defusedxml"
    pypi = "defusedxml/defusedxml-0.5.0.tar.gz"

    license("PSF-2.0")

    version("0.7.1", sha256="1bb3032db185915b62d7c6209c5a8792be6a32ab2fedacc84e01b52c51aa3e69")
    version("0.6.0", sha256="f684034d135af4c6cbb949b8a4d2ed61634515257a67299e5f940fbaa34377f5")
    version("0.5.0", sha256="24d7f2f94f7f3cb6061acb215685e5125fbcdc40a857eff9de22518820b0a4f4")

    depends_on("py-setuptools", type="build")
    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
