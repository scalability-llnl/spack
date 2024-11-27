# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyAmpltools(PythonPackage):
    """This package includes tools to use with AMPL and amplpy."""

    homepage = "https://ampl.com/"
    pypi = "ampltools/ampltools-0.4.6.tar.gz"

    license("BSD-3-Clause")

    version("0.4.6", sha256="d54b399c1d78d02e3f4023aa2335b57832deb7d31cdefe4e219e4f2a2bb19a83")

    depends_on("py-requests", type=("build", "run"))
    depends_on("py-setuptools", type="build")
