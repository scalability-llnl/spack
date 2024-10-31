# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Imlib2(AutotoolsPackage, SourceforgePackage):
    """
    Library that does image file loading and saving as well as rendering,
    manipulation, arbitrary polygon support
    """

    homepage = "https://sourceforge.net/projects/enlightenment/"
    sourceforge_mirror_path = "enlightenment/imlib2-1.5.1.tar.bz2"

    maintainers("TheQueasle")

    license("Imlib2")

    version("1.7.1", sha256="033a6a639dcbc8e03f65ff05e57068e7346d50ee2f2fff304bb9095a1b2bc407")
    version("1.7.0", sha256="1976ca3db48cbae79cd0fc737dabe39cc81494fc2560e1d22821e7dc9c22b37d")
    version("1.6.1", sha256="4d393a77e13da883c8ee2da3b029da3570210fe37d000c9ac33d9fce751b166d")
    version("1.6.0", sha256="cfc440ddfaed5fc85ba2572ad8d87a87cd77a5bffb33ebca882c42cefcd8691d")
    version("1.5.1", sha256="fa4e57452b8843f4a70f70fd435c746ae2ace813250f8c65f977db5d7914baae")

    depends_on("c", type="build")  # generated

    depends_on("libtiff")
    depends_on("giflib")
    depends_on("bzip2")
    depends_on("freetype")
    depends_on("libxext")
    depends_on("libpng")
    depends_on("libid3tag")
    depends_on("libjpeg-turbo")
    depends_on("pkgconfig", type="build")
