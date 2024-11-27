# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
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

    version("1.1", sha256="114570b0f84a545ce0fea5b2da87bc116c134cef64bf90e6e58e8f84e175a0fa")
    version("1.0.3", sha256="4274429f38293d79c7d22ab08aca91109e327e9ce3f682cd329a8f9c6ef429da")

    depends_on("cxx", type="build")  # generated

    variant("cudnn", default=True, description="Build with cuDNN")
    variant("gninavis", default=False, description="Build gninavis")

    _boost = "boost" + "".join(
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
    depends_on(_boost)
    depends_on("glog")
    depends_on("protobuf@:3.21.12")
    depends_on("hdf5+cxx+hl~mpi")
    depends_on("openblas~fortran")

    depends_on("libmolgrid")

    depends_on("openbabel@3:~gui~cairo~maeparser~coordgen")
    depends_on("rdkit", when="+gninavis")

    depends_on("python", type="build")
    depends_on("py-numpy", type="build")
    depends_on("py-pytest", type="build")

    depends_on("cuda@11")
    depends_on("cudnn", when="+cudnn")

    def cmake_args(self):
        args = ["-DBLAS=Open"]  # Use OpenBLAS instead of Atlas' BLAS

        if self.spec.satisfies("+gninavis"):
            args.append(f"-DRDKIT_INCLUDE_DIR={self.spec['rdkit'].prefix.include.rdkit}")

        return args
