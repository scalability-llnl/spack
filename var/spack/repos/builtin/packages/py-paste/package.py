# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPaste(PythonPackage):
    """Tools for using a Web Server Gateway Interface stack"""

    homepage = "https://pythonpaste.readthedocs.io"
    pypi = "Paste/Paste-3.5.2.tar.gz"

    license("MIT")

    version("3.5.2", sha256="d5a7340c30bcdf3023dd0106c8a5c430dd8fe84aeb8113bc7b93f8dd729f4af6")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type=("build", "run"))

    depends_on("py-six@1.4.0:", type=("build", "run"))
