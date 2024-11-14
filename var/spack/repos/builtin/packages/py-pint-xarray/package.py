# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPintXarray(PythonPackage):
    """A convenience wrapper for using pint with xarray"""

    homepage = "https://github.com/xarray-contrib/pint-xarray"
    pypi = "pint-xarray/pint_xarray-0.4.tar.gz"

    license("Apache-2.0")

    version("0.4", sha256="b6b737a9c46dfb14a8598c27a71100496994c9d79dab61fd77f0d2685ae7065e")
    version("0.3", sha256="3545dfa78bee3f98eba29b8bd17500e3b5cb7c7b03a2c2781c4d4d59b6a82841")
    version("0.2.1", sha256="1ee6bf74ee7b52b946f226a96469276fa4f5c68f7381c1b2aae66852562cb275")

    with when("@0.4:"):
        depends_on("py-setuptools@64:", type="build")
        depends_on("py-setuptools-scm@7.0:+toml", type="build")
        depends_on("python@3.9:", type=("build", "run"))
        depends_on("py-numpy@1.23:", type=("build", "run"))
        depends_on("py-xarray@2022.06.0:", type=("build", "run"))
        depends_on("py-pint@0.21:", type=("build", "run"))

    with when("@:0.3"):
        depends_on("py-setuptools@42:", type="build")
        depends_on("py-setuptools-scm@3.4:+toml", type="build")
        depends_on("python@3.8:", type=("build", "run"))
        depends_on("py-numpy@1.17:", type=("build", "run"))
        depends_on("py-xarray@0.16.1:", type=("build", "run"))
        depends_on("py-pint@0.16:", type=("build", "run"))
        depends_on("py-importlib-metadata", when="@0.2.1 ^python@:3.7", type=("build", "run"))

    def url_for_version(self, version):

        if version >= Version("0.4"):
            return super().url_for_version(version)

        url = "https://files.pythonhosted.org/packages/source/p/pint-xarray/pint-xarray-{0}.tar.gz"
        return url.format(version)
