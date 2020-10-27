# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class CargoMpirun(CargoPackage):
    """`cargo mpirun` allows you to easily build and run your MPI applications
    in a single command. It emulates `cargo run`, allowing you to specify a
    target to be built and run, and cargo takes care of the rest."""

    homepage  = "https://crates.io/crates/cargo-mpirun"
    crates_io = "cargo-mpirun"
    git       = "https://github.com/AndrewGaspar/cargo-mpirun.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.1.8', sha256='18ef8a141344a81cc80e1f889257c78d620a9c958a1c0b0581299c3e194c0eef')

    depends_on('mpi', type='run')
