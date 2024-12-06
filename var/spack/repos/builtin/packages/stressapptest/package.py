# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Stressapptest(AutotoolsPackage):
    """
    Stressful Application Test (or stressapptest, its unix name) is a memory
    interface test. It tries to maximize randomized traffic to memory from
    processor and I/O, with the intent of creating a realistic high load
    situation in order to test the existing hardware devices in a computer.
    It has been used at Google for some time and now it is available under the
    apache 2.0 license."""

    homepage = "https://github.com/stressapptest/stressapptest"
    url = "https://github.com/stressapptest/stressapptest/archive/refs/tags/v1.0.9.tar.gz"
    maintainers("saqibkh")

    license("Apache-2.0")

    version("1.0.9", sha256="2ba470587ad4f6ae92057d427c3a2a2756e5f10bd25cd91e62eaef55a40b30a1")
    version("1.0.8", sha256="b0432f39055166156ed04eb234f3c226b17a42f802a3f81d76ee999838e205df")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
