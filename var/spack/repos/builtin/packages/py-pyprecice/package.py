# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyprecice(PythonPackage):
    """
    This package provides python language bindings for the
    C++ library preCICE.
    """

    homepage = "https://www.precice.org"
    git = "https://github.com/precice/python-bindings.git"
    url = "https://github.com/precice/python-bindings/archive/v2.0.0.1.tar.gz"
    maintainers = ["ajaust", "BenjaminRodenberg"]

    # Always prefer final version of release candidate
    version("develop", branch="develop")
    version('2.2.0.1', sha256='032fa58193cfa69e3be37557977056e8f507d89b40c490a351d17271269b25ad')
    version('2.1.1.2', sha256='363eb3eeccf964fd5ee87012c1032353dd1518662868f2b51f04a6d8a7154045')
    version("2.1.1.1", sha256="972f574549344b6155a8dd415b6d82512e00fa154ca25ae7e36b68d4d2ed2cf4")
    version("2.1.0.1", sha256="ac5cb7412c6b96b08a04fa86ea38e52d91ea739a3bd1c209baa93a8275e4e01a")
    version("2.0.2.1", sha256="c6fca26332316de041f559aecbf23122a85d6348baa5d3252be4ddcd5e94c09a")
    version("2.0.1.1", sha256="2791e7c7e2b04bc918f09f3dfca2d3371e6f8cbb7e57c82bd674703f4fa00be7")
    version("2.0.0.2", sha256="5f055d809d65ec2e81f4d001812a250f50418de59990b47d6bcb12b88da5f5d7")
    version("2.0.0.1", sha256="96eafdf421ec61ad6fcf0ab1d3cf210831a815272984c470b2aea57d4d0c9e0e")

    # Older versions of the bindings checked versions via pip. This patch
    # removes the pip dependency.
    # See also https://github.com/spack/spack/pull/19558
    patch("deactivate-version-check-via-pip.patch", when="@:2.1.1.1")

    depends_on("precice@develop", when="@develop")
    depends_on("precice@2.2.0", when="@2.2.0.1:2.2.0.99")
    depends_on("precice@2.1.1", when="@2.1.1.1:2.1.1.99")
    depends_on("precice@2.1.0", when="@2.1.0.1:2.1.0.99")
    depends_on("precice@2.0.2", when="@2.0.2.1:2.0.2.99")
    depends_on("precice@2.0.1", when="@2.0.1.1:2.0.1.99")
    depends_on("precice@2.0.0", when="@2.0.0.1:2.0.0.99")

    depends_on("python@3:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-mpi4py", type=("build", "run"))
    depends_on("py-cython@0.29:", type=("build"))

    phases = ['install_lib', 'build_ext', 'install']

    def build_ext_args(self, spec, prefix):
        return [
            "--include-dirs=" + spec["precice"].headers.directories[0],
            "--library-dirs=" + spec["precice"].libs.directories[0]
        ]

    def install(self, spec, prefix):
        # Older versions of the bindings had a non-standard installation routine
        # See also https://github.com/spack/spack/pull/19558#discussion_r513123239
        if self.version <= Version("2.1.1.1"):
            self.setup_py("install", "--prefix={0}".format(prefix))
