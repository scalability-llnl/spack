# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMdurl(PythonPackage):
    """Markdown URL utilities."""

    homepage = "https://github.com/executablebooks/mdurl"
    pypi = "mdurl/mdurl-0.1.2.tar.gz"

    license("MIT")

    version("0.1.2", sha256="bb413d29f5eea38f31dd4754dd7377d4465116fb207585f97bf925588687c1ba")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-flit-core@3.2:3", type="build")
