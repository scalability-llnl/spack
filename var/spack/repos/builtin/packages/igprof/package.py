# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Igprof(CMakePackage):
    """IgProf (the Ignominous Profiler) is a simple nice tool for measuring and
    analysing application memory and performance characteristics.

    IgProf requires no changes to the application or the build process. It
    currently works on Linux (ia32, x86_64)."""

    homepage = "https://igprof.org/"
    url = "https://github.com/igprof/igprof/archive/v5.9.16.tar.gz"

    version("5.9.18", sha256="f3e378a358469cd269aa5cb3312adc4f5ca89b90c0de89dc070d803c6b68f7b5")
    version("5.9.16", sha256="cc977466b310f47bbc2967a0bb6ecd49d7437089598346e3f1d8aaf9a7555d96")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    depends_on("libunwind")

    # Three patches in one: C++11 compatibility (src/analyse.cc),
    # libunwind "compatibility" (remove -Werror in CMakeLists.txt) -
    # see also https://github.com/spack/spack/pull/21537,
    # and gcc 8.x compatibility (the rest of the changes).
    # Adopted from LCGCMake https://gitlab.cern.ch/sft/lcgcmake
    patch("igprof-5.9.16.patch", when="@5.9.16", level=0)

    def build_system_flags(pkg, name, flags):
        if name == "cxxflags":
            flags.extend(("-Wno-unused-variable", "-Wno-error=unused-result"))

        return (None, None, flags)
