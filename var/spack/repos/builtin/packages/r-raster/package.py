# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRaster(RPackage):
    """Geographic Data Analysis and Modeling.

    Reading, writing, manipulating, analyzing and modeling of spatial data. The
    package implements basic and high-level functions for raster data and for
    vector data operations such as intersections. See the manual and tutorials
    on <https://rspatial.org/> to get started."""

    cran = "raster"

    license("GPL-3.0-or-later")

    version("3.6-26", sha256="c65777225a46ada699e70098f54c60cf191d15e454fac9440aca439a4dbd5592")
    version("3.6-20", sha256="7e5be49f4e37a2c14a3b87661b252956643b959146cbdb08e983660c1d59a813")
    version("3.6-3", sha256="9f06e0f7c36258790a97421b3a26d98c9b6a2cb702f941e58ab0b18f21b0c3c6")
    version("3.5-15", sha256="29c7d3c5d34284f8b5a2ddc9989fbcf092ce209d5eb5310ebc772b5ebdfdd685")
    version("3.5-11", sha256="e6c4823925260c65fe98585d7a0d47778616ae2e4eb1a1782b219580a9db61a3")
    version("3.4-5", sha256="c6620d790b3aba1b64aec31325f726e63f26a14a1b48c1a0f9167a0b1a64e4a5")
    version("2.9-23", sha256="90aaec9e3b1e3e6015d9993ea7491e008f2f71990f8abb8610f979c4e28b38af")
    version("2.9-22", sha256="8107d95f1aa85cea801c8101c6aa391becfef4b5b915d9bc7a323531fee26128")
    version("2.5-8", sha256="47992abd783450513fbce3770298cc257030bf0eb77e42aa3a4b3924b16264cc")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@3.5.0:", type=("build", "run"), when="@3.4-5:")
    depends_on("r-sp@1.2-0:", type=("build", "run"))
    depends_on("r-sp@1.4-1:", type=("build", "run"), when="@3.4-5:")
    depends_on("r-sp@1.4-5:", type=("build", "run"), when="@3.5-11:")
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-terra@1.4-11:", type=("build", "run"), when="@3.5-11:")
    depends_on("r-terra@1.5-12:", type=("build", "run"), when="@3.5-15:")
    depends_on("r-terra@1.6-16:", type=("build", "run"), when="@3.6-3:")
    depends_on("r-terra@1.6-41:", type=("build", "run"), when="@3.6-20:")
    depends_on("r-terra@1.7-29:", type=("build", "run"), when="@3.6-23:")
