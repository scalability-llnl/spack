# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyApacheLibcloud(PythonPackage):
    """Python library for multiple cloud provider APIs"""

    homepage = "https://libcloud.apache.org"
    pypi = "apache-libcloud/apache-libcloud-1.2.1.tar.gz"

    license("Apache-2.0")

    version("1.2.1", sha256="b26b542c6c9785dd4e34892d87421ffa4c043335c1cba301a97a8d9748c423f2")

    depends_on("py-setuptools", type="build")
