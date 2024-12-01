# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetomiIsodatetime(PythonPackage):
    """Python ISO 8601 date time parser and data model/manipulation utilities."""

    homepage = "https://github.com/metomi/isodatetime"
    # NOTE: spack checksum does not yet work for epoch versions
    pypi = "metomi-isodatetime/metomi-isodatetime-1!3.0.0.tar.gz"

    maintainers("LydDeb")

    version("3.1.0", sha256="2ec15eb9c323d5debd0678f33af99bc9a91aa0b534ee5f65f3487aed518ebf2d")
    version("3.0.0", sha256="2141e8aaa526ea7f7f1cb883e6c8ed83ffdab73269658d84d0624f63a6e1357e")

    depends_on("py-setuptools", type="build")

    def url_for_version(self, version):
        return f"https://files.pythonhosted.org/packages/source/m/metomi-isodatetime/metomi-isodatetime-1!{version}.tar.gz"
