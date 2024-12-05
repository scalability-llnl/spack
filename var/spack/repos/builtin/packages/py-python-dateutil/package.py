# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonDateutil(PythonPackage):
    """Extensions to the standard Python datetime module."""

    homepage = "https://dateutil.readthedocs.io/"
    pypi = "python-dateutil/python-dateutil-2.8.0.tar.gz"

    license("Apache-2.0")

    version("2.8.2", sha256="0123cacc1627ae19ddf3c27a5de5bd67ee4586fbdd6440d9748f8abb483d3e86")
    version("2.8.1", sha256="73ebfe9dbf22e832286dafa60473e4cd239f8592f699aa5adaf10050e6e1823c")
    version("2.8.0", sha256="c89805f6f4d64db21ed966fda138f8a5ed7a4fdbc1a8ee329ce1b74e3c74da9e")
    version("2.7.5", sha256="88f9287c0174266bb0d8cedd395cfba9c58e87e5ad86b2ce58859bc11be3cf02")
    version("2.5.2", sha256="063907ef47f6e187b8fe0728952e4effb587a34f2dc356888646f9b71fbb2e4b")
    version("2.4.2", sha256="3e95445c1db500a344079a47b171c45ef18f57d188dffdb0e4165c71bea8eb3d")
    version("2.4.0", sha256="439df33ce47ef1478a4f4765f3390eab0ed3ec4ae10be32f2930000c8d19f417")
    version("2.2", sha256="eec865307ebe7f329a6a9945c15453265a449cdaaf3710340828a1934d53e468")
    version("1.5", sha256="6f197348b46fb8cdf9f3fcfc2a7d5a97da95db3e2e8667cf657216274fe1b009")

    depends_on("python@2.7:2.8,3.3:", when="@2.7.5:", type=("build", "run"))
    depends_on("py-setuptools@24.3:", type="build")
    depends_on("py-setuptools-scm", type="build", when="@2.7.0:")
    depends_on("py-six@1.5:", when="@2:", type=("build", "run"))
