# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNanotime(RPackage):
    """Nanosecond-Resolution Time Support for R.

    Full 64-bit resolution date and time functionality with; nanosecond
    granularity is provided, with easy transition to and from; the standard
    'POSIXct' type. Three additional classes offer interval,; period and
    duration functionality for nanosecond-resolution timestamps."""

    cran = "nanotime"

    license("GPL-2.0-or-later")

    version("0.3.9", sha256="cc2965edfd68f83a84142ead27a5a84e1c5b2931ec911dddecb3e0bc3ffa79d8")
    version("0.3.7", sha256="a771782653aef62a071682907fd7bd611f7f98fc80beda227d619aae166ccb15")
    version("0.3.6", sha256="df751a5cb11ca9ac8762cd1e33bc73e7d20fde9339d2c46bc6f85873388568df")
    version("0.3.5", sha256="44deaae58452bacea4855d018212593811401c2afc460ffb11905479013923a0")
    version("0.3.2", sha256="9ef53c3bca01b605a9519190117988e170e63865327007c90b05d31fe7f22b1d")
    version("0.2.4", sha256="2dfb7e7435fec59634b87563a215467e7793e2711e302749c0533901c74eb184")
    version("0.2.3", sha256="7d6df69a4223ae154f610b650e24ece38ce4aa706edfa38bec27d15473229f5d")
    version("0.2.0", sha256="9ce420707dc4f0cb4241763579b849d842904a3aa0d88de8ffef334d08fa188d")

    depends_on("r-bit64", type=("build", "run"))
    depends_on("r-rcppcctz@0.2.3:", type=("build", "run"))
    depends_on("r-rcppcctz@0.2.9:", type=("build", "run"), when="@0.3.2:")
    depends_on("r-zoo", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"), when="@0.3.2:")
    depends_on("r-rcppdate", type=("build", "run"), when="@0.3.2:")
