# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re
import sys

from spack.package import *


class Hwloc(AutotoolsPackage, CudaPackage, ROCmPackage):
    """The Hardware Locality (hwloc) software project.

    The Portable Hardware Locality (hwloc) software package
    provides a portable abstraction (across OS, versions,
    architectures, ...) of the hierarchical topology of modern
    architectures, including NUMA memory nodes, sockets, shared
    caches, cores and simultaneous multithreading. It also gathers
    various system attributes such as cache and memory information
    as well as the locality of I/O devices such as network
    interfaces, InfiniBand HCAs or GPUs. It primarily aims at
    helping applications with gathering information about modern
    computing hardware so as to exploit it accordingly and
    efficiently.
    """

    homepage = "https://www.open-mpi.org/projects/hwloc/"
    url = "https://download.open-mpi.org/release/hwloc/v2.11/hwloc-2.11.1.tar.bz2"
    git = "https://github.com/open-mpi/hwloc.git"

    maintainers("bgoglin")

    license("BSD-3-Clause")

    executables = ["^hwloc-bind$"]

    version("master", branch="master")
    version("2.11.1", sha256="9f320925cfd0daeaf3a3d724c93e127ecac63750c623654dca0298504aac4c2c")
    version("2.10.0", sha256="c7fd8a1404a9719c76aadc642864b9f77aed1dc1fc8882d6af861a9260ba240d")
    version("2.9.3", sha256="5985db3a30bbe51234c2cd26ebe4ae9b4c3352ab788b1a464c40c0483bf4de59")
    version("2.9.2", sha256="ffb554d5735e0e0a19d1fd4b2b86e771d3b58b2d97f257eedacae67ade5054b3")
    version("2.9.1", sha256="a440e2299f7451dc10a57ddbfa3f116c2a6c4be1bb97c663edd3b9c7b3b3b4cf")
    version("2.9.0", sha256="9d7d3450e0a5fea4cb80ca07dc8db939abb7ab62e2a7bb27f9376447658738ec")
    version("2.8.0", sha256="20b2bd4df436827d8e50f7afeafb6f967259f2fb374ce7330244f8d0ed2dde6f")
    version("2.7.1", sha256="4cb0a781ed980b03ad8c48beb57407aa67c4b908e45722954b9730379bc7f6d5")
    version("2.7.0", sha256="d9b23e9b0d17247e8b50254810427ca8a9857dc868e2e3a049f958d7c66af374")
    version("2.6.0", sha256="9aa7e768ed4fd429f488466a311ef2191054ea96ea1a68657bc06ffbb745e59f")
    version("2.5.0", sha256="38aa8102faec302791f6b4f0d23960a3ffa25af3af6af006c64dbecac23f852c")
    version("2.4.1", sha256="4267fe1193a8989f3ab7563a7499e047e77e33fed8f4dec16822a7aebcf78459")
    version("2.4.0", sha256="30404065dc1d6872b0181269d0bb2424fbbc6e3b0a80491aa373109554006544")
    version("2.3.0", sha256="155480620c98b43ddf9ca66a6c318b363ca24acb5ff0683af9d25d9324f59836")
    version("2.2.0", sha256="2defba03ddd91761b858cbbdc2e3a6e27b44e94696dbfa21380191328485a433")
    version("2.1.0", sha256="1fb8cc1438de548e16ec3bb9e4b2abb9f7ce5656f71c0906583819fcfa8c2031")
    version("2.0.4", sha256="efadca880f5a59c6d5d6f7bc354546aa6f780d77cc2e139634c3de9564e7ce1f")
    version("2.0.3", sha256="64def246aaa5b3a6e411ce10932a22e2146c3031b735c8f94739534f06ad071c")
    version("2.0.2", sha256="27dcfe42e3fb3422b72ce48b48bf601c0a3e46e850ee72d9bdd17b5863b6e42c")
    version("2.0.1", sha256="f1156df22fc2365a31a3dc5f752c53aad49e34a5e22d75ed231cd97eaa437f9d")
    version("2.0.0", sha256="a0d425a0fc7c7e3f2c92a272ffaffbd913005556b4443e1887d2e1718d902887")
    version("1.11.13", sha256="a8f781ae4d347708a07d95e7549039887f151ed7f92263238527dfb0a3709b9d")
    version("1.11.12", sha256="f1d49433e605dd653a77e1478a78cee095787d554a94afe40d1376bca6708ca5")
    version("1.11.11", sha256="74329da3be1b25de8e98a712adb28b14e561889244bf3a8138afe91ab18e0b3a")
    version("1.11.10", sha256="0a2530b739d9ebf60c4c1e86adb5451a20d9e78f7798cf78d0147cc6df328aac")
    version("1.11.9", sha256="85b978995b67db0b1a12dd1a73b09ef3d39f8e3cb09f8b9c60cf04633acce46c")
    version("1.11.8", sha256="8af89b1164a330e36d18210360ea9bb305e19f9773d1c882855d261a13054ea8")
    version("1.11.7", sha256="ac16bed9cdd3c63bca1fe1ac3de522a1376b1487c4fc85b7b19592e28fd98e26")
    version("1.11.6", sha256="67963f15197e6b551539c4ed95a4f8882be9a16cf336300902004361cf89bdee")
    version("1.11.5", sha256="da2c780fce9b5440a1a7d1caf78f637feff9181a9d1ca090278cae4bea71b3df")
    version("1.11.4", sha256="1b6a58049c31ce36aff162cf4332998fd468486bd08fdfe0249a47437311512d")
    version("1.11.3", sha256="03a1cc63f23fed7e17e4d4369a75dc77d5c145111b8578b70e0964a12712dea0")
    version("1.11.2", sha256="d11f091ed54c56c325ffca1083113a405fcd8a25d5888af64f5cd6cf587b7b0a")
    version("1.11.1", sha256="b41f877d79b6026640943d57ef25311299378450f2995d507a5e633da711be61")
    version("1.9", sha256="9fb572daef35a1c8608d1a6232a4a9f56846bab2854c50562dfb9a7be294f4e8")

    variant("nvml", default=False, description="Support NVML device discovery")
    variant("gl", default=False, description="Support GL device discovery")
    variant("libxml2", default=True, description="Build with libxml2")
    variant("libudev", default=False, when="@1.11.0:", description="Build with libudev")
    variant(
        "pci",
        default=(sys.platform != "darwin"),
        description="Support analyzing devices on PCI bus",
    )
    variant(
        "libs",
        default="shared,static",
        values=("shared", "static"),
        multi=True,
        description="Build shared libs, static libs or both",
    )
    variant(
        "cairo", default=False, description="Enable the Cairo back-end of hwloc's lstopo command"
    )
    variant(
        "netloc", default=False, when="@2.0.0:2.9.3", description="Enable netloc [requires MPI]"
    )
    variant("opencl", default=False, description="Support an OpenCL library at run time")
    variant("rocm", default=False, description="Support ROCm devices")
    variant(
        "oneapi-level-zero", default=False, description="Support Intel OneAPI Level Zero devices"
    )

    depends_on("c", type="build")
    depends_on("cxx", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("m4", type="build", when="@master")
    depends_on("autoconf", type="build", when="@master")
    depends_on("automake", type="build", when="@master")
    depends_on("libtool", type="build", when="@master")
    depends_on("cuda", when="+nvml")
    depends_on("cuda", when="+cuda")
    depends_on("gl", when="+gl")
    depends_on("libpciaccess", when="+pci")
    depends_on("libxml2", when="+libxml2")
    depends_on("cairo", when="+cairo")
    depends_on("numactl", when="@:1.11.11 platform=linux")
    depends_on("ncurses")

    # Before 2.2 hwloc does not consider linking to libtinfo
    # to detect ncurses, which is considered a bug.
    # For older versions this can be fixed by depending on
    # ncurses~termlib, but this could lead to insatisfiable
    # constraints (e.g. llvm explicitly depends on ncurses+termlib)
    # Therefore we patch the latest 1.x configure script to make
    # it consider libtinfo too.
    # see https://github.com/open-mpi/hwloc/pull/417
    patch("0001-Try-linking-to-libtinfo.patch", when="@1.11.13")
    depends_on("ncurses ~termlib", when="@2.0:2.2")
    depends_on("ncurses ~termlib", when="@1.0:1.11.12")

    # When mpi=openmpi, this introduces an unresolvable dependency.
    # See https://github.com/spack/spack/issues/15836 for details
    depends_on("mpi", when="+netloc")

    with when("+rocm"):
        depends_on("rocm-smi-lib")
        depends_on("rocm-opencl", when="+opencl")
        # Avoid a circular dependency since the openmp
        # variant of llvm-amdgpu depends on hwloc.
        depends_on("llvm-amdgpu", when="+opencl")

    with when("+oneapi-level-zero"):
        depends_on("oneapi-level-zero")
        # LevelZero support isn't available until hwloc version 2.5.0
        conflicts("@:2.4.99", msg="hwloc supports Intel OneAPI Level Zero only since 2.5.0")

    @classmethod
    def determine_version(cls, exe):
        output = Executable(exe)("--version", output=str, error=str)
        match = re.search(r"hwloc-bind (\S+)", output)
        return match.group(1) if match else None

    def url_for_version(self, version):
        url = "https://download.open-mpi.org/release/hwloc/v{0}/hwloc-{1}.tar.gz"
        return url.format(version.up_to(2), version)

    @property
    def libs(self):
        libs = find_libraries("libhwloc", root=self.prefix, shared=True, recursive=True)
        return LibraryList(libs)

    def configure_args(self):
        args = []

        # If OpenCL is not enabled, disable it since hwloc might
        # pick up an OpenCL library at build time that is then
        # not found at run time.
        # The OpenCl variant allows OpenCl providers such as
        # 'cuda' and 'rocm-opencl' to be used.
        if "+opencl" not in self.spec:
            args.append("--disable-opencl")

        # If ROCm libraries are found in system /opt/rocm
        # during config stage, hwloc builds itself with
        # librocm_smi support.
        # This can fail the config tests while building
        # OpenMPI due to lack of rpath to librocm_smi
        if "+rocm" not in self.spec:
            args.append("--disable-rsmi")

        if self.spec.satisfies("+rocm"):
            args.append("--with-rocm={0}".format(self.spec["hip"].prefix))
            args.append("--with-rocm-version={0}".format(self.spec["hip"].version))

        args.extend(self.enable_or_disable("netloc"))
        args.extend(self.enable_or_disable("cairo"))
        args.extend(self.enable_or_disable("nvml"))
        args.extend(self.enable_or_disable("gl"))
        args.extend(self.enable_or_disable("cuda"))
        args.extend(self.enable_or_disable("libxml2"))
        args.extend(self.enable_or_disable("libudev"))
        args.extend(self.enable_or_disable("pci"))
        args.extend(self.enable_or_disable("libs"))

        if self.spec.satisfies("+cuda"):
            args.append("--with-cuda={0}".format(self.spec["cuda"].prefix))
            args.append("--with-cuda-version={0}".format(self.spec["cuda"].version))

        if self.spec.satisfies("+oneapi-level-zero"):
            args.append("--enable-levelzero")
        else:
            args.append("--disable-levelzero")

        return args
