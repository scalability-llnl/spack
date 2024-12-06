# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Actsvg(CMakePackage):
    """An SVG based C++17 plotting library for ACTS detectors and
    surfaces."""

    homepage = "https://github.com/acts-project/actsvg"
    url = "https://github.com/acts-project/actsvg/archive/refs/tags/v0.4.22.zip"
    list_url = "https://github.com/acts-project/actsvg/tags"
    git = "https://github.com/acts-project/actsvg.git"

    maintainers("wdconinc", "stephenswat")

    license("MPL-2.0")

    version("0.4.50", sha256="c97fb1cc75cbf23caebd3c6fb8716354bdbd0a77ad39dc43dae963692f3256e1")
    version("0.4.48", sha256="0f230c31c64b939e4d311afd997dbaa87a375454cf1595661a449b97943412c9")
    version("0.4.47", sha256="11924fddbdd01f6337875797dc3a97b62be565688e678485e992bcfc9bfb142f")
    version("0.4.46", sha256="0b75e91de240aeac8b91cd4fb8e314d0ab2a4b220048fb373dee9352d571b792")
    version("0.4.45", sha256="402ca863e453055e5abc65a37908f44b03b15f90c694807d78627d7800d2e39c")
    version("0.4.44", sha256="6eda7306b8b863e1860e090f328ac6e7982dc2d3b3d674db2799c13007ffd07f")
    version("0.4.43", sha256="e2aef32185db37cfdc023282b25c003e63dc974a11118ab2040bd30b2d346147")
    version("0.4.42", sha256="a8439d50b469ccc4428973507db1adf56aa68b34900ce0c6077ddb92a133a4f2")
    version("0.4.41", sha256="c675795e74efcf42c3015d6efc8d7a1848b677f1d4efe6dcaa4fb490b46268ff")
    version("0.4.40", sha256="e24f51e70cff57c74d3b5f51c08f6ea1f409ef85ef7b4bad4a29520ecda032a6")
    version("0.4.39", sha256="2d9605ecf8c9975d600cafb6d076969d77c634fa92844bd9586c38066da31739")
    version("0.4.35", sha256="693a4cc0e702842072a478c913895ed3596350ffdfa87f5d296ddd6ea36b61c6")
    version("0.4.33", sha256="25c93b8382bdb1864b4d8de64b146fe8ea86eec84048d594c375700d2fff1d1d")
    version("0.4.30", sha256="f7ffea39b3132914fcbb0fac6ab7395bef295cd6078dfd1c2509fd2d9aab0acb")
    version("0.4.29", sha256="971f4f344c3143b654e6a86422534c6916f785f2c2c3785664c4ae7ddf2f5e4b")
    version("0.4.28", sha256="12c6f0c41b1aeb21164c949498819976bf91a395968debcb400539713bdfc6b0")
    version("0.4.27", sha256="f4b06ad6d0f424505f3b1315503c3197bebb24c900a498bda12c453919b06d27")
    version("0.4.26", sha256="a1dfad15b616cac8191a355c1a87544571c36349400e3de56b9e5be6fa73714c")

    variant("examples", default=False, description="Build the example applications")
    variant("meta", default=True, description="Build the meta level interface")
    variant("python", default=True, when="@0.4.39:", description="Build the python bindings")
    variant(
        "web", default=True, when="@0.4.36:", description="Build the webpage builder interface"
    )

    depends_on("boost +program_options", type="test")
    depends_on("boost +program_options", when="+examples")
    depends_on("googletest", when="+examples")
    depends_on("python@3.8:", when="+python")

    def cmake_args(self):
        args = [
            self.define_from_variant("ACTSVG_BUILD_EXAMPLES", "examples"),
            self.define_from_variant("ACTSVG_BUILD_META", "meta"),
            self.define_from_variant("ACTSVG_BUILD_PYTHON_BINDINGS", "python"),
            self.define_from_variant("ACTSVG_BUILD_WEB", "web"),
            self.define("ACTSVG_BUILD_TESTING", self.run_tests),
        ]
        return args
