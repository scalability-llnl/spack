# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyMyhdl(PythonPackage):
    """Python as a Hardware Description Language"""

    homepage = "https://www.myhdl.org"
    pypi = "myhdl/myhdl-0.9.0.tar.gz"

    license("LGPL-2.1-or-later")

    version("0.9.0", sha256="52d12a5fe2cda22558806272af3c2b519b6f7095292b8e6c8ad255fb604507a5")

    depends_on("c", type="build")  # generated

    depends_on("python@2.6:2.8,3.4:")
    depends_on("py-setuptools", type="build")
