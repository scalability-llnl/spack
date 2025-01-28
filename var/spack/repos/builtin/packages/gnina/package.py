# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gnina(CMakePackage, CudaPackage):
    """gnina (pronounced NEE-na) is a molecular docking program with integrated support
    for scoring and optimizing ligands using convolutional neural networks."""

    homepage = "https://github.com/gnina/gnina"
    url = "https://github.com/gnina/gnina/archive/refs/tags/v1.0.3.tar.gz"
    git = "https://github.com/gnina/gnina.git"

    maintainers("RMeli")

    license("Apache-2.0")

    version("master", branch="master")
    version("1.3", sha256="79630705190576669c9613cc3e1e63f1122cba4e363e73c3a0bd7e21f76f443f")
    version("1.1", sha256="114570b0f84a545ce0fea5b2da87bc116c134cef64bf90e6e58e8f84e175a0fa")
    version("1.0.3", sha256="4274429f38293d79c7d22ab08aca91109e327e9ce3f682cd329a8f9c6ef429da")

    variant("cudnn", default=True, description="Build with cuDNN")
    variant("gninavis", default=False, description="Build gninavis")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    _boost_extensions = " " + "".join(
        [
            "+atomic",
            "+chrono",
            "+date_time",
            "+exception",
            "+filesystem",
            "+graph",
            "+iostreams",
            "+locale",
            "+log",
            "+math",
            "+python",
            "+program_options",
            "+random",
            "+regex",
            "+serialization",
            "+signals",
            "+system",
            "+test",
            "+thread",
            "+timer",
            "+wave",
        ]
    )

    depends_on("zlib-api")
    depends_on("boost@:1.79" + _boost_extensions)
    depends_on("protobuf@:3.21.12")

    depends_on("libmolgrid")

    depends_on("openbabel@3:~gui~cairo~maeparser~coordgen")
    depends_on("rdkit", when="+gninavis")

    depends_on("python", type="build")
    depends_on("py-numpy", type="build")
    depends_on("py-pytest", type="build")

    depends_on("cuda@11", when="@:1.1")
    depends_on("cuda@12", when="@1.3:")
    depends_on("cudnn", when="+cudnn")

    depends_on("cmake@3.27:", when="@1.3:")  # CMake policy CMP0146 introduced in 3.27
    depends_on("jsoncpp", when="@1.3:")
    depends_on("py-torch", when="@1.3:")

    depends_on("glog@:0.6", when="@:1.1")
    depends_on("hdf5+cxx+hl~mpi", when="@:1.1")
    depends_on("openblas~fortran", when="@:1.1")

    patch(
        "https://patch-diff.githubusercontent.com/raw/gnina/gnina/pull/280.patch?full_index=1",
        when="@1.3",
        sha256="88d1760423cedfdb992409b0bfe3f9939ab5900f52074364db9ad8b87f4845d4",
    )
    patch(
        "https://patch-diff.githubusercontent.com/raw/gnina/gnina/pull/282.patch?full_index=1",
        when="@1.3",
        sha256="6a1db3d63039a11ecc6e753b325962773e0084673d54a0d93a503bca8b08fb9e",
    )

    def cmake_args(self):
        args = []

        if self.spec.satisfies("@:1.1"):
            args.append("-DBLAS=Open")  # Use OpenBLAS instead of Atlas' BLAS

        if self.spec.satisfies("+gninavis"):
            args.append(f"-DRDKIT_INCLUDE_DIR={self.spec['rdkit'].prefix.include.rdkit}")

        if self.spec.satisfies("@1.3:"):
            args.append(self.define("GNINA_FORCE_EXTERNAL_LIBS", True))

        return args
