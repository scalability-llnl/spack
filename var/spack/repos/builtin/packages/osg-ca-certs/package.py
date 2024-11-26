# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class OsgCaCerts(Package):
    """OSG Packaging of the IGTF CA Certs and OSG-specific CAs,
    in the OpenSSL 1.0.* format."""

    homepage = "http://repo.opensciencegrid.org/cadist"
    git = "https://github.com/opensciencegrid/osg-certificates.git"

    _igtf_base_url = "https://dist.eugridpma.info/distribution/igtf/{igtf_version}/igtf-policy-installation-bundle-{igtf_version}.tar.gz"
    _letsencrypt_base_url = "https://github.com/opensciencegrid/letsencrypt-certificates/archive/v{letsencrypt_version}/letsencrypt-certificates.tar.gz"

    maintainers("wdconinc")

    releases = [
        {
            "osg_version": "1.119",
            "igtf_version": "1.128",
            "osg_commit": "1f7abbe392e339aae28625a4016bc98d58ad7cab",
            "igtf_sha256": "1385e2206b4088cbad94264e2c252ad431f075f88a427cdee4ed523df95b9ab7",
        }
    ]

    for release in releases:
        _version = "{0}.igtf.{1}".format(release["osg_version"], release["igtf_version"])

        version(_version, commit=release["osg_commit"])

        resource(
            name="igtf-{igtf_version}".format(igtf_version=release["igtf_version"]),
            url=_igtf_base_url.format(igtf_version=release["igtf_version"]),
            sha256=release["igtf_sha256"],
            when="@{0}".format(_version),
        )

    resource(
        name="letsencrypt",
        git="https://github.com/opensciencegrid/letsencrypt-certificates",
        branch="master",
        destination="letsencrypt-certificates-master",
    )

    depends_on("openssl")

    def setup_build_environment(self, env):
        env.set("OSG_CERTS_VERSION", self.version[:2])
        env.set("OUR_CERTS_VERSION", str(self.version[:2]) + "NEW")
        env.set("IGTF_CERTS_VERSION", self.version[3:])
        env.set("CADIST", join_path(self.stage.source_path, "certificates"))
        env.set("PKG_NAME", self.spec.name)

    def setup_run_environment(self, env):
        env.set("X509_CERT_DIR", join_path(self.prefix, "certificates"))

    def install(self, spec, prefix):
        copy_tree(
            "letsencrypt-certificates-master/letsencrypt-certificates", "letsencrypt-certificates"
        )
        Executable(join_path(self.stage.source_path, "build-certificates-dir.sh"))()
        install_tree("certificates", join_path(prefix, "certificates"))
