# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class RocmRoctThunkInterface(CMakePackage):
    """This repository includes the user-mode API interfaces used to
    interact with the ROCk driver. Currently supported agents include
    only the AMD/ATI Fiji family of discrete GPUs."""

    homepage = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface"
    url = "https://github.com/RadeonOpenCompute/ROCT-Thunk-Interface/archive/rocm-3.5.0.tar.gz"

    version('3.5.0', 'd9f458c16cb62c3c611328fd2f2ba3615da81e45f3b526e45ff43ab4a67ee4aa')

    @run_after("install")
    def post_install(self):
        with working_dir(self.build_directory):
            make('build-dev')
            make('install-dev')
