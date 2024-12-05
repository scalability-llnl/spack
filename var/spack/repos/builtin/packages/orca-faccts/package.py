# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class OrcaFaccts(Package):
    """An ab initio, DFT and semiempirical SCF-MO package

    Note: Orca is licensed software. You will need to create an account
    on the Orca homepage and download Orca yourself. Spack will search
    your current directory for the download file. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://faccts.de"
    url = "file://{0}/orca-5.0.4-f.1_linux_x86-64_openmpi41.tar.xz".format(os.getcwd())
    manual_download = True

    version(
        "5.0.4.1",
        sha256="256b446fca33ce637a87ee6f22951ae1bc167fbc6ee5cef033bbe0979279dbad",
        url="file://{0}/orca-5.0.4-f.1_linux_x86-64_openmpi41.tar.xz".format(os.getcwd()),
    )
    version(
        "5.0.3.4",
        sha256="c53feb9d0f2ae998a79d7cfe91726598e38304bd86e80c772dfda011125d5b99",
        url="file://{0}/orca-5.0.3-f.4_linux_x86-64_openmpi41.tar.xz".format(os.getcwd()),
    )
    version(
        "5.0.3.1",
        sha256="dea377459d61ef7d7e822e366420197ee2a4864991dfcdc4ea1a683f9be26c7f",
        url="file://{0}/orca-5.0.3-f.1_linux_x86-64_openmpi41.tar.xz".format(os.getcwd()),
    )

    depends_on("libevent", type="run")
    depends_on("libpciaccess", type="run")

    # Map Orca version with the required OpenMPI version
    openmpi_versions = {"5.0.3.1:5.0.4.1": "4.1.0:4.1.5"}
    for orca_version, openmpi_version in openmpi_versions.items():
        depends_on(
            "openmpi@{0}".format(openmpi_version), type="run", when="@{0}".format(orca_version)
        )

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        install_tree("bin", prefix.bin)
        install_tree("lib", prefix.lib)

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.spec["libevent"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["libpciaccess"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["openmpi"].prefix.lib)
