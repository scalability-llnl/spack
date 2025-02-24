# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class ROptparse(RPackage):
    """Command Line Option Parser.

    A command line parser inspired by Python's 'optparse' library to be used
    with Rscript to write "#!" shebang scripts that accept short and long
    flag/options"""

    cran = "optparse"

    license("GPL-2.0-or-later")

    version("1.7.5", sha256="0cc917505780786e69b8ceca4b3840ed7b0c011495108ec05af3871965415712")
    version("1.7.3", sha256="6287e1af051d4a65037900ce7b30bd962039450dd4eab63b6f2491eace6a07ed")
    version("1.7.1", sha256="324e304c13efd565d766766193d4ccd75e2cd949dfcfb416afc3939489071fe7")
    version("1.6.6", sha256="51779d497146e9354b1153713d939e81551e08948c2b00e4b117b1377c0b60d0")
    version("1.6.2", sha256="b5a5a49ae05005f20359868329b73daac83d50f5e088981dcf5c41399534377f")
    version("1.6.1", sha256="819be3eff54cb7f3f18703eed9714fc655290ab8e169f87605433d069b597e13")
    version("1.6.0", sha256="10e816bb8f5b08d52cfd3a0028903a8c62ef9cf7bfd85f9dae8af442e82bfbb4")

    depends_on("r@2.9.0:", type=("build", "run"))
    depends_on("r@3.6.0:", type=("build", "run"), when="@1.7.3:")
    depends_on("r-getopt@1.20.2:", type=("build", "run"))
