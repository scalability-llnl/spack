# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Lhapdf(AutotoolsPackage):
    """LHAPDF is a general purpose C++ interpolator,
    used for evaluating PDFs from discretised data files."""

    homepage = "https://lhapdf.hepforge.org/"
    git = "https://gitlab.com/hepcedar/lhapdf"
    # the tarballs from hepforge include bundled cython sources
    # that may break the build when using incompatible python versions
    # thus use the release tarball from gitlab that does not include lhapdf.cxx
    url = "https://gitlab.com/hepcedar/lhapdf/-/archive/lhapdf-6.4.0/lhapdf-lhapdf-6.4.0.tar.gz"

    tags = ["hep"]

    maintainers("vvolkl", "wdconinc")

    license("GPL-3.0-or-later")

    version("6.5.4", sha256="ace8913781044ad542e378697fcd95a8535d510818bb74a6665f9fd2b132ac0f")
    version("6.5.3", sha256="90fe7254d5a48a9b2d424fcbac1bf9708b0e54690efec4c78e9ad28b9203bfcd")
    version("6.5.2", sha256="23972ec46289c82a63df60b55b62f219418b4d80f94b8d570feb2b5e48014054")
    version("6.5.1", sha256="7a19ba4cdee7053bb79db317143fe768dd6abef1ec34e2d183225e13df96a983")
    version("6.4.0", sha256="155702c36df46de30c5f7fa249193a9a0eea614191de1606301e06cd8062fc29")
    version("6.3.0", sha256="864468439c7662bbceed6c61c7132682ec83381a23c9c9920502fdd7329dd816")
    version("6.2.3", sha256="37200a1ab70247250a141dfed7419d178f9a83bd23a4f8a38e203d4e27b41308")

    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("python", default=True, description="Build python bindings")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    extends("python", when="+python")
    depends_on("py-cython", type="build", when="+python")
    depends_on("py-setuptools", type="build", when="+python")
    depends_on("gettext", type="build", when="+python")

    def setup_build_environment(self, env):
        # Add -lintl if provided by gettext, otherwise libintl is provided by the system's glibc:
        if (
            self.spec.satisfies("+python")
            and self.spec.satisfies("^gettext")
            and "intl" in self.spec["gettext"].libs.names
        ):
            env.append_flags("LDFLAGS", "-L" + self.spec["gettext"].prefix.lib)

    def configure_args(self):
        args = ["FCFLAGS=-O3", "CFLAGS=-O3", "CXXFLAGS=-O3"]

        if self.spec.satisfies("+python"):
            args.append(
                "LIBS=-L"
                + self.spec["python"].prefix.lib
                + " -L"
                + self.spec["gettext"].prefix.lib
            )

        args.extend(self.enable_or_disable("python"))
        return args
