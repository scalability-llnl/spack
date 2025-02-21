# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyArcp(PythonPackage):
    """arcp (Archive and Package) URI parser and generator"""

    homepage = "https://arcp.readthedocs.io"
    pypi = "arcp/arcp-0.2.1.tar.gz"

    license("Apache-2.0")

    version("0.2.1", sha256="5c17ac7972c9ef82979cc2caf2b3a87c1aefd3fefe9adb8a5dd728ada57715dd")

    depends_on("py-setuptools", type="build")
