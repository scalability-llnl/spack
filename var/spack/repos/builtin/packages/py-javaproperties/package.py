# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyJavaproperties(PythonPackage):
    """Read & write Java .properties files."""

    homepage = "https://github.com/jwodder/javaproperties"
    pypi = "javaproperties/javaproperties-0.7.0.tar.gz"

    license("MIT")

    version("0.7.0", sha256="cf45b39fcbaeced1dfc0b7f2bda16e34fc0349116269e001dada42fd2e145d87")
    version("0.5.1", sha256="2b0237b054af4d24c74f54734b7d997ca040209a1820e96fb4a82625f7bd40cf")

    depends_on("python@2.7:2.8,3.4:3", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-six@1.4:1", type=("build", "run"))
