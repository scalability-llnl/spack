# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Changa(AutotoolsPackage, CudaPackage):
    """ChaNGa (Charm N-body GrAvity solver) is a code to perform collisionless
    N-body simulations.
    """

    homepage = "https://faculty.washington.edu/trq/hpcc/tools/changa.html"
    url = "https://github.com/N-BodyShop/changa/archive/v3.4.tar.gz"
    git = "https://github.com/N-BodyShop/changa.git"

    license("GPL-2.0-or-later")

    version("master", branch="master")
    version("3.5", sha256="8c49ab5b540a8adb23d3eaa80942621e5ac83244918e66c87886c9d3fb463d39")
    version("3.4", sha256="c2bceb6ac00025dfd704bb6960bc17c6df7c746872185845d1e75f47e6ce2a94")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    patch("fix_configure_path.patch")
    # Version 3.5 assumes to have a git repository available to compute the current version
    # using `git describe ...` Since we are installing from the release tarball, hardcode
    # the version to 3.5
    patch("fix_makefile.patch", when="@3.5")

    resource(
        name="utility",
        url="https://github.com/N-BodyShop/utility/archive/v3.4.tar.gz",
        sha256="19f9f09023ce9d642e848a36948788fb29cd7deb8e9346cdaac4c945f1416667",
        placement="utility",
        when="@3.4",
    )

    resource(
        name="utility",
        git="https://github.com/N-BodyShop/utility.git",
        commit="f947639f78162a68d697195e6963328f2665bf44",
        placement="utility",
        when="@3.5",
    )

    depends_on("charmpp build-target=ChaNGa")
    depends_on("charmpp +cuda", when="+cuda")
    depends_on("libjpeg")
    depends_on("zlib-api")

    parallel = False

    def setup_build_environment(self, env):
        env.set("CHARM_DIR", self.spec["charmpp"].prefix)

    def configure_args(self):
        args = [f"STRUCT_DIR={self.stage.source_path}/utility/structures"]
        if "avx" in self.spec.target:
            args.append("--enable-arch=avx")
        if self.spec.satisfies("+cuda"):
            args.append(f"--with-cuda={self.spec['cuda'].prefix}")
        return args

    def install(self, spec, prefix):
        with working_dir(self.build_directory):
            mkdirp(prefix.bin)
            install("ChaNGa", prefix.bin)
            install("charmrun", prefix.bin)
