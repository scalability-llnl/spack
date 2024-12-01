# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyScs(PythonPackage, CudaPackage):
    """SCS: splitting conic solver"""

    homepage = "https://github.com/cvxgrp/scs"
    pypi = "scs/scs-2.1.1-2.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version("3.2.2", sha256="7206a2ad27ca031d693d65cbcbcfc661498f3983838079a66579bcc784b25293")
    version("2.1.1-2", sha256="f816cfe3d4b4cff3ac2b8b96588c5960ddd2a3dc946bda6b09db04e7bc6577f2")

    depends_on("c", type="build")  # generated

    variant(
        "float32",
        default=False,
        description="Use 32 bit (single precision) floats, default is 64 bit",
    )
    variant("extra_verbose", default=False, description="Extra verbose SCS (for debugging)")
    variant("int32", default=False, description="Use 32 bit ints")
    variant("blas64", default=False, description="Use 64 bit ints for the blas/lapack libs")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.7:", type=("build", "run"))
    depends_on("py-scipy@0.13.2:", type=("build", "run"))

    # in newer pip versions --install-option does not exist
    # technically only the variants need this restriction
    depends_on("py-pip@:23.0", type="build")

    def install_options(self, spec, prefix):
        args = []
        if (
            "+cuda" in spec
            or "+float32" in spec
            or "+int32" in spec
            or "+extra_verbose" in spec
            or "+blas64" in spec
        ):
            args = ["--scs"]
        if "+cuda" in spec:
            args.append("--gpu")
        if "+float32" in spec:
            args.append("--float")
        if "+extra_verbose" in spec:
            args.append("--extraverbose")
        if "+int32" in spec:
            args.append("--int")
        if "+blas64" in spec:
            args.append("--blas64")
        return args
