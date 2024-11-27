# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyZipstreamNew(PythonPackage):
    """Zipfile generator that takes input files as well as streams"""

    homepage = "https://github.com/arjan-s/python-zipstream"
    pypi = "zipstream-new/zipstream-new-1.1.8.tar.gz"

    version("1.1.8", sha256="b031fe181b94e51678389d26b174bc76382605a078d7d5d8f5beae083f111c76")

    depends_on("py-setuptools", type="build")
