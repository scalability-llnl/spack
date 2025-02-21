# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyXClip(PythonPackage):
    """A concise but complete implementation of CLIP with various experimental
    improvements from recent papers"""

    homepage = "https://github.com/lucidrains/x-clip"
    pypi = "x-clip/x-clip-0.14.4.tar.gz"

    license("MIT", checked_by="alex391")

    version("0.14.4", sha256="e2539953f1c81a2ab892843c2bc02c218f4ac410cf10ce37495830f6a0e259c6")

    depends_on("py-setuptools", type="build")
    depends_on("py-beartype", type=("build", "run"))
    depends_on("py-einops@0.6:", type=("build", "run"))
    depends_on("py-ftfy", type=("build", "run"))
    depends_on("py-regex", type=("build", "run"))
    depends_on("py-torch@1.6:", type=("build", "run"))
    depends_on("py-torchvision", type=("build", "run"))
