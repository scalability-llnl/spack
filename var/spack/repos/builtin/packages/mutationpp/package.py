# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Mutationpp(CMakePackage):
    """Mutation++ is an open-source library originally developed
    at the von Karman Institute for Fluid Dynamics, designed to
    couple with conventional computational fluid dynamics codes
    to provide thermodynamic, transport, chemistry, and energy
    transfer properties associated with subsonic to hypersonic flows."""

    homepage = "https://github.com/mutationpp/Mutationpp"
    url = "https://github.com/mutationpp/Mutationpp/archive/v0.3.1.tar.gz"

    license("LGPL-3.0-only")

    version("1.0.5", sha256="319eca4e82a2469946344195373eabf28caaf6a39ddf3142b2337f47aa0835a8")
    version("1.0.0", sha256="928df99accd1a02706a57246edeef8ebbf3bd91bb40492258ee18b810a7e0194")
    version("0.3.1", sha256="a6da2816e145ac9fcfbd8920595b7f65ce7bc8df0bec572b32647720758cbe69")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated
    depends_on("fortran", type="build")  # generated

    variant("fortran", default=True, description="Enable Fortran interface")
    variant("data", default=True, description="Install default model data")
    variant("examples", default=True, description="Install examples")

    def cmake_args(self):
        args = []
        if "+fortran" in self.spec:
            args.append("-DBUILD_FORTRAN_WRAPPER=ON")
        return args

    @run_after("install")
    def install_data(self):
        if "+data" in self.spec and os.path.isdir("data"):
            install_tree("data", self.prefix.data)

    @run_after("install")
    def install_examples(self):
        if "+examples" in self.spec and os.path.isdir("examples"):
            install_tree("examples", self.prefix.examples)

    def setup_run_environment(self, env):
        env.set("MPP_DIRECTORY", self.prefix)
        if os.path.isdir(self.prefix.data):
            env.set("MPP_DATA_DIRECTORY", self.prefix.data)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set("MPP_DIRECTORY", self.prefix)
        if os.path.isdir(self.prefix.data):
            env.set("MPP_DATA_DIRECTORY", self.prefix.data)
