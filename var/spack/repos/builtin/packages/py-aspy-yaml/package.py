# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAspyYaml(PythonPackage):
    """Some extensions to pyyaml."""

    homepage = "https://github.com/asottile/aspy.yaml/"
    pypi = "aspy.yaml/aspy.yaml-1.3.0.tar.gz"

    license("MIT")

    version("1.3.0", sha256="e7c742382eff2caed61f87a39d13f99109088e5e93f04d76eb8d4b28aa143f45")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
