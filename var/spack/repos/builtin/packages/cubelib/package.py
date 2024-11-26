# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Cubelib(AutotoolsPackage):
    """Component of CubeBundle: General purpose C++ library and tools"""

    homepage = "https://www.scalasca.org/software/cube-4.x/download.html"
    url = "https://apps.fz-juelich.de/scalasca/releases/cube/4.4/dist/cubelib-4.4.tar.gz"

    maintainers("swat-jsc", "wrwilliams")

    version("4.8.2", sha256="d6fdef57b1bc9594f1450ba46cf08f431dd0d4ae595c47e2f3454e17e4ae74f4")
    version("4.8.1", sha256="e4d974248963edab48c5d0fc5831146d391b0ae4632cccafe840bf5f12cd80a9")
    version("4.8", sha256="171c93ac5afd6bc74c50a9a58efdaf8589ff5cc1e5bd773ebdfb2347b77e2f68")
    version("4.7.1", sha256="62cf33a51acd9a723fff9a4a5411cd74203e24e0c4ffc5b9e82e011778ed4f2f")
    version("4.7", sha256="e44352c80a25a49b0fa0748792ccc9f1be31300a96c32de982b92477a8740938")
    version("4.6", sha256="36eaffa7688db8b9304c9e48ca5dc4edc2cb66538aaf48657b9b5ccd7979385b")
    version(
        "4.5",
        sha256="98f66837b4a834b1aacbcd4480a242d7a8c4a1b8dd44e02e836b8c7a4f0ffd98",
        deprecated="true",
    )
    version(
        "4.4.4",
        sha256="adb8216ee3b7701383884417374e7ff946edb30e56640307c65465187dca7512",
        deprecated="true",
    )
    version(
        "4.4.3",
        sha256="bcd4fa81a5ba37194e590a5d7c3e6c44b448f5e156a175837b77c21206847a8d",
        deprecated="true",
    )
    version(
        "4.4.2",
        sha256="843335c7d238493f1b4cb8e07555ccfe99a3fa521bf162e9d8eaa6733aa1f949",
        deprecated="true",
    )
    version(
        "4.4",
        sha256="77548e1732fa5e82b13cc8465c8a21349bf42b45a382217d2e70d18576741d5c",
        deprecated="true",
    )

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("pkgconfig", type="build")
    depends_on("zlib-api")

    def url_for_version(self, version):
        url = "http://apps.fz-juelich.de/scalasca/releases/cube/{0}/dist/cubelib-{1}.tar.gz"

        return url.format(version.up_to(2), version)

    def configure_args(self):
        configure_args = ["--enable-shared"]
        configure_args.append("--with-frontend-zlib=%s" % self.spec["zlib-api"].prefix.lib)
        return configure_args

    def install(self, spec, prefix):
        make("install", parallel=False)
