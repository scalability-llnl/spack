# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Amdsmi(CMakePackage):
    """The AMD System Management Interface Library, or AMD SMI library,
    is a C library for Linux that provides a user space interface for
    applications to monitor and control AMD device."""

    homepage = "https://github.com/ROCm/amdsmi"
    url = "https://github.com/ROCm/amdsmi/archive/refs/tags/rocm-6.1.2.tar.gz"

    tags = ["rocm"]
    maintainers("srekolam", "renjithravindrankannath")
    libraries = ["libamd_smi"]

    license("MIT")
    version("6.2.1", sha256="136941e3f13e0d373ee3698bd60d4fc36353a2df6406e5a50b6ac78f1b639698")
    version("6.2.0", sha256="49e4b15af62bf9800c02a24c75c6cd99dc8b146d69cc7f00ecbbcd60f6106315")
    version("6.1.2", sha256="4583ea9bc71d55e987db4a42f9b3b730def22892953d30bca64ca29ac844e058")
    version("6.1.1", sha256="10ece6b1ca8bb36ab3ae987fc512838f30a92ab788a2200410e9c1707fe0166b")
    version("6.1.0", sha256="5bd1f150a2191b1703ff2670e40f6fed730f59f155623d6e43b7f64c39ae0967")
    version("6.0.2", sha256="aeadf07750def0325a0eaa29e767530b2ec94f3d45dc3b7452fd7a2493769428")
    version("6.0.0", sha256="2626e3af9d60dec245c61af255525a0c0841a73fb7ec2836477c0ce5793de39c")
    version("5.7.0", sha256="144391d537710dafa9ef69571dd76203e56db6142ab61a1375346b5733137e23")
    version("5.6.0", sha256="595c9d6d79d9071290b2f19ab4ef9222c8d2983b4322b3143fcd9d0b1ce0f6d8")
    version("5.5.1", sha256="b794c7fd562fd92f2c9f2bbdc2d5dded7486101fcd4598f2e8c3484c9a939281")
    version("5.5.0", sha256="dcfbd96e93afcf86b1261464e008e9ef7e521670871a1885e6eaffc7cdc8f555")

    depends_on("cxx", type="build")  # generated

    depends_on("cmake@3.11:")
    depends_on("python@3.6:")
    depends_on("py-virtualenv")
    depends_on("pkgconfig")
    depends_on("libdrm")
    depends_on("py-pyyaml")

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r"lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)", lib)
        if match:
            ver = "{0}.{1}.{2}".format(
                int(match.group(1)), int(match.group(2)), int(match.group(3))
            )
        else:
            ver = None
        return ver

    def cmake_args(self):
        args = []
        args.append(self.define("BUILD_TESTS", "ON"))
        args.append("-DCMAKE_INSTALL_LIBDIR=lib")
        return args
