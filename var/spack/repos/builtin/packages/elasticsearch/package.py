# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Elasticsearch(Package):
    """Elasticsearch is a search engine based on Lucene. It provides a
    distributed, multitenant-capable full-text search engine with an HTTP web
    interface and schema-free JSON documents.
    """

    homepage = "https://www.elastic.co/"
    url = "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.15.2-linux-x86_64.tar.gz"

    version("8.15.2", sha256="0b6905ede457be9d1d73d0b6be1c3a7c7c6220829846b532f2604ad30ba7308f")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2018-3831
        version("6.4.0", sha256="e9786efb5cecd12adee2807c7640ba9a1ab3b484d2e87497bb8d0b6df0e24f01")
        version("6.3.0", sha256="0464127140820d82b24bd2830232131ea85bcd49267a8bc7365e4fa391dee2a3")
        version("6.2.4", sha256="91e6f1ea1e1dd39011e7a703d2751ca46ee374665b08b0bfe17e0c0c27000e8e")

    depends_on("java", type="run")

    def url_for_version(self, version):
        if self.spec.satisfies("@:6"):
            return f"https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{version}.tar.gz"
        else:
            return f"https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{version}-linux-x86_64.tar.gz"

    def install(self, spec, prefix):
        dirs = ["bin", "config", "lib", "modules", "plugins"]

        for d in dirs:
            install_tree(d, join_path(prefix, d))
