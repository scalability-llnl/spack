# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEmpy(PythonPackage):
    """A powerful and robust templating system for Python"""

    homepage = "http://www.alcyone.com/software/empy"
    pypi = "empy/empy-3.3.4.tar.gz"

    license("Ruby")

    version("3.3.4", sha256="73ac49785b601479df4ea18a7c79bc1304a8a7c34c02b9472cf1206ae88f01b3")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
