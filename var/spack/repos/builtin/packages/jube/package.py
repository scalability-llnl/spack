# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jube(PythonPackage):
    """The Juelich benchmarking environment (JUBE) provides a script based
    framework to easily create benchmark sets, run those sets on different
    computer systems and evaluate the results."""

    homepage = "https://www.fz-juelich.de/jsc/jube/"
    url = "https://apps.fz-juelich.de/jsc/jube/jube2/download.php?version=2.2.2"

    license("GPL-3.0-or-later")

    version(
        "2.7.1",
        sha256="fe8b505a8bf224d785df665af134a1e69063d34d1a7214700d8c7325fef9ecfc",
        extension="tar.gz",
    )
    version(
        "2.7.0",
        sha256="31bba50c40547db6dc777d9766babb4786bb8539e988fd5de962602593304d26",
        extension="tar.gz",
    )
    version(
        "2.6.2",
        sha256="44fd0dd74500cb2537af52850d5742e5bc09f0379036bad83984a69bd7396151",
        extension="tar.gz",
    )
    version(
        "2.6.1",
        sha256="348ebeb4db0ea56889a5d13bf49e394fccc0992f620e8c0c61c40185db13ad64",
        extension="tar.gz",
    )
    version(
        "2.6.0",
        sha256="cc1bfa30c4a1de010c0a203c9d22ec810c5de8b76108d5a8174b395573e2ebcc",
        extension="tar.gz",
    )
    version(
        "2.5.1",
        sha256="4c9a754b0e6f2b5e8cd0f5bd643dcfd7863a96b05cd02141d5eb301f2b89f6a3",
        extension="tar.gz",
    )
    version(
        "2.5.0",
        sha256="2f136f9c46069e62b7b818e102527bbe7adc84190dbbcb3eb153b7c5b23d7162",
        extension="tar.gz",
    )
    version(
        "2.4.3",
        sha256="5ff37495a0c8ef4ec501866217b758d8ea474e985b678af757f7906cc56c6d7e",
        extension="tar.gz",
    )
    version(
        "2.4.2",
        sha256="d1de15e9792802f83521b582d1d144ec81e3d5a28c01dbd945288ea29b946729",
        extension="tar.gz",
    )
    version(
        "2.4.1",
        sha256="d5d4a33fd339c7cd721a2836998605b9e492455c7bf755c64c7fd45e07be9016",
        extension="tar.gz",
    )
    version(
        "2.4.0",
        sha256="87c02555f3d1a8ecaff139cf8e7a7167cabd1049c8cc77f1bd8f4484e210d524",
        extension="tar.gz",
    )
    version(
        "2.3.0",
        sha256="6051d45af2ff35031ccc460185fbfa61f7f36ea14f17a0d51a9e62cd7af3709a",
        extension="tar.gz",
    )
    version(
        "2.2.2",
        sha256="135bc03cf07c4624ef2cf581ba5ec52eb44ca1dac15cffb83637e86170980477",
        extension="tar.gz",
    )
    version(
        "2.2.1",
        sha256="68751bf2e17766650ccddb7a5321dd1ac8b34ffa3585db392befbe9ff180ddd9",
        extension="tar.gz",
    )
    version(
        "2.2.0",
        sha256="bc825884fc8506d0fb7b3b5cbb5ad4c7e82b1fe1d7ec861ca33699adfc8100f1",
        extension="tar.gz",
    )
    version(
        "2.1.4",
        sha256="13da3213db834ed2f3a04fedf20a24c4a11b76620e18fed0a0bbcb7484f980bb",
        extension="tar.gz",
    )
    version(
        "2.1.3",
        sha256="ccc7af95eb1e3f63c52a26db08ef9986f7cc500df7a51af0c5e14ed4e7431ad6",
        extension="tar.gz",
    )
    version(
        "2.1.2",
        sha256="4ff1c4eabaaa71829e46e4fb4092a88675f8c2b6708d5ec2b12f991dd9a4de2d",
        extension="tar.gz",
    )
    version(
        "2.1.1",
        sha256="0c48ce4cb9300300d115ae428b1843c4229a54eb286ab0ced953e96ed3f2b9b2",
        extension="tar.gz",
    )
    version(
        "2.1.0",
        sha256="eb9c542b9eb760ea834459a09f8be55891e993a40e277d325bc093b040921e23",
        extension="tar.gz",
    )
    version(
        "2.0.1",
        sha256="ef3c4de8b2353ec0ee229428b1ef1912bc3019b72d4e78be00eecd1f384aeec0",
        extension="tar.gz",
    )
    version(
        "2.0.0",
        sha256="ecfe8717bc61f35f333bc24d27b39e78e67c596e23512bdd97c9b4f28491f0b3",
        extension="tar.gz",
    )

    variant(
        "resource_manager",
        default="none",
        description="Select resource manager templates",
        values=("none", "loadleveler", "lsf", "moab", "pbs", "slurm"),
        multi=False,
    )

    depends_on("python@3.2:", type=("build", "run"), when="@2.5:")
    depends_on("py-setuptools", type="build")
    depends_on("py-pyyaml", type=("build", "run"))

    def setup_run_environment(self, env):
        if not self.spec.variants["resource_manager"].value == "none":
            env.prepend_path(
                "JUBE_INCLUDE_PATH",
                join_path(self.prefix.platform, self.spec.variants["resource_manager"].value),
            )
