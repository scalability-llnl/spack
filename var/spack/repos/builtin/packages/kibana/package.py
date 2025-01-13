# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Kibana(Package):
    """Kibana lets you visualize your Elasticsearch data and navigate the
    Elastic Stack"""

    homepage = "https://www.elastic.co/products/kibana"
    url = "https://artifacts.elastic.co/downloads/kibana/kibana-6.4.0-linux-x86_64.tar.gz"

    version("8.15.2", sha256="b1f8082a4200867078170e92ad299e293ee514f5fdbb96b7a0d1de17a880d1eb")
    with default_args(deprecated=True):
        # https://nvd.nist.gov/vuln/detail/CVE-2019-7609
        version("6.4.0", sha256="df2056105a08c206a1adf9caed09a152a53429a0f1efc1ba3ccd616092d78aee")

    depends_on("java", type="run")

    def install(self, spec, prefix):
        install_tree(".", join_path(prefix, "."))
