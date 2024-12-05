# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Viennarna(AutotoolsPackage):
    """The ViennaRNA Package consists of a C code library and several
    stand-alone programs for the prediction and comparison of RNA secondary
    structures.
    """

    homepage = "https://www.tbi.univie.ac.at/RNA/"
    url = "https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_4_x/ViennaRNA-2.4.3.tar.gz"
    maintainers("snehring")

    version("2.6.4", sha256="d1259ce5809601a12b0dc9b724ea2c55806fece80d8d83ad417ea8a2dd574982")
    version("2.5.0", sha256="b85544650ee316743173ec9b30497cc4c559f1bfb8f66d16c563f780afd8c0c5")
    version("2.4.3", sha256="4cda6e22029b34bb9f5375181562f69e4a780a89ead50fe952891835e9933ac0")
    version("2.3.5", sha256="26b62a00da21bc5597b580ab8fef4e624234ec446d7d3cb0ce22803a5d7074ca")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant(
        "sse", default=True, description="Enable SSE in order to substantially speed up execution"
    )
    variant("perl", default=True, description="Build ViennaRNA with Perl interface")
    variant("python", default=True, description="Build ViennaRNA with Python interface")

    depends_on("perl", type=("build", "run"))
    depends_on("python", type=("build", "run"))
    depends_on("libsvm")
    depends_on("gsl")

    def url_for_version(self, version):
        url = "https://www.tbi.univie.ac.at/RNA/download/sourcecode/{0}_x/ViennaRNA-{1}.tar.gz"
        return url.format(version.up_to(2).underscored, version)

    def configure_args(self):
        args = self.enable_or_disable("sse")
        args += self.with_or_without("python")
        args += self.with_or_without("perl")
        if self.spec.satisfies("@2.4.3"):
            args.append("--without-swig")

        if "python@3:" in self.spec:
            args.append("--with-python3")

        return args
