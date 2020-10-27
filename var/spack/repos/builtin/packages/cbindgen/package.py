# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cbindgen(CargoPackage):
    """A tool for generating C bindings to Rust code."""

    homepage  = "https://crates.io/crates/cbindgen"
    crates_io = "cbindgen"
    git       = "https://github.com/eqrion/cbindgen.git"

    maintainers = ['AndrewGaspar']

    version('master', branch='master')
    version('0.14.4', sha256='e783d38a7700989e0209d0b0ed224c34ade92d3603da0cf15dc502ebada685a6')
