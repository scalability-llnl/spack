# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyTblib(PythonPackage):
    """Traceback fiddling library. Allows you to pickle tracebacks."""

    homepage = "https://github.com/ionelmc/python-tblib"
    pypi = "tblib/tblib-1.6.0.tar.gz"

    license("BSD-2-Clause")

    version("1.6.0", sha256="229bee3754cb5d98b4837dd5c4405e80cfab57cb9f93220410ad367f8b352344")
    version("1.4.0", sha256="bd1ad564564a158ff62c290687f3db446038f9ac11a0bf6892712e3601af3bcd")

    depends_on("python@2.7:2.8,3.5:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
