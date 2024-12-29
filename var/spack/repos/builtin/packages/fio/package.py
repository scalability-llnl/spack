# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Fio(AutotoolsPackage):
    """Flexible I/O Tester.

    Fio spawns a number of threads or processes doing a particular type of I/O
    action as specified by the user. fio takes a number of global parameters,
    each inherited by the thread unless otherwise parameters given to them
    overriding that setting is given.
    """

    homepage = "https://github.com/axboe/fio"
    url = "https://github.com/axboe/fio/archive/fio-3.26.tar.gz"

    license("GPL-2.0-only")

    version("3.37", sha256="b59099d42d5c62a8171974e54466a688c8da6720bf74a7f16bf24fb0e51ff92d")
    version("3.36", sha256="b34b8f3c5cd074c09ea487ffe3f444e95565c214b34a73042f35b00cbaab0e17")
    version("3.34", sha256="42ea28c78d269c4cc111b7516213f4d4b32986797a710b0ff364232cc7a3a0b7")
    version("3.33", sha256="f48b2547313ffd1799c58c6a170175176131bbd42bc847b5650784eaf6d914b3")
    version("3.26", sha256="8bd6987fd9b8c2a75d3923661566ade50b99f61fa4352148975e65577ffa4024")
    version("3.25", sha256="d8157676bc78a50f3ac82ffc6f80ffc3bba93cbd892fc4882533159a0cdbc1e8")
    version("3.19", sha256="809963b1d023dbc9ac7065557af8129aee17b6895e0e8c5ca671b0b14285f404")
    version("3.16", sha256="c7731a9e831581bab7104da9ea60c9f44e594438dbe95dff26726ca0285e7b93")
    version("2.19", sha256="61fb03a18703269b781aaf195cb0d7931493bbb5bfcc8eb746d5d66d04ed77f7")

    variant("gui", default=False, description="Enable building of gtk gfio")
    variant("doc", default=False, description="Generate documentation")
    variant("libaio", default=False, description="Enable libaio engine")

    depends_on("c", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("zlib-api")
    depends_on("gtkplus@2.18:", when="+gui")
    depends_on("cairo", when="+gui")
    depends_on("libaio", when="+libaio")
    depends_on("py-sphinx", type="build", when="+doc")

    conflicts("+libaio", when="platform=darwin", msg="libaio does not support Darwin")
    conflicts("+libaio", when="platform=windows", msg="libaio does not support Windows")
    conflicts("@:3.18", when="%gcc@10:", msg="gcc@10: sets -fno-common by default")

    def configure_args(self):
        config_args = ["--disable-native"]

        if self.spec.satisfies("+gui"):
            config_args.append("--enable-gfio")

        return config_args

    @run_after("build")
    def build_docs(self):
        if self.spec.satisfies("+doc"):
            make("-C", "doc", "html")
            make("-C", "doc", "man")
