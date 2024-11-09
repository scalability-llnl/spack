# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class PyLibensemble(PythonPackage):
    """Library for managing ensemble-like collections of computations."""

    homepage = "https://libensemble.readthedocs.io"
    pypi = "libensemble/libensemble-1.4.2.tar.gz"
    git = "https://github.com/Libensemble/libensemble.git"
    maintainers("shuds13", "jlnav")

    tags = ["e4s"]

    license("BSD-3-Clause")

    version("develop", branch="develop")
    version("1.4.2", sha256="d283935594333793112f65cec1070137e0a87e31cd2bf1baec4a1261ac06ab63")
    version("1.4.1", sha256="fd39d5c4010f9cb1728af1666d0f10d0da7dd43c12e411badcbc53aab42ab183")
    version("1.4.0", sha256="0d9f76175dcd5ca7a5e0076a8e64ea59b504055779100d259114468630e82fa2")
    version("1.3.0", sha256="4a2f47de9ab57c577f3de5dd849ec1b621effde7206a54b2aa29aaf309c87532")
    version("1.2.2", sha256="936e34ed4e8129a9980187b21d586472b6362403889a739595d6b631335a8678")
    version("1.2.1", sha256="b80e77548a1e2a71483352b3b00e22b47191e45ca5741324c2b0f20b05579a3d")
    version("1.2.0", sha256="e1076e8eea7844d3799f92d136586eca4da34ec753bf41a8d1be04d7a45ec4c1")
    version("1.1.0", sha256="3e3ddc4233272d3651e9d62c7bf420018930a4b9b135ef9ede01d5356235c1c6")
    version("1.0.0", sha256="b164e044f16f15b68fd565684ad8ce876c93aaeb84e5078f4ea2a29684b110ca")
    version("0.10.2", sha256="ef8dfe5d233dcae2636a3d6aa38f3c2ad0f42c65bd38f664e99b3e63b9f86622")
    version("0.10.1", sha256="56ae42ec9a28d3df8f46bdf7d016db9526200e9df2a28d849902e3c44fe5c1ba")
    version("0.10.0", sha256="f800f38d02def526f1d2a325710d01fdd3637cd1e33a9a083a3cf4a7f419a726")
    version("0.9.3", sha256="00e5a65d6891feee6a686c048d8de72097b8bff164431f163be96ec130a9c390")
    version("0.9.2", sha256="e46598e5696f770cbff4cb90507b52867faad5654f1b80de35405a95228c909f")
    version("0.9.1", sha256="684e52b0ea64f5ec610e7868b7e4c9fa5fd2316a370a726870aa5fd5fb1b0ede")
    version("0.9.0", sha256="34976e775f0d2ba5955744560104eab214fd22cb47173440eb5136e852a8ec38")
    version("0.8.0", sha256="1102e56c6381c9692de6888add23780ec69f18ad33f12119dc0391776a9a7300")
    version("0.7.2", sha256="69b64304d1ecce4d57687ea6062f89bd813ae93b2a290bb1f595c5626ab6f197")
    version("0.7.1", sha256="5cb294269624c1284ea25be9ed3bc668a2333e21e97a97b57ad339eb85435e46")
    version("0.7.0", sha256="4c3c16ef3d4750b7a54198fae5d7ae402c5f5411ae85189da41afd20e20027dc")
    version("0.6.0", sha256="3f6a926d3868da53835ed93fc2e2a047b368dacb648c7608ee3a66debcee4d38")
    version("0.5.2", sha256="3e36c29a4a2adc0984ecfcc998cb5bb8a2cdfbe7a1ae92f7b35b06e41d21b889")
    version("0.5.1", sha256="522e0cc086a3ed75a101b704c0fe01eae07f2684bd8d6da7bdfe9371d3187362")
    version("0.5.0", sha256="c4623171dee049bfaa38a9c433609299a56b1afb774db8b71321247bc7556b8f")
    version("0.4.1", sha256="282c32ffb79d84cc80b5cc7043c202d5f0b8ebff10f63924752f092e3938db5e")
    version("0.4.0", sha256="9384aa3a58cbc20bbd1c6fddfadb5e6a943d593a3a81c8665f030dbc6d76e76e")
    version("0.3.0", sha256="c8efdf45d0da0ef6299ee778cea1c285c95972af70d3a729ee6dc855e66f9294")
    version("0.2.0", sha256="ecac7275d4d0f4a5e497e5c9ef2cd998da82b2c020a0fb87546eeea262f495ff")
    version("0.1.0", sha256="0b27c59ae80f7af8b1bee92fcf2eb6c9a8fd3494bf2eb6b3ea17a7c03d3726bb")

    depends_on("c", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("mpi", default=True, description="Install with MPI")  # Optional communications method

    # The following variants are for optional built-in generators
    variant("scipy", default=False, description="Install with scipy")
    variant("petsc4py", default=False, description="Install with petsc4py")
    variant("nlopt", default=False, description="Install with nlopt")
    variant("mpmath", default=False, description="Install with mpmath")
    variant("deap", default=False, description="Install with DEAP")
    variant("tasmanian", default=False, description="Install with tasmanian")

    depends_on("py-numpy@1.21:", when="@1:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-psutil@5.9.4:", when="@1:", type=("build", "run"))
    depends_on("py-psutil", when="@0.7.1:", type=("build", "run"))
    depends_on("py-setuptools", when="@0.10.2:", type="build")
    depends_on("py-setuptools", when="@:0.10.1", type=("build", "run"))
    depends_on("py-pydantic@1.10:", when="@1.2.0:", type=("build", "run"))
    depends_on("py-pydantic@:1", when="@0.10:", type=("build", "run"))
    depends_on("py-tomli@1.2.1:", when="@1:", type=("build", "run"))
    depends_on("py-tomli", when="@0.10:", type=("build", "run"))
    depends_on("py-pyyaml@6.0:", when="@1:", type=("build", "run"))
    depends_on("py-pyyaml", when="@0.10:", type=("build", "run"))
    depends_on("mpi", when="@:0.4.1")
    depends_on("mpi", when="+mpi")
    depends_on("py-mpi4py@2.0:", when="@:0.4.1", type=("build", "run"))
    depends_on("py-mpi4py@2.0:", when="+mpi", type=("build", "run"))
    depends_on("py-scipy", when="+scipy", type=("build", "run"))
    depends_on("py-petsc4py", when="+petsc4py", type=("build", "run"))
    depends_on("py-petsc4py@main", when="@develop+petsc4py", type=("build", "run"))
    depends_on("nlopt", when="+nlopt", type=("build", "run"))
    depends_on("py-mpmath", when="+mpmath", type=("build", "run"))
    depends_on("py-deap", when="+deap", type=("build", "run"))
    depends_on("tasmanian+python", when="+tasmanian", type=("build", "run"))
    conflicts("~mpi", when="@:0.4.1")

    @run_after("install")
    def cache_test_sources(self):
        """Copy the example source files after the package is installed to an
        install test subdirectory for use during `spack test run`."""
        cache_extra_test_sources(
            self, join_path("examples", "calling_scripts", "regression_tests")
        )

    def run_tutorial_script(self, script):
        """run the tutorial example regression test"""

        exe = (
            self.test_suite.current_test_cache_dir.examples.calling_scripts.regression_tests.join(
                script
            )
        )
        if not os.path.isfile(exe):
            raise SkipTest(f"{script} is missing")

        python(exe, "--comms", "local", "--nworkers", "2")

    def test_uniform_sampling(self):
        """run test_uniform_sampling.py"""
        self.run_tutorial_script("test_uniform_sampling.py")

    def test_1d_sampling(self):
        """run test_1d_sampling.py"""
        self.run_tutorial_script("test_1d_sampling.py")
