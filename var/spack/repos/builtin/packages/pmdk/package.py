# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Pmdk(Package):
    """The Persistent Memory Development Kit (PMDK), formerly known as NVML,
    is a library for using memory-mapped persistence, optimized specifically
    for persistent memory
    """

    homepage = "https://pmem.io/pmdk/"
    url = "https://github.com/pmem/pmdk/archive/1.12.1.tar.gz"
    git = "https://github.com/pmem/pmdk.git"
    maintainers("hyoklee")

    version("master", branch="master")
    version("1.12.1", sha256="53602e4c2439957046b428187665c5ff38cb90ca50956eb917b509a2e96909a3")
    version("1.11.0", sha256="bfbc82e6bfd788c8bcb380da76172b83732d12775a719c9c423eb2fadc78bb3a")
    version("1.10", sha256="06edcd43ef267c4cc70754d5d1a5d88aeb9f2086bc014bf2594df4c5efd8cc4e")
    version("1.9.2", sha256="6bca98ecf9e036603951024b7436d688cd1907b2d8c428373697fafff4096a4f")
    version("1.9.1", sha256="3d0ea15099d6dc7b454a67ecd0ed04d7426ff05ee0331a221cb384e293d841f0")
    version("1.9", sha256="2c8a148070f4bbf9f82e2ca63d2f84cb5101fc6e72c1ba93cc673ca3b7b95467")
    version("1.8.1", sha256="ee4e93bbf29976eac2444e4eb04a862f38b8446f7400f8f7cdcf58febf6f6ba2")
    version("1.8", sha256="a241ea76ef76d233cb92826b6823ed48091a2fb6963282a4fea848dbce68aa21")
    version("1.7.1", sha256="7e98c0522a3e96b64822902c66024e24455f4742246c679cc0f46036ef4685bc")
    version("1.7", sha256="865ce1b422bc83109cb4a63dcff8fd1077eea3617e668faf6a043208d8be03ca")
    version("1.6", sha256="3b99e6c30709326a94d2e73a9247a8dfb58d0a394c5b7714e5c3d8a3ad2e2e9f")
    version("1.5", sha256="6b069d7207febeb62440e89245e8b18fcdf40b6170d2ec2ef33c252ed16db2d4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("ndctl", default=False, description="Build components requiring ndctl")
    variant("doc", default=False, description="Build documentation")
    variant("experimental", default=False, description="Build experimental stuff")
    variant("rpmem", default=False, description="Build remote persistent memory components")

    depends_on("cmake", when="@1.12.1:")
    depends_on("pkgconfig", when="@1.12.1:")
    depends_on("ncurses", when="@1.6:")
    depends_on("libfabric", when="+rpmem")
    # documentation requires doxygen and a bunch of other dependencies
    patch("0001-make-doc-building-explicit.patch", when="@:1.7")
    patch("pmem-1.8-disable-docs.patch", when="@1.8")

    def install(self, spec, prefix):
        make_args = [
            "prefix=%s" % prefix,
            "EXTRA_CFLAGS=-Wno-error",
            "NDCTL_ENABLE={0}".format("y" if "+ndctl" in spec else "n"),
            "BUILD_RPMEM={0}".format("y" if "+rpmem" in spec else "n"),
            "DOC={0}".format("y" if "+doc" in spec else "n"),
            "EXPERIMENTAL={0}".format("y" if "+experimental" in spec else "n"),
        ]

        # pmdk prior to 1.8 was particular about the ARCH specification, must
        # be exactly "x86_64" for build to work
        if spec.target.family == "x86_64":
            make_args += ["ARCH=x86_64"]

        make("install", *make_args)
