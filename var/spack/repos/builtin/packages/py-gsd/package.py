# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGsd(PythonPackage):
    """The GSD file format is the native file format for HOOMD-blue. GSD files
    store trajectories of the HOOMD-blue system state in a binary file with
    efficient random access to frames. GSD allows all particle and topology
    properties to vary from one frame to the next. Use the GSD Python API to
    specify the initial condition for a HOOMD-blue simulation or analyze
    trajectory output with a script. Read a GSD trajectory with a visualization
    tool to explore the behavior of the simulation."""

    homepage = "https://gsd.readthedocs.io/en/stable/"
    pypi = "gsd/gsd-1.9.3.tar.gz"

    maintainers("RMeli")

    license("BSD-2-Clause")

    version("3.2.1", sha256="cf05148e23f169a00c073eb7d8151e8b521e0f962ce460b55d812cae5be326aa")
    version("3.2.0", sha256="cf3c8419ec66085b2b9853577058861d9e738bfe397b0170ead821b866ab49b9")
    version("3.1.1", sha256="6802b79d7f078536faf5a96ac300518613dd285cf3bc21ed81e1f2d0f7155bf5")
    version("3.1.0", sha256="35a70419c6a519825afd9d5e47a570d98cec7273c39f43e2ab0aa3e7166ad198")
    version("3.0.1", sha256="7b3ce7428d9f9f708618b3a2ef19ab122cc36b658ea53b70d0de40189d19647c")
    version("2.8.0", sha256="f2b031a26a7a5bee5f3940dc2f36c5a5b6670307b297c526adf2e26c1f5b46ae")
    version("1.9.3", sha256="c6b37344e69020f69fda2b8d97f894cb41fd720840abeda682edd680d1cff838")

    depends_on("c", type="build")  # generated

    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools@42:", type="build", when="@2.8.0:")
    depends_on("py-setuptools@64:", type="build", when="@3.0.1:")
    depends_on("py-cython", type="build")
    depends_on("py-numpy@1.9.3:", type=("build", "run"))
    depends_on("py-numpy@1.9.3:1", when="@:1", type=("build", "run"))
