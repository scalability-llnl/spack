# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGcovr(PythonPackage):
    """Gcovr provides a utility for managing the use of the GNU gcov utility
    and generating summarized code coverage results. This command is inspired
    by the Python coverage.py package, which provides a similar utility for
    Python."""

    homepage = "https://gcovr.com/"
    pypi = "gcovr/gcovr-4.2.tar.gz"

    version("7.2", sha256="e3e95cb56ca88dbbe741cb5d69aa2be494eb2fc2a09ee4f651644a670ee5aeb3")
    version("5.2", sha256="217195085ec94346291a87b7b1e6d9cfdeeee562b3e0f9a32b25c9530b3bce8f")
    version("4.2", sha256="5aae34dc81e51600cfecbbbce3c3a80ce3f7548bc0aa1faa4b74ecd18f6fca3f")

    depends_on("python@3.8:", when="@7.2:", type=("build", "run"))
    depends_on("python@3.7:", when="@5.1:", type=("build", "run"))
    depends_on("python@3.6:", when="@5.0", type=("build", "run"))
    depends_on("python@2.7:2,3.5:", when="@:4", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-jinja2", type=("build", "run"))
    depends_on("py-lxml", type=("build", "run"))
    depends_on("py-pygments", when="@5:", type=("build", "run"))
    depends_on("py-pygments@2.13.0:", when="@7.2:", type=("build", "run"))
    depends_on("py-colorlog", when="@7.2:", type=("build", "run"))
    depends_on("py-tomli@1.1:", when="@7.2: ^python@:3.10", type=("build", "run"))
