# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os

from spack.package import *


class Qucs(AutotoolsPackage):
    """QUCS - Quite Universal Circuit Simulator

    Qucs is an integrated circuit simulator which means you are able to
    setup a circuit with a graphical user interface (GUI) and simulate
    the large-signal, small-signal and noise behaviour of the circuit.
    After that simulation has finished you can view the simulation results
    on a presentation page or window.
    """

    homepage = "https://qucs.sourceforge.net/"
    url = "https://sourceforge.net/projects/qucs/files/qucs/0.0.19/qucs-0.0.19.tar.gz"
    git = "https://git.code.sf.net/p/qucs/git"

    version("master", branch="master")
    version("0.0.19", sha256="45c6434fde24c533e63550675ac21cdbd3cc6cbba29b82a1dc3f36e7dd4b3b3e")
    version("0.0.18", sha256="3609a18b57485dc9f19886ac6694667f3251702175bd1cbbbea37981b2c482a7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    # Can use external simulators:
    variant(
        "simulators",
        default="qucs",
        multi=True,
        values=("qucs", "ngspice", "xyce"),
        description="Circuits simulators (builtin qucsator and external ngspice, xyce)",
    )

    depends_on("flex@2.5.9:", type="build")
    depends_on("bison@2.5:", type="build")
    depends_on("pkgconfig", type="build")

    depends_on("autoconf@2.64:", type="build")
    depends_on("automake@1.7.0:", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")

    depends_on("adms", when="@0.0.19:")
    depends_on("qt@4.8.5:4.8.7")
    depends_on("gperf@3.0.1:")

    # Simulators can be qucsator, the Circuit simulator of the Qucs project
    # from https://github.com/Qucs/qucsator, or they can also be provided by
    # ngspice and xyce.
    # See https://qucs-help.readthedocs.io/en/spice4qucs/BasSim.html
    depends_on("ngspice build=bin", type="run", when="simulators=ngspice")
    depends_on("xyce", type="run", when="simulators=xyce")

    def autoreconf(self, spec, prefix):
        sh = which("sh")
        if os.path.exists("bootstrap"):
            sh("./bootstrap")
        else:
            sh("./autogen.sh")

    def configure_args(self):
        args = ["--disable-doc"]
        return args
