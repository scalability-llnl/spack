# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHatchet(PythonPackage):
    """Hatchet is a performance tool for analyzing hierarchical performance data
    using a graph-indexed Pandas dataframe."""

    homepage = "https://github.com/hatchet/hatchet"
    url = "https://github.com/hatchet/hatchet/archive/v1.0.0.tar.gz"
    tags = ["radiuss"]

    maintainers("slabasan", "bhatele", "tgamblin")

    license("MIT")

    version("1.4.0", sha256="9f934f128666703d30818e9a091493df1bf1819bf7445ffb35a0f46871501b55")
    version(
        "1.3.0",
        sha256="d77d071fc37863fdc9abc3fd9ea1088904cd98c6980a014a31e44595d2deac5e",
        deprecated=True,
    )
    version(
        "1.2.0",
        sha256="1d5f80abfa69d1a379dff7263908c5c915023f18f26d50b639556e2f43ac755e",
        deprecated=True,
    )
    version(
        "1.1.0",
        sha256="71bfa2881ef295294e5b4493acb8cce98d14c354e9ae59b42fb56a76d8ec7056",
        deprecated=True,
    )
    version(
        "1.0.1",
        sha256="e5a4b455ab6bfbccbce3260673d9af8d1e4b21e19a2b6d0b6c1e1d7727613b7a",
        deprecated=True,
    )
    version(
        "1.0.0",
        sha256="efd218bc9152abde0a8006489a2c432742f00283a114c1eeb6d25abc10f5862d",
        deprecated=True,
    )

    depends_on("c", type="build")  # generated

    # https://github.com/hatchet/hatchet/issues/428
    depends_on("python@2.7:3.8", when="@:1.3.0", type=("build", "run"))
    depends_on("python@2.7:", when="@1.3.1:", type=("build", "run"))

    depends_on("py-cython", when="@1.4:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-pydot", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-textx", when="@1.4:", type=("build", "run"))
    depends_on("py-multiprocess", when="@1.4:", type=("build", "run"))
    depends_on("py-caliper-reader", when="@1.4:", type=("build", "run"))
    depends_on("py-pycubexr", when="@1.4:", type=("build", "run"))
