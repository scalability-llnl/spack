# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *

# Although this looks like an Autotools package, it's not one. Refer to:
# https://github.com/flame/blis/issues/17
# https://github.com/flame/blis/issues/195
# https://github.com/flame/blis/issues/197


class BlisBase(MakefilePackage):
    """Base class for building BLIS, shared with the AMD optimized version
    of the library in the 'amdblis' package.
    """

    maintainers("jeffhammond")

    depends_on("python@2.7:2.8,3.4:", type=("build", "run"))

    variant(
        "threads",
        default="none",
        values=("pthreads", "openmp", "none"),
        description="Multithreading support",
        multi=False,
    )

    variant("ilp64", default=False, description="Force 64-bit Fortran native integers")
    variant("blas", default=True, description="BLAS compatibility")
    variant("cblas", default=True, description="CBLAS compatibility")
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )

    # TODO: add cpu variants. Currently using auto.
    # If one knl, should the default be memkind ?

    # BLIS has it's own API but can be made compatible with BLAS
    # enabling CBLAS automatically enables BLAS.

    provides("blas", when="+blas")
    provides("blas", when="+cblas")

    conflicts("%nvhpc")
    conflicts("%pgi")

    def configure_args(self):
        spec = self.spec
        config_args = ["--enable-threading={0}".format(spec.variants["threads"].value)]

        if spec.satisfies("+ilp64"):
            config_args.append("--blas-int-size=64")
        else:
            config_args.append("--blas-int-size=32")

        if spec.satisfies("+cblas"):
            config_args.append("--enable-cblas")
        else:
            config_args.append("--disable-cblas")

        if spec.satisfies("+blas"):
            config_args.append("--enable-blas")
        else:
            config_args.append("--disable-blas")

        if spec.satisfies("libs=shared"):
            config_args.append("--enable-shared")
        else:
            config_args.append("--disable-shared")

        if spec.satisfies("libs=static"):
            config_args.append("--enable-static")
        else:
            config_args.append("--disable-static")

        return config_args

    def edit(self, spec, prefix):
        # To ensure auto should always be the last argument for base and derived class
        config_args = self.configure_args() + ["auto"]
        configure("--prefix={0}".format(prefix), *config_args)

    @run_after("install")
    def darwin_fix(self):
        # The shared library is not installed correctly on Darwin; fix this
        if self.spec.satisfies("platform=darwin"):
            fix_darwin_install_name(self.prefix.lib)

    @property
    def libs(self):
        return find_libraries(
            ["libblis", "libblis-mt"],
            root=self.prefix,
            shared=self.spec.satisfies("libs=shared"),
            recursive=True,
        )


class Blis(BlisBase):
    """BLIS is a portable software framework for instantiating high-performance
    BLAS-like dense linear algebra libraries.

    The framework was designed to isolate essential kernels of computation
    that, when optimized, immediately enable optimized implementations of
    most of its commonly used and computationally intensive operations. BLIS
    is written in ISO C99 and available under a new/modified/3-clause BSD
    license. While BLIS exports a new BLAS-like API, it also includes a
    BLAS compatibility layer which gives application developers access to
    BLIS implementations via traditional BLAS routine calls.
    An object-based API unique to BLIS is also available.
    """

    homepage = "https://github.com/flame/blis"
    url = "https://github.com/flame/blis/archive/0.7.0.tar.gz"
    git = "https://github.com/flame/blis.git"

    license("BSD-3-Clause")

    version("master", branch="master")
    version("1.0", sha256="9c12972aa1e50f64ca61684eba6828f2f3dd509384b1e41a1e8a9aedea4b16a6")
    version("0.9.0", sha256="1135f664be7355427b91025075562805cdc6cc730d3173f83533b2c5dcc2f308")
    version("0.8.1", sha256="729694128719801e82fae7b5f2489ab73e4a467f46271beff09588c9265a697b")
    version("0.8.0", sha256="5e05868c4a6cf5032a7492f8861653e939a8f907a4fa524bbb6e14394e170a3d")
    version("0.7.0", sha256="7e345d666799e15bba570bd125f97042f17bf752a61dcf314486a6cd096d5f68")
    version("0.6.1", sha256="76b22f29b7789cf117c0873d2a6b2a6d61f903869168148f2e7306353c105c37")
    version("0.6.0", sha256="ad5765cc3f492d0c663f494850dafc4d72f901c332eb442f404814ff2995e5a9")
    version("0.5.0", sha256="1a004d69c139e8a0448c6a6007863af3a8c3551b8d9b8b73fe08e8009f165fa8")
    version("0.4.0", sha256="9c7efd75365a833614c01b5adfba93210f869d92e7649e0b5d9edc93fc20ea76")
    version("0.3.2", sha256="b87e42c73a06107d647a890cbf12855925777dc7124b0c7698b90c5effa7f58f")
    version("0.3.1", sha256="957f28d47c5cf71ffc62ce8cc1277e17e44d305b1c2fa8506b0b55617a9f28e4")
    version("0.3.0", sha256="d34d17df7bdc2be8771fe0b7f867109fd10437ac91e2a29000a4a23164c7f0da")
    version("0.2.2", sha256="4a7ecb56034fb20e9d1d8b16e2ef587abbc3d30cb728e70629ca7e795a7998e8")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    # Problems with permissions on installed libraries:
    # https://github.com/flame/blis/issues/343
    patch("Makefile_0.6.0.patch", when="@0.4.0:0.6.0")
