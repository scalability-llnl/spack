# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonMultipart(PythonPackage):
    """A streaming multipart parser for Python"""

    homepage = "https://github.com/andrew-d/python-multipart"
    pypi = "python-multipart/python-multipart-0.0.5.tar.gz"

    license("Apache-2.0")

    version("0.0.17", sha256="41330d831cae6e2f22902704ead2826ea038d0419530eadff3ea80175aec5538")
    version("0.0.5", sha256="f7bb5f611fc600d15fa47b3974c8aa16e93724513b49b5f95c81e6624c83fa43")

    depends_on("py-setuptools", type="build", when="@:0.0.5")
    depends_on("py-hatchling", type="build", when="@0.0.6:")

    depends_on("py-six@1.4.0:", type=("build", "run"))

    def url_for_version(self, version):
        url = "https://files.pythonhosted.org/packages/source/p/python-multipart/{}-{}.tar.gz"
        if self.spec.satisfies("@:0.0.5"):
            name = "python-multipart"
        else:
            name = "python_multipart"
        return url.format(name, version)
