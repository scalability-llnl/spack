# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cube(AutotoolsPackage):
    """Cube the profile viewer for Score-P and Scalasca profiles. It displays a
    multi-dimensional performance space consisting of the dimensions:
    - performance metric
    - call path
    - system resource
    """

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.4/dist/cubegui-4.4.2.tar.gz"
    maintainers("swat-jsc")

    version("4.8.2", sha256="bf2e02002bb2e5c4f61832ce37b62a440675c6453463014b33b2474aac78f86d")
    version("4.8.1", sha256="a8a2a62b4e587c012d3d32385bed7c500db14232419795e0f4272d1dcefc55bc")
    version("4.8", sha256="1df8fcaea95323e7eaf0cc010784a41243532c2123a27ce93cb7e3241557ff76")
    version("4.7.1", sha256="7c96bf9ffb8cc132945f706657756fe6f88b7f7a5243ecd3741f599c2006d428")
    version("4.7", sha256="103fe00fa9846685746ce56231f64d850764a87737dc0407c9d0a24037590f68")
    version("4.6", sha256="1871c6736121d94a22314cb5daa8f3cbb978b58bfe54f677c4c9c9693757d0c5")
    version("4.5", sha256="ffe84108adce0adf06dca80820d941b1a60a5580a8bacc8f7c1b6989c8ab1bfa")
    version("4.4.4", sha256="9b7b96d5a64b558a9017cc3599bba93a42095534e018e3de9b1f80ab6d04cc34")
    version("4.4.3", sha256="bf4b0f2ff68507ff82ba24eb4895aed961710dae16d783c222a12f152440cf36")
    version("4.4.2", sha256="29b6479616a524f8325f5031a883963bf965fb92569de33271a020f08650ec7b")
    version("4.4", sha256="0620bae3ac357d0486ce7f5f97e448eeb2494c9a31865b679380ee08c6750e70")
    version("4.3.5", sha256="1dc26f473e8bb4cdbdd411224c3c2026a394f3e936f1918000dc65a222753912")
    version("4.3.4", sha256="34c55fc5d0c84942c0845a7324d84cde09f3bc1b3fae6a0f9556f7ea0e201065")
    version("4.3.3", sha256="ce8e1bff5a208fe5700a0194170be85bbd8f554e1aa1514b4afc5129326c7f83")
    version("4.2.3", sha256="b30c6998bcc54f795bcd6de3cfbef9c3cec094f782820174b533f628b0e60765")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("gui", default=True, description="Build Cube GUI")

    patch("qt-version.patch", when="@4.3.0:4.3 +gui")

    depends_on("cubelib@4.8:4.8.99", when="@4.8:4.8.99")
    depends_on("cubelib@4.7:4.7.99", when="@4.7:4.7.99")
    depends_on("cubelib@4.6:4.6.99", when="@4.6:4.6.99")
    depends_on("cubelib@4.5:4.5.99", when="@4.5:4.5.99")
    # There is a backwards dependency in series 4
    depends_on("cubelib@4.4:4.4.4", when="@4.4.4")
    depends_on("cubelib@4.4:4.4.3", when="@4.4.3")
    depends_on("cubelib@4.4:4.4.2", when="@4.4.2")
    depends_on("cubelib@4.4", when="@4.4")

    depends_on("pkgconfig", type="build")
    depends_on("dbus")
    depends_on("zlib-api")

    depends_on("qt@5:", when="@4.3.0: +gui")
    depends_on("qt@4.8:", when="@4.2.0:4.2 +gui")

    conflicts("~gui", when="@4.4:")

    def url_for_version(self, version):
        if version >= Version("4.4"):
            url = "http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cubegui-{1}.tar.gz"
        else:
            url = "http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cube-{1}.tar.gz"

        return url.format(version.up_to(2), version)

    def configure_args(self):
        spec = self.spec

        configure_args = ["--enable-shared"]

        if "+gui" not in spec:
            configure_args.append("--without-gui")

        return configure_args

    def install(self, spec, prefix):
        make("install", parallel=False)
