# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPygresql(PythonPackage):
    """PyGreSQL is an open-source Python module that interfaces to a
    PostgreSQL database"""

    homepage = "https://www.pygresql.org"
    url = "https://www.pygresql.org/files/PyGreSQL-5.0.5.tar.gz"

    version("5.0.5", sha256="ff5e76b840600d4912b79daf347b44274a1c0368663e7b57529c406f8426479c")

    depends_on("py-setuptools", type="build")
    depends_on("postgresql", type=("build", "run"))
