# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.boost import Boost


class Caffe(CMakePackage, CudaPackage):
    """Caffe is a deep learning framework made with expression, speed, and
    modularity in mind. It is developed by the Berkeley Vision and Learning
    Center (BVLC) and by community contributors."""

    homepage = "https://caffe.berkeleyvision.org"
    url = "https://github.com/BVLC/caffe/archive/1.0.tar.gz"

    license("BSD-2-Clause")

    version("1.0", sha256="71d3c9eb8a183150f965a465824d01fe82826c22505f7aa314f700ace03fa77f")
    version("rc5", sha256="06592aa8f5254335df3e244dafacc15765e2c60479b4bf2e7c887e8e023802fb")
    version("rc4", sha256="018792411d75ee34b6107216550cca2a1d668d45cb366033ba3c647e6a3018df")
    version("rc3", sha256="0884207bfba0fbc8b263b87d30f9304f7094eec3a48f975177d142f8c72b6e3b")
    version("rc2", sha256="55c9c20870b30ce398e19e4f1a62ade1eff08fce51e28fa5604035b711978eec")

    depends_on("cxx", type="build")  # generated

    variant("cuda", default=False, description="Builds with support for GPUs via CUDA and cuDNN")
    variant("opencv", default=True, description="Build with OpenCV support")
    variant("leveldb", default=True, description="Build with levelDB")
    variant("lmdb", default=True, description="Build with lmdb")
    variant("python", default=False, description="Build python wrapper and caffe python layer")
    variant("matlab", default=False, description="Build Matlab wrapper")

    depends_on("boost +python", when="+python")

    # TODO: replace this with an explicit list of components of Boost,
    # for instance depends_on('boost +filesystem')
    # See https://github.com/spack/spack/pull/22303 for reference
    depends_on(Boost.with_default_variants, when="+python")
    depends_on("cuda", when="+cuda")
    depends_on("blas")
    depends_on("protobuf@:3.17")
    depends_on("glog")
    depends_on("gflags")
    depends_on("hdf5 +hl +cxx")

    # Optional dependencies
    depends_on("opencv@:3+highgui+imgproc+imgcodecs", when="+opencv")
    depends_on("leveldb", when="+leveldb")
    depends_on("lmdb", when="+lmdb")
    depends_on("python@2.7:", when="+python")
    depends_on("py-numpy@1.7:", when="+python", type=("build", "run"))
    depends_on("matlab", when="+matlab")

    extends("python", when="+python")

    def cmake_args(self):
        spec = self.spec
        args = [
            "-DBLAS={0}".format("open" if spec["blas"].name == "openblas" else spec["blas"].name),
            "-DCPU_ONLY=%s" % ("~cuda" in spec),
            "-DUSE_CUDNN=%s" % ("+cuda" in spec),
            "-DBUILD_python=%s" % ("+python" in spec),
            "-DBUILD_python_layer=%s" % ("+python" in spec),
            "-DBUILD_matlab=%s" % ("+matlab" in spec),
            "-DUSE_OPENCV=%s" % ("+opencv" in spec),
            "-DUSE_LEVELDB=%s" % ("+leveldb" in spec),
            "-DUSE_LMDB=%s" % ("+lmdb" in spec),
            "-DGFLAGS_ROOT_DIR=%s" % spec["gflags"].prefix,
            "-DGLOG_ROOT_DIR=%s" % spec["glog"].prefix,
        ]

        if spec.satisfies("^openblas"):
            env["OpenBLAS_HOME"] = spec["openblas"].prefix

        if spec.satisfies("+lmdb"):
            env["LMDB_DIR"] = spec["lmdb"].prefix

        if spec.satisfies("+leveldb"):
            env["LEVELDB_ROOT"] = spec["leveldb"].prefix

        if spec.satisfies("+python"):
            version = spec["python"].version.up_to(1)
            args.append("-Dpython_version=%s" % version)

        if spec["hdf5"].satisfies("+mpi"):
            args.extend(
                [
                    "-DCMAKE_C_COMPILER={0}".format(self.spec["mpi"].mpicc),
                    "-DCMAKE_CXX_COMPILER={0}".format(self.spec["mpi"].mpicxx),
                ]
            )

        if spec.satisfies("+cuda"):
            if spec.variants["cuda_arch"].value[0] != "none":
                cuda_arch = spec.variants["cuda_arch"].value
                args.append(self.define("CUDA_ARCH_NAME", "Manual"))
                args.append(self.define("CUDA_ARCH_BIN", " ".join(cuda_arch)))

        return args
