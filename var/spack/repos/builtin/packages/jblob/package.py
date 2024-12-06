# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Jblob(Package):
    """
    The German Climate Computing Center
    (DKRZ: Deutsches Klimarechenzentrum GmbH)
    provides a Long Term Archiving Service for large research
    data sets which are relevant for climate or Earth system research.
    """

    homepage = "https://cera-www.dkrz.de/WDCC/ui/cerasearch"
    url = "https://cera-www.dkrz.de/jblob/jblob-3.0.zip"

    maintainers("ajkotobi")

    version("3.0", sha256="576b5956358386a8832c6d1d13c410705e54888354a10cfd4f094513458067e4")

    depends_on("java@8:", type="run")

    def setup_run_environment(self, env):
        env.set("JAVA_HOME", self.spec["java"].prefix)

    def install(self, spec, prefix):
        filter_file("/opt/jblob-" + self.version, prefix, "jblob")

        mkdir(prefix.bin)
        install("jblob", prefix.bin)
        install_tree("lib", prefix.lib)
        install_tree("docs", prefix.docs)
