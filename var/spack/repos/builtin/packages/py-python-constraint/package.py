# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonConstraint(PythonPackage):
    """Constraint Solving Problem resolver for Python"""

    homepage = "https://github.com/python-constraint/python-constraint"
    pypi = "python-constraint/python-constraint-1.4.0.tar.bz2"

    version("1.4.0", sha256="501d6f17afe0032dfc6ea6c0f8acc12e44f992733f00e8538961031ef27ccb8e")

    depends_on("py-setuptools", type="build")
