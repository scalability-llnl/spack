# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Activeharmony(MakefilePackage):
    """Active Harmony: a framework for auto-tuning (the automated search for
    values to improve the performance of a target application)."""

    homepage = "https://github.com/ActiveHarmony/harmony"
    url = "https://github.com/ActiveHarmony/harmony/archive/refs/tags/v4.5.tar.gz"

    license("LGPL-3.0-only")

    version("4.6.0", sha256="01011c0c455fca31e5806b03743e27a12161c152253370894876f851242ccd51")
    version("4.5", sha256="74bde94f6c4f710a5003b0111f27fe3ba98161505e0155a87e94dd209b586951")

    patch(
        "fix_logical_bug_in_slave_list_parsing.patch",
        sha256="3e000616f84de80b262efcae7559d65eed0efcd53e915580dab63b0ffbbb8bf2",
        when="@4.6.0",
    )

    cflags = ["-O3", "-fPIC"]

    def setup_build_environment(self, spack_env):
        spack_env.set("CFLAGS", " ".join(self.cflags))

    @when("@:4.5")
    def install(self, spec, prefix):
        make("install", f"PREFIX={prefix}")

    @when("@4.6.0:")
    def install(self, spec, prefix):
        make("install")
        install_tree("./bin", prefix.bin)
        install("./src/harmony.cfg", prefix.bin)
        install_tree("./lib", prefix.lib)
        install_tree("./libexec", prefix.libexec)
        install_tree("./include", prefix.include)
        install_tree("./doc", prefix.doc)
