# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class KimApi(CMakePackage):
    """OpenKIM is an online framework for making molecular simulations
    reliable, reproducible, and portable. Computer implementations of
    inter-atomic models are archived in OpenKIM, verified for coding
    integrity, and tested by computing their predictions for a variety
    of material properties.  Models conforming to the KIM application
    programming interface (API) work seamlessly with major simulation
    codes that have adopted the KIM API standard.

    This package provides the kim-api library and supporting
    utilities.  It also provides a small set of example models.

    To obtain all models archived at https://openkim.org that are
    compatible with the kim-api package, install and activate the
    openkim-models package too.
    """

    extendable = True
    homepage = "https://openkim.org/"
    url = "https://s3.openkim.org/kim-api/kim-api-2.2.1.txz"
    git = "https://github.com/openkim/kim-api.git"

    maintainers("ellio167")

    license("CDDL-1.0")

    version("develop", branch="devel")
    version("2.2.1", sha256="1d5a12928f7e885ebe74759222091e48a7e46f77e98d9147e26638c955efbc8e")
    version("2.1.3", sha256="88a5416006c65a2940d82fad49de0885aead05bfa8b59f87d287db5516b9c467")
    version("2.1.2", sha256="16c7dd362cf95288b6288e1a76caf8baef652eb2cf8af500a5eb4767ba2fe80c")
    version("2.1.1", sha256="25c4e83c6caa83a1c4ad480b430f1926fb44813b64f548fdaedc45e310b5f6b9")
    version("2.1.0", sha256="d6b154b31b288ec0a5643db176950ed71f1ca83a146af210a1d5d01cce8ce958")
    version("2.0.2", sha256="26e7cf91066692f316b8ba1548ccb7152bf56aad75902bce2338cff53e74e63d")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated
    # The Fujitsu compiler requires the '--linkfortran'
    # option to combine C++ and Fortran programs.
    patch("fujitsu_add_link_flags.patch", when="%fj")

    def patch(self):
        # Remove flags not recognized by the NVIDIA compiler
        if self.spec.satisfies("%nvhpc"):
            filter_file(
                "-std=gnu", "", "examples/simulators/simulator-model-example/CMakeLists.txt"
            )

    def cmake_args(self):
        args = [self.define("CMAKE_INSTALL_SYSCONFDIR", self.prefix.etc)]
        return args
