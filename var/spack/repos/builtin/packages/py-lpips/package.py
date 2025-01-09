# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLpips(PythonPackage):
    """LPIPS Similarity metric"""

    homepage = "https://github.com/richzhang/PerceptualSimilarity"
    pypi = "lpips/lpips-0.1.4.tar.gz"

    license("BSD-2-Clause", checked_by="qwertos")

    version("0.1.4", sha256="3846331df6c69688aec3d300a5eeef6c529435bc8460bd58201c3d62e56188fa")

    depends_on("py-setuptools", type="build")
    depends_on("py-torch@0.4:", type=("build", "run"))
    depends_on("py-torchvision@0.2.1:", type=("build", "run"))
    depends_on("py-numpy@1.14.3:", type=("build", "run"))
    depends_on("py-scipy@1.0.1:", type=("build", "run"))
    depends_on("py-tqdm@4.28.1:", type=("build", "run"))
