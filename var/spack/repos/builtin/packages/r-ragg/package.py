# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRagg(RPackage):
    """Graphic Devices Based on AGG.

    Anti-Grain Geometry (AGG) is a high-quality and high-performance 2D drawing
    library. The 'ragg' package provides a set of graphic devices based on AGG
    to use as alternative to the raster devices provided through the
    'grDevices' package."""

    cran = "ragg"

    license("MIT")

    version("1.3.2", sha256="8037a45209fdd50acf101208af8e832b840a11ad4201cf7fb480de432e6b6931")
    version("1.2.5", sha256="936f4d75e0e01cdeefb9f57d121cdd7812d0de5a9e1a3a8315f92ce1c84da8f9")
    version("1.2.4", sha256="c547e5636a2eefaa0021a0d50fad1e813c2ce976ec0c9c3f796d38a110680dcd")
    version("1.2.3", sha256="976da0007ef0d4dbadda4734727b539671b65c1eff4ff392d734f4e2c846f2b2")

    depends_on("r-systemfonts@1.0.3:", type=("build", "run"))
    depends_on("r-textshaping@0.3.0:", type=("build", "run"))
    depends_on("freetype")
    depends_on("libpng")
    depends_on("libtiff")
    depends_on("jpeg")

    def flag_handler(self, name, flags):
        # Freetype 2.13.3 broke the public interface by switching char/unsigned char:
        if name == "cxxflags" and self.spec["freetype"].version >= Version("2.13.3"):
            flags.append("-fpermissive")
        return (flags, None, None)
