# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPybedtools(PythonPackage):
    """Python wrapper -- and more -- for Aaron Quinlan's BEDTools"""

    homepage = "https://daler.github.io/pybedtools"
    pypi = "pybedtools/pybedtools-0.9.0.tar.gz"

    license("MIT")

    version("0.10.0", sha256="1a6fbaad23b013becc741d7d5922a2df03e391bc44ff92772ffb7dd456711161")
    version("0.9.0", sha256="9267c92cd764173449d9c31baedac0659b4eccc3d7c05e22ec378f86c0fc30a3")
    version("0.8.0", sha256="4eebd2cd1764ee1c604fd881703c3e329195485350b987b7fb8db42d232984f6")
    version("0.7.10", sha256="518a2311bd33f29cf2ee8fc1a028dda8c8e380c9fc83fcb0fbaa206933174b50")
    version("0.7.9", sha256="e9134d7dc3de41b90126df633fe3aa854a0427d7ada834dc8681081e8b2fea14")
    version("0.7.8", sha256="e80e8b73b233ec6950069e0e1cf14127aff8310a8eaf3ee663bdfbcb61309fdc")
    version("0.7.7", sha256="dba8758bd86121e4dcfc8b25ebae7d3b2de6ff9e38e4cdd9dc03f128bf5d4c9d")
    version("0.7.6", sha256="8b6382036c715b49f83e35cc787d7084c1633ebe94a2a3c4102e805613f7426b")
    version("0.7.5", sha256="f2428b4845083eff36385bec241ddddf7488a7de3f18886a78c73226e9e3306c")
    version("0.7.4", sha256="15cfae9e8a207ded403ad9fa2e77f09d14c2fe377d1bc5f8b063647e2d0554e0")
    version("0.6.9", sha256="56915b3e2200c6fb56260a36f839e66ce27d7dd3ef55fba278c3931b786fbfd1")

    depends_on("cxx", type="build")  # generated

    depends_on("py-setuptools@0.6c5:", type="build")
    depends_on("py-cython", type="build")

    depends_on("bedtools2", type="run")

    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pysam", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
