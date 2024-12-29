# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libgeotiff(AutotoolsPackage):
    """GeoTIFF represents an effort by over 160 different remote sensing, GIS,
    cartographic, and surveying related companies and organizations to
    establish a TIFF based interchange format for georeferenced raster imagery.
    """

    homepage = "https://trac.osgeo.org/geotiff/"
    url = "https://download.osgeo.org/geotiff/libgeotiff/libgeotiff-1.6.0.tar.gz"

    maintainers("adamjstewart")

    license("Public-Domain")

    version("1.7.1", sha256="05ab1347aaa471fc97347d8d4269ff0c00f30fa666d956baba37948ec87e55d6")
    version("1.7.0", sha256="fc304d8839ca5947cfbeb63adb9d1aa47acef38fc6d6689e622926e672a99a7e")
    version("1.6.0", sha256="9311017e5284cffb86f2c7b7a9df1fb5ebcdc61c30468fb2e6bca36e4272ebca")
    version("1.5.1", sha256="f9e99733c170d11052f562bcd2c7cb4de53ed405f7acdde4f16195cd3ead612c")
    version("1.5.0", sha256="1c0bef329c60f770ed128e8b273945100f1a4b5abd161ac61e93bc947b0624dd")
    version("1.4.3", sha256="b8510d9b968b5ee899282cdd5bef13fd02d5a4c19f664553f81e31127bc47265")
    version("1.4.2", sha256="ad87048adb91167b07f34974a8e53e4ec356494c29f1748de95252e8f81a5e6e")

    depends_on("c", type="build")  # generated

    variant("zlib", default=True, description="Include zlib support")
    variant("jpeg", default=True, description="Include jpeg support")
    variant("proj", default=True, description="Use PROJ.x library")

    depends_on("zlib-api", when="+zlib")
    depends_on("jpeg", when="+jpeg")
    depends_on("libtiff")
    depends_on("proj", when="+proj")
    depends_on("proj@:5", when="@:1.4+proj")
    depends_on("proj@6:", when="@1.5:+proj")

    # Patches required to fix rounding issues in unit tests
    # https://github.com/OSGeo/libgeotiff/issues/16
    patch(
        "https://github.com/OSGeo/libgeotiff/commit/7cb9b68ea72fb2a6023bb98796fd3ba6dc7b64a1.patch?full_index=1",
        sha256="bae1441ba8cd1d4e94b8d6a080db64b768dd537faa7e2fb8c04133f68e71d304",
        level=2,
        when="@1.5.0:1.5.1",
    )
    patch(
        "https://github.com/OSGeo/libgeotiff/commit/4b41ca6ce332f0c21504c2da3da850275d9da5ae.patch?full_index=1",
        sha256="b368cdf5755f2ddf69d974bf86691440dcc861c41d86280780626f5a31f33b13",
        level=2,
        when="@1.5.0:1.5.1",
    )
    # Patch required to fix absolute path issue in unit tests
    # https://github.com/OSGeo/libgeotiff/issues/16
    patch("a76c686441398669422cb728411abd2dec358f7f.patch", level=2, when="@1.5.0:1.5.1")

    def configure_args(self):
        spec = self.spec

        args = ["--with-libtiff={0}".format(spec["libtiff"].prefix)]

        if spec.satisfies("+zlib"):
            args.append("--with-zlib={0}".format(spec["zlib-api"].prefix))
        else:
            args.append("--with-zlib=no")

        if spec.satisfies("+jpeg"):
            args.append("--with-jpeg={0}".format(spec["jpeg"].prefix))
        else:
            args.append("--with-jpeg=no")

        if spec.satisfies("+proj"):
            args.append("--with-proj={0}".format(spec["proj"].prefix))
        else:
            args.append("--with-proj=no")

        return args
