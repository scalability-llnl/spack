# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import re

from spack.package import *


class Yafyaml(CMakePackage):
    """
    yet another Fortran (implementation of) YAML

    There is at least one other open source Fortran-based YAML parser.

    The rationale for this one is simply to be compatible with the
    containers in gFTL.  It is not intended to be a complete YAML
    parser, just the subset needed by my own projects.
    """

    homepage = "https://github.com/Goddard-Fortran-Ecosystem/yaFyaml"
    url = "https://github.com/Goddard-Fortran-Ecosystem/yaFyaml/archive/refs/tags/v1.0.4.tar.gz"
    list_url = "https://github.com/Goddard-Fortran-Ecosystem/yaFyaml/tags"
    git = "https://github.com/Goddard-Fortran-Ecosystem/yaFyaml.git"

    maintainers("mathomp4", "tclune")

    license("Apache-2.0")

    version("main", branch="main")

    version("1.4.0", sha256="2a415087eb26d291ff40da4430d668c702d22601ed52a72d001140d97372bc7d")
    version("1.3.0", sha256="a3882210b2620485471e3337d995edc1e653b49d9caaa902a43293826a61a635")
    version("1.2.0", sha256="912a4248bbf2e2e84cf3e36f2ae8483bee6b32d2eaa4406dd2100ad660c9bfc6")
    version("1.1.0", sha256="f0be81afe643adc2452055e5485f09cdb509a8fdd5a4ec5547b0c31dd22b4830")
    version("1.0.7", sha256="54f5c87e86c12e872e615fbc9540610ae38053f844f1e75d1e753724fea85c64")
    version("1.0.6", sha256="8075e1349d900985f5b5a81159561568720f21c5f011c43557c46f5bbedd0661")
    version("1.0.5", sha256="84abad01cdcfe387240844c35e5fb36d5099f657b57a50d5d5909cc567e72200")
    version("1.0.4", sha256="93ba67c87cf96be7ebe479907ca5343251aa48072b2671b8630bd244540096d3")
    version("1.0.3", sha256="cfbc6b6db660c5688e37da56f9f0091e5cafeeaec395c2a038469066c83b0c65")
    version("1.0.2", sha256="1d08d093d0f4331e4019306a3b6cb0b230aed18998692b57931555d6805f3d94")
    version("1.0.1", sha256="706d77c43a9c3d2cbd1030c4bbf6b196ea2e0d84df72b3704035d1b52c408baf")
    version("1.0.0", sha256="19334e924d031445f159602a27a1e6778e8a1bd2ead219accdb397c25706f88e")
    version("1.0-beta8", sha256="0a2ae37f45abaca2e4d8dbc317117eeb08c5652d5d2524f51852d957fd719855")
    version("1.0-beta7", sha256="cf7992818cc2caa86346f6f24c251bcfd96bc68eaacc17da89d997260d9db867")
    version("1.0-beta6", sha256="9d90ffd78ae70e477ed58afa474e214822a3c1a0a86c067ba3e245550108a028")
    version("1.0-beta5", sha256="509487c544f199503b3724c170a6d6cd35c237e8ee23a34e94ee3c056b9e39ee")
    version("1.0-beta4", sha256="42bf9c8517d7867614cc24cc4267c70bbe6f8d62474e22d3552d9cc5aa4fc195")
    version("0.5.1", sha256="7019460314e388b2d556db75d5eb734237a18494f79b921613addb96b7b7ce2f")
    version("0.5.0", sha256="8ac5d41b1020e9311ac87f50dbd61b9f3e3188f3599ce463ad59650208fdb8ad")

    depends_on("fortran", type="build")

    depends_on("gftl-shared")
    depends_on("gftl")
    depends_on("cmake@3.12:", type="build")

    # yafyaml only works with the Fujitsu compiler from 1.3.0 onwards
    conflicts(
        "%fj",
        when="@:1.2.0",
        msg="yaFyaml only works with the Fujitsu compiler from 1.3.0 onwards",
    )

    # GCC 13.3 and higher only work with yafyaml 1.4.0 onwards
    # First we can check if the spec is gcc@13.3...
    conflicts("%gcc@13.3:", when="@:1.3.0", msg="GCC 13.3+ only works with yafyaml 1.4.0 onwards")

    # ...but if it is not (say apple-clang with gfortran as a fc), there is
    # no easy way to check this. So we hijack flag_handler to raise an
    # exception if we detect gfortran 13.3 or 14.
    # NOTE: This will only error out at install time, so `spack spec` will
    # not catch this.
    def flag_handler(self, name, flags):
        # We need to match any compiler that has a name of gfortran or gfortran-*
        pattern = re.compile(r"gfortran(-\d+)?$")

        if pattern.search(self.compiler.fc):
            gfortran_version = spack.compiler.get_compiler_version_output(
                self.compiler.fc, "-dumpfullversion"
            ).strip()

            # gfortran_version is now a string like "13.3.0". We now need to just capture
            # the major and minor version numbers
            gfortran_version = ".".join(gfortran_version.split(".")[:2])

            if self.spec.satisfies("@:1.3.0") and (float(gfortran_version) >= 13.3):
                raise InstallError(
                    f"Your gfortran version {gfortran_version} is not compatible with "
                    f"yafyaml 1.3.0 and below. Use yafyaml 1.4.0 or higher."
                )
        return None, None, None

    variant(
        "build_type",
        default="Release",
        description="The build type to build",
        values=("Debug", "Release"),
    )
    variant("fismahigh", default=False, description="Apply patching for FISMA-high compliance")

    @when("+fismahigh")
    def patch(self):
        if os.path.exists("tools/ci-install-gfe.bash"):
            os.remove("tools/ci-install-gfe.bash")
