# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Yosys(MakefilePackage):
    """Yosys is a framework for RTL synthesis tools. It currently has extensive
    Verilog-2005 support and provides a basic set of synthesis algorithms for
    various application domains.

    Yosys can be adapted to perform any synthesis job by combining the existing
    passes (algorithms) using synthesis scripts and adding additional passes
    as needed by extending the yosys C++ code base.

    Yosys is free software licensed under the ISC license (a GPL compatible
    license that is similar in terms to the MIT license or the 2-clause BSD license).
    """

    homepage = "https://yosyshq.net/yosys"
    url = "https://github.com/YosysHQ/yosys/archive/refs/tags/yosys-0.46.tar.gz"
    git = "https://github.com/YosysHQ/yosys.git"

    maintainers("davekeeshan")

    license("ISC")

    version("master", branch="master")

    version("0.48", commit="aaa5347494801e9e3870b31387da59da24233f76", submodules=True)
    version("0.47", commit="647d61dd9212365a3cd44db219660b8f90b95cbd", submodules=True)
    version("0.46", commit="e97731b9dda91fa5fa53ed87df7c34163ba59a41", submodules=True)
    version("0.45", commit="9ed031ddd588442f22be13ce608547a5809b62f0", submodules=True)
    version("0.44", commit="80ba43d26264738c93900129dc0aab7fab36c53f", submodules=True)
    version("0.43", commit="ead4718e567aed2e552dcfe46294b132aa04c158", submodules=True)
    version("0.42", commit="9b6afcf3f83fea413b57c3790c25ba43b9914ce2", submodules=True)
    version("0.41", sha256="b0037d0a5864550a07a72ba81346e52a7d5f76b3027ef1d7c71b975d2c8bd2b2")
    version("0.40", sha256="c1d42ad90d587b587210b40cf3c5584e41e20f656e8630c33b6583322e8b764e")
    version("0.39", sha256="a66d95747b21d03e5b9c274d3f7cb0f7dd99610891dd66920bfaee25bc30dad1")
    version("0.38", sha256="5f3d7bb12c5371db00586700a658a9196008a9457839f046403a660fe0c7a1df")
    version("0.37", sha256="98e91253b116728e5db037512a4d837529d408269358f06fe7b4633c89cf8756")
    version("0.36", sha256="d69beedcb76db80681c2a0f445046311f3ba16716d5d0c3c5034dabcb6bd9b23")
    version("0.35", sha256="a00643cf4cf83701bfa2b358066eb9d360393d30e8f5a8e65f619ab1fd10474a")
    version("0.34", sha256="57897bc3fe5fdc940e9f3f3ae03b84f5f8e9149b6f26d3699f7ecb9f31a41ae0")
    version("0.33", sha256="c240fa4fcc71c73b8989ab500f7bfa3109436fa1d7ba8d7e1028af4c42688f29")
    version("0.32", sha256="07b168491fa103a57231483a80f8e03545d0c957672e96b73d4eb9c8c8c43930")
    version("0.31", sha256="aadbd885b72a6c705035abcf7e2eb58d25689b18824ad91c71efd1d966f0bf50")
    version("0.30", sha256="1b29c9ed3d396046b67c48f0900a5f2156c6136f2e0651671d05ee26369f147d")
    version("0.29", sha256="475ba8cd06eec9050ebfd63a01e7a7c894d8f06c838b35459b7e29bbc89f4a22")
    version("0.28", sha256="36048ef3493ab43cfaac0bb89fa405715b22acd3927bf7fd3c4b25f8ad541c22")
    version("0.27", sha256="bd6c933daf48c0929b4a9b3f75713d1f79c173be4bdb82fc5d2f5feb97f3668b")
    version("0.26", sha256="e869e3770797f7edf352fd3033d5bba8606d40d6b32bae5051d917d120b9a177")
    version("0.25", sha256="673e87eecb68fd5e889ac94b93dc9ae070f1a27d94dacbd738212cf09f39578c")
    version("0.24", sha256="6a00b60e2d6bc8df0db1e66aa27af42a0694121cfcd6a3cf6f39c9329ed91263")
    version("0.23", sha256="ec982a9393b3217deecfbd3cf9a64109b85310a949e46a51cf2e07fba1071aeb")
    version("0.22", sha256="2a0c29b6f66b3ee70316dd734eceb14f452445a83ccac600b97100ffd7c7a7aa")
    version("0.21", sha256="2b0e140f47d682e1069b1ca53b1fd91cbb1c1546932bd5cb95566f59a673cd8d")
    version("0.20", sha256="ee261487badf1b554616d555da8496a7c84ef21ae66a979ddd946b6949a780a4")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    variant("abc", default=True, description="build with abc support")
    variant("ccache", default=False, description="build with ccache support")

    depends_on("automake", type="build")
    depends_on("flex")
    depends_on("bison")
    depends_on("libffi")
    depends_on("readline")
    depends_on("pkgconfig")
    depends_on("tcl")
    depends_on("zlib")
    depends_on("llvm")
    depends_on("ccache", type=("build", "run"), when="+ccache")

    def edit(self, spec, prefix):
        makefile = FileFilter("Makefile")

        makefile.filter(r"ENABLE_ABC :=", "ENABLE_ABC ?=")
        makefile.filter(r"ENABLE_CCACHE :=", "ENABLE_CCACHE ?=")

    def setup_build_environment(self, env):
        env.set("PREFIX", self.prefix)
        env.set("CXXFLAGS", f'-I{self.spec["readline"].prefix.include}')
        env.set(
            "LDFLAGS", f'-L{self.spec["readline"].prefix.lib} -L{self.spec["zlib"].prefix.lib}'
        )
        if self.spec.satisfies("+abc"):
            env.set("ENABLE_ABC", "1")
            env.set("ABC_READLINE_INCLUDES", f'-I{self.spec["readline"].prefix.include}')
        else:
            env.set("ENABLE_ABC", "0")
        if self.spec.satisfies("+ccache"):
            env.set("ENABLE_CCACHE", "1")
        else:
            env.set("ENABLE_CCACHE", "0")
