# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Gsl(AutotoolsPackage, GNUMirrorPackage):
    """The GNU Scientific Library (GSL) is a numerical library for C and C++
    programmers. It is free software under the GNU General Public License. The
    library provides a wide range of mathematical routines such as random
    number generators, special functions and least-squares fitting. There are
    over 1000 functions in total with an extensive test suite."""

    homepage = "https://www.gnu.org/software/gsl"
    gnu_mirror_path = "gsl/gsl-2.3.tar.gz"

    license("GPL-3.0-or-later")

    version("2.8", sha256="6a99eeed15632c6354895b1dd542ed5a855c0f15d9ad1326c6fe2b2c9e423190")
    version("2.7.1", sha256="dcb0fbd43048832b757ff9942691a8dd70026d5da0ff85601e52687f6deeb34b")
    version("2.7", sha256="efbbf3785da0e53038be7907500628b466152dbc3c173a87de1b5eba2e23602b")
    version("2.6", sha256="b782339fc7a38fe17689cb39966c4d821236c28018b6593ddb6fd59ee40786a8")
    version("2.5", sha256="0460ad7c2542caaddc6729762952d345374784100223995eb14d614861f2258d")
    version("2.4", sha256="4d46d07b946e7b31c19bbf33dda6204d7bedc2f5462a1bae1d4013426cd1ce9b")
    version("2.3", sha256="562500b789cd599b3a4f88547a7a3280538ab2ff4939504c8b4ac4ca25feadfb")
    version("2.2.1", sha256="13d23dc7b0824e1405f3f7e7d0776deee9b8f62c62860bf66e7852d402b8b024")
    version("2.1", sha256="59ad06837397617f698975c494fe7b2b698739a59e2fcf830b776428938a0c66")
    version("2.0", sha256="e361f0b19199b5e6c21922e9f16adf7eca8dd860842802424906d0f83485ca2d")
    version("1.16", sha256="73bc2f51b90d2a780e6d266d43e487b3dbd78945dd0b04b14ca5980fe28d2f53")

    depends_on("c", type="build")  # generated

    variant("external-cblas", default=False, description="Build against external blas")
    variant("shared", default=True, description="Build shared library")
    variant("pic", default=True, description="Enable position-independent code (PIC)")

    # from https://dev.gentoo.org/~mgorny/dist/gsl-2.3-cblas.patch.bz2
    patch("gsl-2.3-cblas.patch", when="@2.3:2.5+external-cblas")
    patch("gsl-2.6-cblas.patch", when="@2.6:2.7 +external-cblas")
    patch("gsl-2.8-cblas.patch", when="@2.8: +external-cblas")

    conflicts("+external-cblas", when="@:2.2")

    depends_on("m4", type="build", when="+external-cblas")
    depends_on("autoconf", type="build", when="+external-cblas")
    depends_on("automake", type="build", when="+external-cblas")
    depends_on("libtool", type="build", when="+external-cblas")
    depends_on("blas", when="+external-cblas")

    @property
    def force_autoreconf(self):
        # The external cblas patch touches configure
        return self.spec.satisfies("+external-cblas")

    def configure_args(self):
        configure_args = []
        if self.spec.satisfies("+external-cblas"):
            configure_args.append("--with-external-cblas")
            configure_args.append("CBLAS_CFLAGS=%s" % self.spec["blas"].headers.include_flags)
            configure_args.append("CBLAS_LIBS=%s" % self.spec["blas"].libs.ld_flags)

        configure_args.extend(self.enable_or_disable("shared"))
        configure_args.extend(self.with_or_without("pic"))

        return configure_args

    def setup_run_environment(self, env):
        # cmake looks for GSL_ROOT_DIR to find GSL so this helps pick the spack one
        # when there are multiple installations (e.g. a system one and a spack one)
        env.set("GSL_ROOT_DIR", self.prefix)
