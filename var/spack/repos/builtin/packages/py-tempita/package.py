# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTempita(PythonPackage):
    """A very small text templating language"""

    homepage = "https://pypi.org/project/Tempita"
    pypi = "tempita/Tempita-0.5.2.tar.gz"

    license("MIT")

    version("0.5.2", sha256="cacecf0baa674d356641f1d406b8bff1d756d739c46b869a54de515d08e6fc9c")

    depends_on("py-setuptools", type="build")
