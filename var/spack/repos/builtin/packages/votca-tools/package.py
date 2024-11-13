# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class VotcaTools(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
    Applications (VOTCA) is a package intended to reduce the amount of
    routine work when doing systematic coarse-graining of various
    systems. The core is written in C++.

    This package contains the basic tools library of VOTCA.
    """

    homepage = "https://www.votca.org"
    url = "https://github.com/votca/tools/tarball/v1.4"
    git = "https://github.com/votca/tools.git"
    maintainers("junghans")

    version("stable", branch="stable", deprecated=True)
    version(
        "2021.2",
        sha256="2cd3175b65924803aff90dce49f60e1dda9015988a453d60358e51f0dbb4292d",
        deprecated=True,
    )
    version(
        "2021.1",
        sha256="c2fdf5ab72fc75580fb3623182fa88dd0eed856388bdc862aff42148bb0a16e7",
        deprecated=True,
    )
    version(
        "2021",
        sha256="b84f68ba4a8bfae7b06b61e1e078dcbfb3b340c516da3be39ef545152da00ccd",
        deprecated=True,
    )
    version(
        "1.6.4",
        sha256="aa79ef4617a80ba3ca063932d5ee0d5767c0285b4b613abd373ad3c986ab9f4c",
        deprecated=True,
    )
    version(
        "1.6.3",
        sha256="b4ba63861f4342070d81309992f76c4cc798dffeab894bff64799881e75b3cc2",
        deprecated=True,
    )
    version(
        "1.6.2",
        sha256="1b31e0dd7550b80b963e6714d671f3516d68ebc1e75068a5d827a6e8b4f1759a",
        deprecated=True,
    )
    version(
        "1.6.1",
        sha256="3e8f51d484cb3fdfbeb851aab387807ba4c40aecef8317c90182da68ad282dcc",
        deprecated=True,
    )
    version(
        "1.6",
        sha256="cfd0fedc80fecd009f743b5df47777508d76bf3ef294a508a9f11fbb42efe9a5",
        deprecated=True,
    )
    version(
        "1.5.1",
        sha256="4be4fe25a2910e24e1720cd9022d214001d38196033ade8f9d6e618b4f47d5c4",
        deprecated=True,
    )
    version(
        "1.5",
        sha256="a82a6596c24ff06e79eab17ca02f4405745ceeeb66369693a59023ad0b62cf22",
        deprecated=True,
    )
    version(
        "1.4.1",
        sha256="b6b87f6bec8db641a1d8660422ca44919252a69494b32ba6c8c9ac986bae9a65",
        deprecated=True,
    )
    version(
        "1.4",
        sha256="41638122e7e59852af61d391b4ab8c308fd2e16652f768077e13a99d206ec5d3",
        deprecated=True,
    )

    depends_on("cxx", type="build")  # generated

    # https://github.com/votca/tools/pull/229, fix mkl in exported target
    patch(
        "https://github.com/votca/tools/pull/229.patch?full_index=1",
        sha256="2a9ef179904d5057f36a5ce533c002d8f5880dc4b3eba569825f4a7e7f055eb1",
        when="@=1.6+mkl",
    )
    # https://github.com/votca/tools/pull/361, fix build with newer glibc/gcc, fixed in stable and 2021.1
    patch(
        "https://github.com/votca/tools/commit/6bb7e35ba7d1a31247eafb323be2777ec0439cfe.patch?full_index=1",
        sha256="5a67eaf362755412b9825558bedb53fac3204713effd60c59f14c54eb1ad52b9",
        when="@2021:2021.0",
    )

    variant("mkl", default=False, description="Build with MKL support")
    conflicts("+mkl", when="@1.4:1.5")

    depends_on("cmake@2.8:", type="build")
    depends_on("expat")
    depends_on("fftw-api@3")
    depends_on("gsl", when="@1.4:1.4.9999")
    depends_on("eigen@3.3:", when="@stable,1.5:")
    depends_on("boost+exception+filesystem+system+container+math+program_options")
    depends_on("sqlite", when="@1.4:1.5")
    depends_on("mkl", when="+mkl")

    def cmake_args(self):
        args = ["-DWITH_RC_FILES=OFF"]

        if "~mkl" in self.spec:
            args.append("-DCMAKE_DISABLE_FIND_PACKAGE_MKL=ON")

        return args
