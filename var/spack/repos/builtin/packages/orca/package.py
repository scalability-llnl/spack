# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Orca(Package):
    """An ab initio, DFT and semiempirical SCF-MO package

    Note: Orca is licensed software. You will need to create an account
    on the Orca homepage and download Orca yourself. Spack will search
    your current directory for the download file. Alternatively, add this
    file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see https://spack.readthedocs.io/en/latest/mirrors.html"""

    homepage = "https://cec.mpg.de"
    maintainers("snehring")
    manual_download = True

    license("LGPL-2.1-or-later")

    version(
        "avx2-6.0.0", sha256="02c21294efe7b1b721e26cb90f98ee15ad682d02807201b7d217dfe67905a2fd"
    )
    version("6.0.0", sha256="219bd1deb6d64a63cb72471926cb81665cbbcdec19f9c9549761be67d49a29c6")
    version("5.0.4", sha256="c4ea5aea60da7bcb18a6b7042609206fbeb2a765c6fa958c5689d450b588b036")
    version("5.0.3", sha256="b8b9076d1711150a6d6cb3eb30b18e2782fa847c5a86d8404b9339faef105043")
    version("4.2.1", sha256="a84b6d2706f0ddb2f3750951864502a5c49d081836b00164448b1d81c577f51a")
    version("4.2.0", sha256="01096466e41a5232e5a18af7400e48c02a6e489f0d5d668a90cdd2746e8e22e2")

    depends_on("libevent", type="run")
    depends_on("libpciaccess", type="run")

    # Map Orca version with the required OpenMPI version
    # OpenMPI@4.1.1 has issues in pmix environments, hence 4.1.2 here
    openmpi_versions = {
        "4.2.0": "3.1.4",
        "4.2.1": "3.1.4",
        "5.0.3": "4.1.2",
        "5.0.4": "4.1.2",
        "6.0.0": "4.1.6",
        "avx2-6.0.0": "4.1.6",
    }
    for orca_version, openmpi_version in openmpi_versions.items():
        depends_on(
            "openmpi@{0}".format(openmpi_version), type="run", when="@{0}".format(orca_version)
        )

    def url_for_version(self, version):
        openmpi_version = self.openmpi_versions[version.string].replace(".", "")
        if openmpi_version == "412":
            openmpi_version = "411"
        ver_parts = version.string.split("-")
        ver_underscored = ver_parts[-1].replace(".", "_")
        features = ver_parts[:-1] + ["shared"]
        feature_text = "_".join(features)
        return f"file://{os.getcwd()}/orca_{ver_underscored}_linux_x86-64_{feature_text}_openmpi{openmpi_version}.tar.xz"

    def install(self, spec, prefix):
        mkdirp(prefix.bin)

        install_tree(".", prefix.bin)

        # Check "mpirun" usability when building against OpenMPI
        # with Slurm scheduler and add a "mpirun" wrapper that
        # calls "srun" if need be
        if "^openmpi ~legacylaunchers schedulers=slurm" in self.spec:
            mpirun_srun = join_path(os.path.dirname(__file__), "mpirun_srun.sh")
            install(mpirun_srun, prefix.bin.mpirun)

    def setup_run_environment(self, env):
        env.prepend_path("LD_LIBRARY_PATH", self.prefix.bin)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["libevent"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["libpciaccess"].prefix.lib)
        env.prepend_path("LD_LIBRARY_PATH", self.spec["openmpi"].prefix.lib)
