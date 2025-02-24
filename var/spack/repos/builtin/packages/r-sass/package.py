# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSass(RPackage):
    """Syntactically Awesome Style Sheets ('Sass').

    An 'SCSS' compiler, powered by the 'LibSass' library. With this, R
    developers can use variables, inheritance, and functions to generate
    dynamic style sheets. The package uses the 'Sass CSS' extension language,
    which is stable, powerful, and CSS compatible."""

    cran = "sass"

    license("MIT")

    version("0.4.9", sha256="e133049aad7964e0f6150257e1470b3748f36029322265ee797b8caf7517d4d2")
    version("0.4.5", sha256="eba161d982d2db108c8c0b61ec6b41a20d3adec430c7cc39537ab388c1007a90")
    version("0.4.2", sha256="b409049d0de9fae853f46c19d353226c8e9244ce847bdada033d8669fc2c9646")
    version("0.4.1", sha256="850fcb6bd49085d5afd25ac18da0744234385baf1f13d8c0a320f4da2de608bb")
    version("0.4.0", sha256="7d06ca15239142a49e88bb3be494515abdd8c75f00f3f1b0ee7bccb55019bc2b")

    depends_on("r-fs", type=("build", "run"))
    depends_on("r-fs@1.2.4:", type=("build", "run"), when="@0.4.7:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"))
    depends_on("r-htmltools@0.5.1:", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-rappdirs", type=("build", "run"))
    depends_on("gmake", type="build")
