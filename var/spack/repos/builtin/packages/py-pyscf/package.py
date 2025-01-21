# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPyscf(PythonPackage):
    """PySCF is a collection of electronic structure programs powered
    by Python."""

    homepage = "https://pyscf.org"
    pypi = "pyscf/pyscf-2.5.0.tar.gz"

    maintainers("naromero77")

    license("Apache-2.0")

    version("2.8.0", sha256="db720372e7f7d1aa2df0fb90c07f483da363730197c937a6378952d34b6abf3d")
    version("2.7.0", sha256="ca8efc2f28d72c3130f26a967e7fa8d0bbc4a6b47d16a7c4c732ec85a31b7eec")
    version("2.6.2", sha256="744c89a8e4d38c4b5562f75fa68f9d079faeb23602d255fba0eb6d1bac97bca2")
    version("2.6.1", sha256="faeaeeb0c07fec5018937655511709a9c2445e3d7c421c0fa1ae5d889e4ab455")
    version("2.6.0", sha256="08ff920fedd4b257273d235fb4492535147c1e3154de5ab02b5446de93e200d8")
    version("2.5.0", sha256="9596603c914fb3fba853607e96366fa541012faffd59a4ea052f0122dcea5343")
    version("2.4.0", sha256="af0597c481851b5448e7055c3160aef28dc12a1e0b35dda8279555c0780c0d45")
    version("2.3.0", sha256="71781de62c25924fd4e93ffeb0451ec0d0b3646fe426c75023f4f519f0f35d85")
    version("2.2.1", sha256="4ff6851351caadc5dfa543b6b2c5fbd926ded87e3cc39faa0054e1e5090ed69a")
    version("2.2.0", sha256="8f65042cf7e86aa5088756988eb90418befcd18f07a6b8c597229a5f2ba4f644")
    version("2.1.1", sha256="608442171f5db106b02a95c878c65798fbbd87dc0ce50551a2e081e7d206adb0")
    version("2.1.0", sha256="45feecc9c9a0ce18dee73c5b178fb0faa3f0c0d3dd5f98b48dc2370c9e13d05b")
    version("2.0.1", sha256="b2f00330f98edf7c5b8272904fc11ca74f4677219ba6468aaa7154580efd9edd")
    version("1.7.5", sha256="52856b39f0ada2f6340757caa65dc5c1d9a3cdfceea2a6615ad8af92664a6c69")
    version("1.7.3", sha256="62a26146a222140395b276ea33182f87809a21989ddcf78e2dcb8e35ebc57af2")

    depends_on("c", type="build")  # generated

    # dependencies
    depends_on("cmake@3.10:", type="build", when="@2.1:")
    depends_on("cmake@2.8:", type="build")
    depends_on("python@3.6:", type=("build", "run"), when="@2.1:")
    depends_on("python@2.6:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.8.0:", type=("build", "run"))
    depends_on("py-numpy@1.13.0:", type=("build", "run"), when="@2:")
    depends_on("py-numpy@1", type=("build", "run"), when="@:2.6.0")
    conflicts("^py-numpy@1.16:1.17", when="@2:")
    depends_on("py-scipy@0.12:1.10", type=("build", "run"), when="@:2.0")
    depends_on("py-scipy@0.19:1.10", type=("build", "run"), when="@2.1:2.2")
    # https://github.com/pyscf/pyscf/issues/1783
    depends_on("py-scipy@0.19:", type=("build", "run"), when="@2.3:")
    depends_on("py-scipy@1.6.0:", type=("build", "run"), when="@2.7.0:")
    conflicts("^py-scipy@1.5.0:1.5.1", when="@2:")
    depends_on("py-h5py@2.3.0:", type=("build", "run"))
    depends_on("py-h5py@2.7.0:", type=("build", "run"), when="@2:")
    depends_on("blas")
    depends_on("libcint+coulomb_erf+f12")
    depends_on("libxc")
    depends_on("xcfun")

    def setup_build_environment(self, env):
        # Tell PSCF where supporting libraries are located."
        spec = self.spec

        pyscf_search_dir = []
        pyscf_search_dir.append(spec["blas"].prefix)
        pyscf_search_dir.append(spec["libcint"].prefix)
        pyscf_search_dir.append(spec["libcint"].prefix.lib64)
        pyscf_search_dir.append(spec["libxc"].prefix)
        pyscf_search_dir.append(spec["xcfun"].prefix)
        pyscf_search_dir.append(spec["xcfun"].prefix.include.XCFun)

        env.set("PYSCF_INC_DIR", ":".join(pyscf_search_dir))
