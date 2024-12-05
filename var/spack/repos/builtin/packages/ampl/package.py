# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Ampl(Package):
    """AMPL integrates a modeling language for describing optimization data, variables,
    objectives, and constraints; a command language for debugging models and analyzing
    results; and a scripting language for manipulating data and implementing
    optimization strategies."""

    homepage = "https://ampl.com/"
    manual_download = True

    maintainers("robgics")

    # Use the version as you would expect the user to know it, not necessarily the
    # version as it appears in the file name.  To get the checksum, use sha256sum.
    version("20220525", sha256="24f91bc5a53c9a4e7127062599a0b33348c977f666a56031a60c6ee2be2745d9")
    version("20210226", sha256="d9ffaed591c0491e311a44c2b246d9d81785f6c0b2747a7e32a783e522e18450")
    version("20190529", sha256="c35a87d85055ae5fe41b68d4b4458f1fdbf80643890501eeaad35b134cb11a2d")

    # Licensing
    license_required = True
    license_comment = "#"
    license_files = ["ampl.lic"]
    license_url = "https://ampl.com/resources/floating-licenses/installation/"

    variant("api", default=True, description="Install the AMPL API")
    variant("ide", default=True, description="Install the AMPL IDE")

    resource(
        when="@:20210226 +api",
        name="amplapi",
        url="file://{0}/amplapi-linux64.2.0.0.zip".format(os.getcwd()),
        sha256="a4abe111f142b862f11fcd8700f964b688d5d2291e9e055f6e7adbd92b0e243a",
        destination="",
        placement="amplapi",
    )
    resource(
        when="@20220525 +api",
        name="amplapi",
        url="file://{0}/amplapi-linux64.2.0.8.zip".format(os.getcwd()),
        sha256="6ea572827a9e69c4e285e01c9c2e235af6237acd6052d109c5d7e9762b7a8bd7",
        destination="",
        placement="amplapi",
    )
    resource(
        when="@:20210226 +ide",
        name="amplide",
        url="file://{0}/amplide-linux64.3.5.tgz".format(os.getcwd()),
        sha256="c2163896df672b71901d2e46cd5cf1c1c4f0451e478ef32d0971705aaf86d6ac",
        destination="",
        placement="amplide",
    )
    resource(
        when="@20220525 +ide",
        name="amplide",
        url="file://{0}/amplide.linux64.3.6.8.tgz".format(os.getcwd()),
        sha256="f482afb7a2bb977d8ca68f288b41b9691ac501bd2d5f4dbc11b42c8dc19b366a",
        destination="",
        placement="amplide",
    )
    resource(
        when="@:20210226",
        name="ampl_lic",
        url="file://{0}/ampl_lic.linux-intel64.20210618.tgz".format(os.getcwd()),
        sha256="f5c38638d6cc99c85e0d6de001722b64a03e2adeaf5aed9ed622401654d9ff33",
        destination="",
        placement="",
    )
    resource(
        when="@20220525",
        name="ampl_lic",
        url="file://{0}/ampl_lic.linux-intel64.20210929.tgz".format(os.getcwd()),
        sha256="19dc1a511c59a6c2917dec50b495ed9850a6a3c8ec84e42979656916f2cbafb4",
        destination="",
        placement="",
    )

    def url_for_version(self, version):
        return "file://{0}/ampl.linux-intel64.{1}.tgz".format(os.getcwd(), version)

    def setup_run_environment(self, env):
        env.prepend_path("PATH", self.prefix)
        if self.spec.satisfies("+ide"):
            env.prepend_path("PATH", join_path(self.prefix, "amplide"))

    def install(self, spec, prefix):
        install_tree(".", prefix)

        for res in self._get_needed_resources():
            if res.name == "ampl_lic":
                res_path = join_path(res.fetcher.stage.source_path, res.name)
                install(res_path, prefix)
