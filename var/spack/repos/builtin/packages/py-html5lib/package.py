# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHtml5lib(PythonPackage):
    """HTML parser based on the WHATWG HTML specification."""

    homepage = "https://github.com/html5lib/html5lib-python"
    pypi = "html5lib/html5lib-1.1.tar.gz"

    license("MIT")

    version("1.1", sha256="b2e5b40261e20f354d198eae92afc10d750afb487ed5e50f9c4eaf07c184146f")
    version("1.0.1", sha256="66cb0dcfdbbc4f9c3ba1a63fdb511ffdbd4f513b2b6d81b80cd26ce6b3fb3736")
    version("0.99", sha256="aff6fd3031c563883197e5a04b7df324086ff5f358278a0386808c463a077e59")

    depends_on("py-six", type=("build", "run"))
    depends_on("py-six@1.9:", type=("build", "run"), when="@1.0.1:")
    depends_on("py-setuptools", type="build", when="@1.0.1:")
    depends_on("py-webencodings", type=("build", "run"), when="@1.0.1:")
