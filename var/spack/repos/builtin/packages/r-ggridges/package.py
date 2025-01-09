# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgridges(RPackage):
    """Ridgeline Plots in 'ggplot2'.

    Ridgeline plots provide a convenient way of visualizing changes in
    distributions over time or space. This package enables the creation of such
    plots in 'ggplot2'."""

    cran = "ggridges"

    license("GPL-2.0-only OR custom")

    version("0.5.6", sha256="efccaa309a150d11c6b402b912e618ea041f25cca3101f32cd821a6f41684e35")
    version("0.5.4", sha256="2bf71c2034804cec637e6748dc51d8cadad01d3ea4d14ace754327f082e8d851")
    version("0.5.3", sha256="f5eafab17f2d4a8a2a83821ad3e96ae7c26b62bbce9de414484c657383c7b42e")
    version("0.5.1", sha256="01f87cdcdf2052ed9c078d9352465cdeda920a41e2ca55bc154c1574fc651c36")
    version("0.5.0", sha256="124bc84044e56728fa965682f8232fc868f2af7d3eb7276f6b0df53be8d2dbfe")
    version("0.4.1", sha256="03d2013df6adf07c9741d4476df96865b878a88359763ac36b98aa86591cca4d")
    version("0.4.0", sha256="c62153fb47f55468c873e6cf882b46754b6eedec423dacf3992ab23c474d521c")

    depends_on("r@3.2:", type=("build", "run"))
    depends_on("r-ggplot2@2.2.0:", type=("build", "run"))
    depends_on("r-ggplot2@3.0.0:", type=("build", "run"), when="@0.5.3:")
    depends_on("r-ggplot2@3.4.0:", type=("build", "run"), when="@0.5.5:")
    depends_on("r-scales@0.4.1:", type=("build", "run"))
    depends_on("r-withr@2.1.1:", type=("build", "run"), when="@0.5.0:")

    depends_on("r-plyr@1.8.0:", type=("build", "run"), when="@:0.5.3")
