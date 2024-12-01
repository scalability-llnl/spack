# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxy2cwl(PythonPackage):
    """Convert a Galaxy workflow to abstract Common Workflow Language (CWL)"""

    homepage = "https://github.com/workflowhub-eu/galaxy2cwl"
    url = "https://github.com/workflowhub-eu/galaxy2cwl/archive/refs/tags/0.1.4.tar.gz"

    license("BSD-3-Clause")

    version("0.1.4", sha256="ceb9024a7bf74c874be216c943cc97343563b1ec78f85fd3ec5b482c64350290")

    depends_on("py-setuptools", type="build")

    depends_on("py-pyyaml@5.3.0:", type=("build", "run"))
    depends_on("py-gxformat2@0.11.0:", type=("build", "run"))
