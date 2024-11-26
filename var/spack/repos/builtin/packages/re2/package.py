# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Re2(CMakePackage):
    """RE2 is a fast, safe, thread-friendly alternative to backtracking
    regular expression engines like those used in PCRE, Perl, and Python."""

    homepage = "https://github.com/google/re2"
    url = "https://github.com/google/re2/archive/2020-08-01.tar.gz"

    license("BSD-3-Clause", checked_by="wdconinc")

    version(
        "2024-07-02", sha256="eb2df807c781601c14a260a507a5bb4509be1ee626024cb45acbd57cb9d4032b"
    )
    version(
        "2024-06-01", sha256="7326c74cddaa90b12090fcfc915fe7b4655723893c960ee3c2c66e85c5504b6c"
    )
    version(
        "2024-05-01", sha256="fef2f366578401eada34f5603679fb2aebe9b409de8d275a482ce5f2cbac2492"
    )
    version(
        "2024-04-01", sha256="3f6690c3393a613c3a0b566309cf04dc381d61470079b653afc47c67fb898198"
    )
    version(
        "2024-03-01", sha256="7b2b3aa8241eac25f674e5b5b2e23d4ac4f0a8891418a2661869f736f03f57f4"
    )
    version(
        "2024-02-01", sha256="cd191a311b84fcf37310e5cd876845b4bf5aee76fdd755008eef3b6478ce07bb"
    )
    version(
        "2023-11-01", sha256="4e6593ac3c71de1c0f322735bc8b0492a72f66ffccfad76e259fa21c41d27d8a"
    )
    version(
        "2023-09-01", sha256="5bb6875ae1cd1e9fedde98018c346db7260655f86fdb8837e3075103acd3649b"
    )
    version(
        "2021-06-01", sha256="26155e050b10b5969e986dab35654247a3b1b295e0532880b5a9c13c0a700ceb"
    )
    version(
        "2020-08-01", sha256="6f4c8514249cd65b9e85d3e6f4c35595809a63ad71c5d93083e4d1dcdf9e0cd6"
    )
    version(
        "2020-04-01", sha256="98794bc5416326817498384a9c43cbb5a406bab8da9f84f83c39ecad43ed5cea"
    )

    depends_on("cxx", type="build")

    variant(
        "icu",
        default=False,
        description="Build against ICU for full Unicode properties support",
        when="@2023-02-01:",
    )
    variant("shared", default=False, description="Build shared instead of static libraries")
    variant("pic", default=True, description="Enable position independent code")

    depends_on("abseil-cpp", when="@2023-09-01:")

    depends_on("icu4c", when="+icu")

    depends_on("googletest", type="test")
    depends_on("benchmark ~performance_counters", type="test")

    # shared libs must have position-independent code
    conflicts("+shared ~pic")

    def cmake_args(self):
        args = [
            self.define_from_variant("RE2_USE_ICU", "icu"),
            self.define_from_variant("BUILD_SHARED_LIBS", "shared"),
            self.define_from_variant("CMAKE_POSITION_INDEPENDENT_CODE", "pic"),
            self.define("RE2_BUILD_TESTING", self.run_tests),
        ]

        abseil = self.spec.dependencies("abseil-cpp")

        if abseil:
            args.append(self.define("CMAKE_CXX_STANDARD", abseil[0].variants["cxxstd"].value))
        return args
