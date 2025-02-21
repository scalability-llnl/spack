# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSp(RPackage):
    """Classes and Methods for Spatial Data.

    Classes and methods for spatial data; the classes document where the
    spatial location information resides, for 2D or 3D data. Utility functions
    are provided, e.g. for plotting data as maps, spatial selection, as well as
    methods for retrieving coordinates, for subsetting, print, summary, etc."""

    cran = "sp"

    license("GPL-2.0-or-later")

    version("2.1-4", sha256="e185e7fb61d2d7dbc50fd765a93e170fa778083a653588db1f5e99d019479f0a")
    version("1.6-0", sha256="f5977fbe80e7dee8e95d41fe0ef9d87c2c984422bb529ea5211fd38a13f9fcda")
    version("1.5-1", sha256="69b9eab481d389bbb736d2adcf50c180aca248c3ffc4ebda8ffe2accc5f229df")
    version("1.5-0", sha256="939a06adf78ec8de7a663d6ca5bba426780852b357773446b00cc298200ff81c")
    version("1.4-7", sha256="01946953707363b78d3eb8dcf472ea8c6ea0097094aa0ca0b756ce5fac01b1ad")
    version("1.4-6", sha256="9aebb3ef2140e8984a67eb93d72f686b8707d48d82445db0c54ae895576ba226")
    version("1.4-5", sha256="6beeb216d540475cdead5f2c72d6c7ee400fe2423c1882d72cf57f6df58f09da")
    version("1.3-1", sha256="57988b53ba8acc35f3912d62feba4b929a0f757c6b54080c623c5d805e0cb59f")
    version("1.2-7", sha256="6d60e03e1abd30a7d4afe547d157ce3dd7a8c166fc5e407fd6d62ae99ff30460")
    version("1.2-3", sha256="58b3a9e395ca664ee61b20b480be4eb61576daca44c3d3f6f9a943bb0155879a")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.2.0:", type=("build", "run"), when="@2.0-0:")
    depends_on("r@3.5.0:", type=("build", "run"), when="@2.1-0:")
    depends_on("r-lattice", type=("build", "run"))
