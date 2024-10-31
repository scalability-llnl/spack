# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Logstash(Package):
    """
    Logstash is part of the Elastic Stack along with Beats, Elasticsearch
    and Kibana. Logstash is a server-side data processing pipeline that
    ingests data from a multitude of sources simultaneously, transforms it,
    and then sends it to your favorite "stash.
    """

    homepage = "https://artifacts.elastic.co"
    url = "https://artifacts.elastic.co/downloads/logstash/logstash-6.6.0.tar.gz"

    version("6.6.0", sha256="5a9a8b9942631e9d4c3dfb8d47075276e8c2cff343841145550cc0c1cfe7bba7")

    depends_on("c", type="build")  # generated
    depends_on("cxx", type="build")  # generated

    def install(self, spec, prefix):
        install_tree(".", prefix)
