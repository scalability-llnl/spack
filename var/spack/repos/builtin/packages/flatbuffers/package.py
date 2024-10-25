# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Flatbuffers(CMakePackage):
    """Memory Efficient Serialization Library"""

    homepage = "https://google.github.io/flatbuffers/"
    url = "https://github.com/google/flatbuffers/archive/v1.9.0.tar.gz"

    license("Apache-2.0")

    version("24.3.25", sha256="4157c5cacdb59737c5d627e47ac26b140e9ee28b1102f812b36068aab728c1ed")
    version("24.3.7", sha256="bfff9d2150fcff88f844e8c608b02b2a0e94c92aea39b04c0624783464304784")
    version("2.0.6", sha256="e2dc24985a85b278dd06313481a9ca051d048f9474e0f199e372fea3ea4248c9")
    version("2.0.0", sha256="9ddb9031798f4f8754d00fca2f1a68ecf9d0f83dfac7239af1311e4fd9a565c4")
    version("1.12.0", sha256="62f2223fb9181d1d6338451375628975775f7522185266cd5296571ac152bc45")
    version("1.11.0", sha256="3f4a286642094f45b1b77228656fbd7ea123964f19502f9ecfd29933fd23a50b")
    version("1.10.0", sha256="3714e3db8c51e43028e10ad7adffb9a36fc4aa5b1a363c2d0c4303dd1be59a7c")
    version("1.9.0", sha256="5ca5491e4260cacae30f1a5786d109230db3f3a6e5a0eb45d0d0608293d247e3")
    version("1.8.0", sha256="c45029c0a0f1a88d416af143e34de96b3091642722aa2d8c090916c6d1498c2e")

    depends_on("cxx", type="build")  # generated

    variant("shared", default=True, description="Build shared instead of static libraries")
    variant("python", default=False, description="Build with python support")

    extends("python", when="+python")
    depends_on("python@3.6:", when="+python", type=("build", "run"))
    depends_on("py-pip", when="+python", type="build")
    depends_on("py-wheel", when="+python", type="build")
    depends_on("py-setuptools", when="+python", type="build")

    # Fixes "Class-memaccess" compilation error in test
    # https://github.com/google/flatbuffers/issues/5930
    # Possibly affects earlier releases but I haven't tried to apply it.
    patch(
        "https://raw.githubusercontent.com/Flamefire/easybuild-easyconfigs/"
        "72ba2a1a0d44fbd96ded9f279373ef804bdf3903/easybuild/easyconfigs/f/"
        "flatbuffers/flatbuffers-1.12.0_replace-usage-of-memset.patch",
        sha256="094a98b5a7debbc2c60c2b235942c79e505ec76f9281f87c95d15e9ad8a97c52",
        when="@1.12.0:1%gcc@10:",
    )
    # Silences false positive "-Wstringop-overflow" on GCC 10+
    # https://github.com/google/flatbuffers/issues/5950
    # Possibly affects earlier releases but I haven't tried to apply it.
    patch(
        "https://github.com/google/flatbuffers/pull/6020.patch?full_index=1",
        sha256="579cb6fa4430d4304b93c7a1df7e922f3c3ec614c445032877ad328c209d5462",
        when="@1.12.0:1%gcc@10:",
    )

    @run_after("install")
    def python_install(self):
        if self.spec.satisfies("+python"):
            pydir = join_path(self.stage.source_path, "python")
            with working_dir(pydir):
                args = std_pip_args + ["--prefix=" + self.prefix, "."]
                pip(*args)

    def cmake_args(self):
        args = []
        args.append(self.define_from_variant("FLATBUFFERS_BUILD_SHAREDLIB", "shared"))
        args.append(f"-DFLATBUFFERS_BUILD_FLATLIB={'ON' if '+shared' not in self.spec else 'OFF'}")
        if "darwin" in self.spec.architecture:
            args.append("-DCMAKE_MACOSX_RPATH=ON")
        return args
