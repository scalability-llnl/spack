# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyYacs(PythonPackage):
    """YACS was created as a lightweight library to define and manage
    system configurations, such as those commonly found in software
    designed for scientific experimentation."""

    homepage = "https://github.com/rbgirshick/yacs"
    pypi = "yacs/yacs-0.1.8.tar.gz"

    version("0.1.8", sha256="efc4c732942b3103bea904ee89af98bcd27d01f0ac12d8d4d369f1e7a2914384")
    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))
