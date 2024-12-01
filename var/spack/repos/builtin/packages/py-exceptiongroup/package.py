# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyExceptiongroup(PythonPackage):
    """A backport of the BaseExceptionGroup and ExceptionGroup classes from Python 3.11."""

    homepage = "https://github.com/agronholm/exceptiongroup"
    pypi = "exceptiongroup/exceptiongroup-1.0.4.tar.gz"

    version("1.1.1", sha256="d484c3090ba2889ae2928419117447a14daf3c1231d5e30d0aae34f354f01785")
    version("1.0.4", sha256="bd14967b79cd9bdb54d97323216f8fdf533e278df937aa2a90089e7d6e06e5ec")

    depends_on("py-flit-scm", type="build")
