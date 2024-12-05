# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Vdt(CMakePackage):
    """Vectorised math. A collection of fast and inline implementations of
    mathematical functions.
    """

    homepage = "https://github.com/dpiparo/vdt"
    url = "https://github.com/dpiparo/vdt/archive/v0.3.9.tar.gz"

    version("0.4.4", sha256="8b1664b45ec82042152f89d171dd962aea9bb35ac53c8eebb35df1cb9c34e498")
    version("0.4.3", sha256="705674612ebb5c182b65a8f61f4d173eb7fe7cdeee2235b402541a492e08ace1")
    version("0.3.9", sha256="1662d21037a29cae717ee50b73bd177bea79582f4138b7ad11404fc4be4e542e")
    version("0.3.8", sha256="e6d8485c3c8923993cb1b1a5bb85068a86746285058bf77faeb177363647be62")
    version("0.3.7", sha256="713a7e6d76d98f3b2b56b5216e7d5906e30f17865a5c7c889968e9a0b0664949")
    version("0.3.6", sha256="fb8f6386f2cd1eeb03db43f2b5c83a172107949bb5e5e8d4dfa603660a9757b0")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant(
        "preload",
        default=False,
        description="Create in the library the symbols to preload the library",
    )

    depends_on("python", type="build")

    @property
    def build_directory(self):
        d = join_path(self.stage.path, "spack-build")
        if self.spec.satisfies("@:0.3.8"):
            d = self.stage.source_path
        return d

    def cmake_args(self):
        spec = self.spec

        disable_features = set()
        if spec.satisfies("target=aarch64:"):
            disable_features.add("neon")
        elif spec.satisfies("target=ppc64le:"):
            disable_features.add("fma")

        args = [self.define_from_variant("PRELOAD")]
        for f in ["sse", "avx", "avx2", "fma", "neon"]:
            args.append(
                self.define(f.upper(), f not in disable_features and f in self.spec.target)
            )

        return args
