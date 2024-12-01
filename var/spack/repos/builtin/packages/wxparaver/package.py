# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Wxparaver(AutotoolsPackage):
    """ "A very powerful performance visualization and analysis tool
    based on traces that can be used to analyse any information that
    is expressed on its input trace format.  Traces for parallel MPI,
    OpenMP and other programs can be genereated with Extrae."""

    homepage = "https://tools.bsc.es/paraver"
    url = "https://ftp.tools.bsc.es/wxparaver/wxparaver-4.9.2-src.tar.bz2"

    license("LGPL-2.1-or-later")

    version("4.9.2", sha256="83289584040bcedf8cab1b2ae3545191c8bdef0e11ab62b06e54cbf111f2127a")
    version("4.9.1", sha256="e89fdf563d1fc73ed0018cf0e25b458b6617ec33325ed3fdbf06397c556f3a8e")
    version("4.9.0", sha256="1f9964d7987032d01a354327845bf53ae369be5d8acf7d4e85bec81699a6ddf6")
    version("4.8.2", sha256="0d22ec362e4798d7ed21b15b607859e9bda9579e3d5b23af3812c1e32ccc192d")
    version("4.8.1", sha256="d03b04254bd3015d61374b95aeda6888f593be67286c5268849623baa2ae6e2e")
    version("4.8.0", sha256="780af8fff7cb40d1325260fb9f79210f6676f07357bc9b95b1b838862f2d1e5b")
    version("4.7.2", sha256="90107797d6af6fc3ebd9505445bb518d673edecbe5d08d1b7af01695d53241ae")
    version("4.7.1", sha256="8cbec0c5e0f8a849820f6682cbb0920ea234bb7f20d1483e38ea5d0b0ee045cd")
    version("4.7.0", sha256="81e02bcc1853455b13435172a4336ba85ba05020887d322c9678c97def03d76f")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.36: +serialization")
    depends_on("wxwidgets@2.8:")  # NOTE: using external for this one is usually simpler
    depends_on("wxpropgrid@1.4:")
    depends_on("libxml2")
    depends_on("zlib-api")

    def configure_args(self):
        spec = self.spec
        args = []

        args.append("--with-boost=%s" % spec["boost"].prefix)
        args.append("--with-wx-config=%s/wx-config" % spec["wxwidgets"].prefix.bin)
        if spec["wxwidgets"].satisfies("@:2"):
            args.append("--with-wxpropgrid=%s" % spec["wxpropgrid"].prefix)

        return args

    # use make install directly as expected by Paraver (See README)
    def build(self, spec, prefix):
        pass
