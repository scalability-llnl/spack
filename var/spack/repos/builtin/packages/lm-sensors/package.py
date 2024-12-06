# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class LmSensors(MakefilePackage):
    """The lm-sensors package provides user-space support for the
    hardware monitoring drivers in Linux."""

    homepage = "https://github.com/groeck/lm-sensors/"
    url = "https://github.com/groeck/lm-sensors/archive/V3-4-0.tar.gz"
    maintainers("G-Ragghianti")

    license("LGPL-2.1-or-later AND GPL-2.0-or-later")

    version("3-6-0", sha256="0591f9fa0339f0d15e75326d0365871c2d4e2ed8aa1ff759b3a55d3734b7d197")
    version("3-5-0", sha256="f671c1d63a4cd8581b3a4a775fd7864a740b15ad046fe92038bcff5c5134d7e0")
    version("3-4-0", sha256="e334c1c2b06f7290e3e66bdae330a5d36054701ffd47a5dde7a06f9a7402cb4e")
    version("3-3-5", sha256="e3802f80785c54822027a8c187b10066ba685ec5e997fd02c1d29761ea9c83d4")
    version("3-3-4", sha256="1c586684b39292b5fabaf5a2701241885ea6483e5e15265e1f501e1b639fdd86")
    version("3-3-3", sha256="f1c1078afc712693f003989446b59d817794ed7eb733b401c83ed6b1d7d45b73")
    version("3-3-2", sha256="927f841e42afb16b35a313a02825122d3a5be59d4b6c567fd90caf23eeda30a8")
    version("3-3-1", sha256="769b8649e4da2739c07c9a1b2975a8efe6aa9b69cd65fe350ccccbafd4821d95")
    version("3-3-0", sha256="35ed28640cb2cd1492c4d6620a7c6b8dd2fa44fbb603d5f4d867311e8f56dd37")
    version("3-2-0", sha256="ff54bee654f9f317224489fa64aeb659425d58ac3d031fe019c2c072ba19ee9a")
    version("3-1-2", sha256="a587f4f37c0f32ac48575338013ee443a0152d87543e8e702db6161ec0ca1161")
    version("3-1-1", sha256="22b5ab0bab853c34298ff617efb292c5dde7b254596b31ce4c6e90b1d1cf8ad8")

    depends_on("c", type="build")  # generated

    depends_on("bison", type="build")
    depends_on("flex", type="build")
    depends_on("perl", type="run")

    @property
    def build_targets(self):
        targets = []

        targets.append("CC={0}".format(spack_cc))

        return targets

    def install(self, spec, prefix):
        make("install", "PREFIX={0}".format(prefix), "ETCDIR={0}/etc".format(prefix))

    @property
    def libs(self):
        return find_libraries("libsensors", root=self.prefix, shared=True, recursive=True)
