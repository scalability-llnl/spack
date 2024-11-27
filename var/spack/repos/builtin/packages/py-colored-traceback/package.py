# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyColoredTraceback(PythonPackage):
    """Automatically color Python's uncaught exception tracebacks."""

    homepage = "https://github.com/staticshock/colored-traceback.py"
    pypi = "colored-traceback/colored-traceback-0.3.0.tar.gz"

    license("ISC")

    version("0.3.0", sha256="6da7ce2b1da869f6bb54c927b415b95727c4bb6d9a84c4615ea77d9872911b05")

    depends_on("py-setuptools", type="build")
    depends_on("py-pygments", type=("build", "run"))
