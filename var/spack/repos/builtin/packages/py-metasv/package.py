# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMetasv(PythonPackage):
    """An accurate and integrative structural-variant caller for next
    generation sequencing"""

    homepage = "https://bioinform.github.io/metasv/"
    url = "https://github.com/bioinform/metasv/archive/0.5.4.tar.gz"

    license("BSD-2-Clause")

    version("0.5.4", sha256="c8613b56f44b9303b9e126618b2aee9dbc0b26c03d14e70e1aeed918582eeec1")

    depends_on("py-pybedtools@0.6.9", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-pyvcf", type=("build", "run"))
    depends_on("py-setuptools", type="build")
