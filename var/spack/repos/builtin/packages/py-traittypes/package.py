# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTraittypes(PythonPackage):
    """Custom trait types for scientific computing."""

    homepage = "http://ipython.org/"
    pypi = "traittypes/traittypes-0.2.1.tar.gz"

    license("BSD")

    version("0.2.1", sha256="be6fa26294733e7489822ded4ae25da5b4824a8a7a0e0c2dccfde596e3489bd6")

    depends_on("py-setuptools", type="build")
    depends_on("py-traitlets@4.2.2:", type=("build", "run"))
