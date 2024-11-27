# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyNanotime(PythonPackage):
    """The nanotime module provides a time object that keeps time as the
    number of nanoseconds since the UNIX epoch. In other words, it is
    a 64bit UNIX timestamp with nanosecond precision.
    """

    homepage = "https://github.com/jbenet/nanotime"
    pypi = "nanotime/nanotime-0.5.2.tar.gz"

    license("MIT")

    version("0.5.2", sha256="c7cc231fc5f6db401b448d7ab51c96d0a4733f4b69fabe569a576f89ffdf966b")

    depends_on("py-setuptools", type="build")
