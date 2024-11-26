# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Toml11(CMakePackage):
    """toml11 is a C++11 (or later) header-only toml parser/encoder depending
    only on C++ standard library."""

    homepage = "https://github.com/ToruNiina/toml11"
    url = "https://github.com/ToruNiina/toml11/archive/refs/tags/v3.7.1.tar.gz"

    maintainers("ashermancinelli", "ToruNiina")

    license("MIT")

    version("4.0.2", sha256="d1bec1970d562d328065f2667b23f9745a271bf3900ca78e92b71a324b126070")
    version("4.0.1", sha256="96965cb00ca7757c611c169cd5a6fb15736eab1cd1c1a88aaa62ad9851d926aa")
    version("4.0.0", sha256="f3dc3095f22e38745a5d448ac629f69b7ee76d2b3e6d653e4ce021deb7f7266e")
    version("3.8.1", sha256="6a3d20080ecca5ea42102c078d3415bef80920f6c4ea2258e87572876af77849")
    version("3.8.0", sha256="36ce64b09f9151b57ba1970f12a591006fcae17b751ba011314c1f5518e77bc7")
    version("3.7.1", sha256="afeaa9aa0416d4b6b2cd3897ca55d9317084103077b32a852247d8efd4cf6068")
    version("3.7.0", sha256="a0b6bec77c0e418eea7d270a4437510884f2fe8f61e7ab121729624f04c4b58e")
    version("3.6.1", sha256="ca4c390ed8da0d77ae6eca30e70ab0bf5cc92adfc1bc2f71a2066bc5656d8d96")
    version("3.6.0", sha256="39e8d651db346ae8c7e3b39d6338a37232b9af3bba36ade45b241bf105c2226c")
    version("3.5.0", sha256="fc613874c6e80dc740134a7353cf23c7f834b59cd601af84ab535ee16a53b1c3")
    version("3.4.0", sha256="bc6d733efd9216af8c119d8ac64a805578c79cc82b813e4d1d880ca128bd154d")
    version("3.3.1", sha256="0c1b29e1a2873a1b1f6d0865a2966a2d3fd9155aeccb6139cd5af22f70b0b08f")
    version("3.3.0", sha256="b29995475922fae3095445219d36733ef18976abdc85685d0804ee3ea04f09c0")
    version("3.2.1", sha256="370f17409cfcbf3f629728ed7ec2e1573544058615fb5d066f4f7c14693143a9")
    version("3.2.0", sha256="3d54cac38ea24477190e0535377e824bf06562970ef4d35b59aa9729437e1019")
    version("3.1.0", sha256="3a118f32e5343998f37be9807c72fd11c3168fe12a5b1abfdc0f1e60de6380a4")

    depends_on("cxx", type="build")  # generated

    variant(
        "cxx_std", default="11", description="C++ standard", values=("11", "14", "17"), multi=False
    )

    @when("@3.8.0:")
    def cmake_args(self):
        args = [self.define_from_variant("CMAKE_CXX_STANDARD", "cxx_std")]
        return args
