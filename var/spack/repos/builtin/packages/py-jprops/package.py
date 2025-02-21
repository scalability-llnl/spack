# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJprops(PythonPackage):
    """Java properties file parser for Python"""

    homepage = "https://github.com/mgood/jprops/"
    pypi = "jprops/jprops-2.0.2.tar.gz"

    version("2.0.2", sha256="d297231833b6cd0a3f982a48fe148a7f9817f2895661743d166b267e4d3d5b2c")

    depends_on("py-setuptools", type="build")
