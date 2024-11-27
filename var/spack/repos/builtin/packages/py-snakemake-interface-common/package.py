# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySnakemakeInterfaceCommon(PythonPackage):
    """Common functions and classes for Snakemake and its plugins."""

    homepage = "https://github.com/snakemake/snakemake-interface-common"
    pypi = "snakemake_interface_common/snakemake_interface_common-1.17.3.tar.gz"
    maintainers("w8jcik")

    license("MIT")

    version("1.17.3", sha256="cca6e2c728072a285a8e750f00fdd98d9c50063912184c41f8b89e4cab66c7b0")
    version("1.17.1", sha256="555c8218d9b68ddc1046f94a517e7d0f22e15bdc839d6ce149608d8ec137b9ae")

    depends_on("py-argparse-dataclass@2", type=("build", "run"))
    depends_on("py-configargparse@1.7:1", type=("build", "run"))

    depends_on("python@:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
