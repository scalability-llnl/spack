# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyVstsCdManager(PythonPackage):
    """Python wrapper around some of the VSTS APIs."""

    homepage = "https://github.com/microsoft/vsts-cd-manager"
    pypi = "vsts-cd-manager/vsts-cd-manager-1.0.2.tar.gz"

    version("1.0.2", sha256="0bb09059cd553e1c206e92ef324cb0dcf92334846d646c44c684f6256b86447b")

    depends_on("py-setuptools", type="build")
    depends_on("py-msrest@0.2.0:", type=("build", "run"))
    depends_on("py-mock", type=("build", "run"))
