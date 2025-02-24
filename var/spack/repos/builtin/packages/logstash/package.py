# Copyright Spack Project Developers. See COPYRIGHT file for details.
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
    url = "https://artifacts.elastic.co/downloads/logstash/logstash-8.15.2-linux-x86_64.tar.gz"

    version("8.15.2", sha256="fc75c8cad1016b07f7aeeeeb7ea23f4195ab1beee2ced282f11ff6d0e84f7e51")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2019-7612
        version("6.6.0", sha256="5a9a8b9942631e9d4c3dfb8d47075276e8c2cff343841145550cc0c1cfe7bba7")

    depends_on("java@11:")

    def url_for_version(self, version):
        if self.spec.satisfies("@:6"):
            return f"https://artifacts.elastic.co/downloads/logstash/logstash-{version}.tar.gz"
        else:
            return f"https://artifacts.elastic.co/downloads/logstash/logstash-{version}-linux-x86_64.tar.gz"

    def install(self, spec, prefix):
        install_tree(".", prefix)

    def setup_run_environment(self, env):
        # do not use the bundled jdk
        env.set("LS_JAVA_HOME", self.spec["java"].home)
