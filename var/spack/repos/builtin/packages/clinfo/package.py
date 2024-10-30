# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Clinfo(MakefilePackage):
    """Print all known information about all available OpenCL platforms and
    devices in the system."""

    homepage = "https://github.com/Oblomov/clinfo"
    url = "https://github.com/Oblomov/clinfo/archive/2.2.18.04.06.tar.gz"

    maintainers("matthiasdiener")

    license("CC0-1.0")

    version(
        "3.0.23.01.25", sha256="6dcdada6c115873db78c7ffc62b9fc1ee7a2d08854a3bccea396df312e7331e3"
    )
    version(
        "3.0.21.02.21", sha256="e52f5c374a10364999d57a1be30219b47fb0b4f090e418f2ca19a0c037c1e694"
    )
    version(
        "3.0.20.11.20", sha256="3c506083e72e9ee09fc7d5de513be7c5eff0284f198a60fb60ab493f6f0a549a"
    )
    version(
        "2.2.18.04.06", sha256="f77021a57b3afcdebc73107e2254b95780026a9df9aa4f8db6aff11c03f0ec6c"
    )

    depends_on("c", type="build")  # generated

    depends_on("opencl")

    def install(self, spec, prefix):
        make("install", "PREFIX={0}".format(prefix))
