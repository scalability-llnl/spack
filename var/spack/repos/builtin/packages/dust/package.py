# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Dust(Package):
    """du + rust = dust. Like du but more intuitive."""

    homepage = "https://github.com/bootandy/dust"
    url = "https://github.com/bootandy/dust/archive/v0.7.5.tar.gz"

    maintainers("fangohr")

    license("Apache-2.0")

    version("0.8.6", sha256="feede818e814011207c5bfeaf06dd9fc95825c59ab70942aa9b9314791c5d6b6")
    version("0.7.5", sha256="f892aaf7a0a7852e12d01b2ced6c2484fb6dc5fe7562abdf0c44a2d08aa52618")

    depends_on("rust")

    sanity_check_is_file = [join_path("bin", "dust")]

    def install(self, spec, prefix):
        cargo = which("cargo")
        cargo("install", "--root", prefix, "--path", ".")

    @run_after("install")
    def check_install(self):
        print("Attempt to call 'dust' with '--version'")
        dust = Executable(join_path(self.spec["dust"].prefix.bin, "dust"))
        output = dust("--version", output=str.split)
        print("stdout received fromm dust is '{}".format(output))
        assert "Dust " in output

    def test_run(self):
        """check dust can execute (with option '--version')"""
        dust = which(self.prefix.bin.dust)
        out = dust("--version", output=str.split, error=str.split)
        assert "Dust " in out
