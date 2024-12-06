# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLogmuse(PythonPackage):
    """A small logging setup package."""

    homepage = "https://github.com/databio/logmuse/"
    pypi = "logmuse/logmuse-0.2.7.tar.gz"

    license("BSD-2-Clause")

    version("0.2.7", sha256="a4692c44ddfa912c3cb149ca4c7545f80119aa7485868fd1412e7c647e9a7e7e")

    depends_on("py-setuptools", type="build")
