# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libxc(AutotoolsPackage, CudaPackage):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "https://libxc.gitlab.io"
    url = "https://gitlab.com/libxc/libxc/-/archive/6.1.0/libxc-6.1.0.tar.gz"

    license("MPL-2.0-no-copyleft-exception")

    version("6.2.2", sha256="d1b65ef74615a1e539d87a0e6662f04baf3a2316706b4e2e686da3193b26b20f")
    version("6.2.1", sha256="da96fc4f6e4221734986f49758b410ffe1d406efd3538761062a4af57a2bd272")
    version("6.2.0", sha256="31edb72c69157b6c0beaff1f10cbbb6348ce7579ef81d8f286764e5ab61194d1")
    version("6.1.0", sha256="9baf23501dca21b05fa22d8e2ffeb56f294abe19ba12584cb3f9b421ae719c5f")
    version("6.0.0", sha256="48a5393984d95bf0dd05c5ffc94e77da938b7f321058fe250c3448c7a9392c88")
    version("5.2.3", sha256="3e0b36b3b9986a621fd8850133408f6f567bd7db5636a32a68f7637e116e268c")
    version("5.1.7", sha256="1d50e1a92e59b5f3c8e7408f8612f0fb0e953d4f159515b7d81485891f3a1bbc")
    version("5.1.5", sha256="101d6ea9e013006deae074843f0d02ab2813e16734e47ff7b0551babc4497163")
    version("5.1.3", sha256="76b2abd063b692ed7e60fb6dfdf5a54072378710ee91f2b352a4e311d9805e97")
    version("5.1.2", sha256="ff13eef8184b6c61dac8933ee74fc05967de4a67489581bdc500f1ec63826aae")
    version("5.1.0", sha256="e8d2b6eb2b46b356a27f0367a7665ff276d7f295da7c734e774ee66f82e56297")
    version("5.0.0", sha256="6b3be3cf6daf6b3eddf32d4077276eb9169531b42f98c2ca28ac85b9ea408493")
    version("4.3.4", sha256="2d5878dd69f0fb68c5e97f46426581eed2226d1d86e3080f9aa99af604c65647")
    version("4.3.2", sha256="3bbe01971d0a43fb63b5c17d922388a39a3f0ae3bd37ae5f6fe31bca9ab63f3c")
    version("4.2.3", sha256="869ca4967cd255097fd2dc31664f30607e81f5abcf5f9c89bd467dc0bf93e5aa")
    version("3.0.0", sha256="df2362351280edaf2233f3b2c8eb8e6dd6c68105f152897a4cc629fa346a7396")
    version("2.2.2", sha256="6ffaad40505dbe8f155049448554b54ea31d31babf74ccf6b7935bfe55eeafd8")
    version("2.2.1", sha256="c8577ba1ddd5c28fd0aa7c579ae65ab990eb7cb51ecf9f8175f9251f6deb9a06")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("shared", default=True, description="Build shared libraries")
    variant("kxc", default=False, when="@5:", description="Build with third derivatives")
    variant("lxc", default=False, when="@5:", description="Build with fourth derivatives")

    conflicts("+shared +cuda", msg="Only ~shared supported with +cuda")
    conflicts("+cuda", when="@:4", msg="CUDA support only in libxc 5.0.0 and above")

    # Remove this if the release tarballs are available again.
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    depends_on("perl", type="build")

    patch("0001-Bugfix-avoid-implicit-pointer-cast-to-make-libxc-com.patch", when="@5.0.0")
    patch("0002-Mark-xc_erfcx-a-GPU_FUNCTION.patch", when="@5.0.0")
    patch(
        "https://raw.githubusercontent.com/cp2k/cp2k/d9e473979eaef93bf16d7abafb9f21845af16eb8/tools/toolchain/scripts/stage3/libxc-6.0.0_mgga_xc_b97mv.patch",
        sha256="938113a697ee14988ccff153e1a8287fdb78072adc4f388a0af434261082fee5",
        when="@6.0.0",
    )

    @property
    def libs(self):
        """Libxc can be queried for the following parameters:

        - "static": returns the static library version of libxc
            (by default the shared version is returned)

        :return: list of matching libraries
        """
        query_parameters = self.spec.last_query.extra_parameters

        libraries = ["libxc"]

        # Libxc installs both shared and static libraries.
        # If a client ask for static explicitly then return
        # the static libraries
        shared = self.spec.variants["shared"].value and "static" not in query_parameters

        # Libxc has a fortran90 interface: give clients the
        # possibility to query for it
        if "fortran" in query_parameters:
            if self.version < Version("4.0.0"):
                libraries = ["libxcf90"] + libraries
            else:  # starting from version 4 there is also a stable f03 iface
                libraries = ["libxcf90", "libxcf03"] + libraries

        return find_libraries(libraries, root=self.prefix, shared=shared, recursive=True)

    def setup_build_environment(self, env):
        # microarchitecture-specific optimization flags should be controlled
        # by Spack, otherwise we may end up with contradictory or invalid flags
        # see https://github.com/spack/spack/issues/17794

        # https://gitlab.com/libxc/libxc/-/issues/430 (configure script does not ensure C99)
        # TODO: Switch to cmake since this is better supported
        env.append_flags("CFLAGS", self.compiler.c99_flag)
        if self.spec.satisfies("%intel"):
            if which("xiar"):
                env.set("AR", "xiar")

        if self.spec.satisfies("%aocc"):
            env.append_flags("FCFLAGS", "-fPIC")

        if self.spec.satisfies("+cuda"):
            nvcc = self.spec["cuda"].prefix.bin.nvcc
            env.set("CCLD", "{0} -ccbin {1}".format(nvcc, spack_cc))
            env.set("CC", "{0} -x cu -ccbin {1}".format(nvcc, spack_cc))

            cuda_arch = self.spec.variants["cuda_arch"].value[0]

            if cuda_arch != "none":
                env.append_flags("CFLAGS", "-arch=sm_{0}".format(cuda_arch))

    def configure_args(self):
        args = []
        args += self.enable_or_disable("shared")
        args += self.enable_or_disable("cuda")
        if self.spec.satisfies("+kxc"):
            args.append("--enable-kxc")
        if self.spec.satisfies("+lxc"):
            args.append("--enable-lxc")
        return args

    @run_after("configure")
    def patch_libtool(self):
        """AOCC support for LIBXC"""
        if self.spec.satisfies("%aocc"):
            filter_file(
                r"\$wl-soname \$wl\$soname",
                r"-fuse-ld=ld -Wl,-soname,\$soname",
                "libtool",
                string=True,
            )

    def check(self):
        # libxc provides a testsuite, but many tests fail
        # http://www.tddft.org/pipermail/libxc/2013-February/000032.html
        pass
