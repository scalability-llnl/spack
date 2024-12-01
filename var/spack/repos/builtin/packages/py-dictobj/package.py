# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDictobj(PythonPackage):
    """A set of Python dictionary objects where keys can be accessed as instance attributes."""

    homepage = "https://github.com/grimwm/py-dictobj"
    pypi = "dictobj/dictobj-0.4.tar.gz"

    license("Apache-2.0")

    version("0.4", sha256="15d6ac1c720350dcce3d01c31882cbc8e4a14cb22a8bca290a18ca7b0c0988f1")

    depends_on("py-setuptools", type="build")
