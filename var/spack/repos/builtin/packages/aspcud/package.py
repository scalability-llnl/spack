# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Aspcud(CMakePackage):
    """Aspcud: Package dependency solver

    Aspcud is a solver for package dependencies. A package universe
    and a request to install, remove, or upgrade packages have to
    be encoded in the CUDF format. Such a CUDF document can then be
    passed to aspcud along with an optimization criteria to obtain
    a solution to the given package problem."""

    homepage = "https://potassco.org/aspcud"
    url = "https://github.com/potassco/aspcud/archive/v1.9.4.tar.gz"

    license("MIT")

    version("1.9.6", sha256="4dddfd4a74e4324887a1ddd7f8ff36231774fc1aa78b383256546e83acdf516c")
    version("1.9.5", sha256="9cd3a9490d377163d87b16fa1a10cc7254bc2dbb9f60e846961ac8233f3835cf")
    version("1.9.4", sha256="3645f08b079e1cc80e24cd2d7ae5172a52476d84e3ec5e6a6c0034492a6ea885")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("boost@1.74:+exception+serialization+container", type=("build"), when="@1.9.5:")
    depends_on("cmake", type=("build"))
    depends_on("re2c", type=("build"))
    depends_on("clingo")

    def cmake_args(self):
        gringo_path = join_path(self.spec["clingo"].prefix.bin, "gringo")
        clasp_path = join_path(self.spec["clingo"].prefix.bin, "clasp")
        return [
            self.define("ASPCUD_GRINGO_PATH", gringo_path),
            self.define("ASPCUD_CLASP_PATH", clasp_path),
        ]
