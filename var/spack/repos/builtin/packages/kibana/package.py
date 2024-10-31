# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kibana(Package):
    """Kibana lets you visualize your Elasticsearch data and navigate the
    Elastic Stack"""

    homepage = "https://www.elastic.co/products/kibana"
    url = "https://artifacts.elastic.co/downloads/kibana/kibana-6.4.0-linux-x86_64.tar.gz"

    version("6.4.0", sha256="df2056105a08c206a1adf9caed09a152a53429a0f1efc1ba3ccd616092d78aee")

    depends_on("cxx", type="build")  # generated

    depends_on("java", type="run")

    def install(self, spec, prefix):
        install_tree(".", join_path(prefix, "."))
