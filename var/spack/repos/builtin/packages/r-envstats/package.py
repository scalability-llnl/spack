# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class REnvstats(RPackage):
    """Package for Environmental Statistics, Including US EPA Guidance.

    Graphical and statistical analyses of environmental data, with  focus on
    analyzing chemical concentrations and physical parameters, usually in  the
    context of mandated environmental monitoring.  Major environmental
    statistical methods found in the literature and regulatory guidance
    documents,  with extensive help that explains what these methods do, how to
    use them,  and where to find them in the literature.  Numerous built-in
    data sets from  regulatory guidance documents and environmental statistics
    literature.  Includes  scripts reproducing analyses presented in the book
    "EnvStats:  An R Package for  Environmental Statistics" (Millard, 2013,
    Springer, ISBN 978-1-4614-8455-4,
    <https://www.springer.com/book/9781461484554>)."""

    cran = "EnvStats"

    version("2.8.1", sha256="12952b9eaa64b7bdbaaa5c6b7acb3aa1028ddfa4e5de7ddfea54f900c452d6a6")
    version("2.7.0", sha256="09a6f0d5b60856c7298371e4a8a085a1db7abf0e71ccb9a2dc9ca24248fb5d81")
    version("2.5.0", sha256="4f77aa66c9dbbe411370a6dd5b9e514823d5506bbcdad9dc09a9e4268d65a7f7")
    version("2.4.0", sha256="49459e76412037b3d8021bd83ee93d140bc3e715a2a2282a347ef60061900514")
    version("2.3.1", sha256="d753d42b42ff28c1cd25c63916fb2aa9e325941672fb16f7dfd97e218416cf2a")
    version("2.3.0", sha256="51b7c982b4ffc6506579ec6933c817b780b8dade9f5e7754122e4132cb677a75")
    version("2.2.1", sha256="bbad7736272a404302190ccf1095abd8674d4366f3827a1c0a9540bcafe0523e")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-nortest", type=("build", "run"))
