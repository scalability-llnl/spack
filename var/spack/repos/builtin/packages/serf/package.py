# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Serf(SConsPackage):
    """Apache Serf - a high performance C-based HTTP client library
    built upon the Apache Portable Runtime (APR) library"""

    homepage = "https://serf.apache.org/"
    url = "https://archive.apache.org/dist/serf/serf-1.3.9.tar.bz2"

    maintainers("cosmicexplorer")

    license("Apache-2.0")

    version("1.3.10", sha256="be81ef08baa2516ecda76a77adf7def7bc3227eeb578b9a33b45f7b41dc064e6")
    version("1.3.9", sha256="549c2d21c577a8a9c0450facb5cca809f26591f048e466552240947bdf7a87cc")
    version("1.3.8", sha256="e0500be065dbbce490449837bb2ab624e46d64fc0b090474d9acaa87c82b2590")

    depends_on("c", type="build")  # generated

    variant(
        "debug", default=False, description="Enable debugging info and strict compile warnings"
    )

    depends_on("apr")
    depends_on("apr-util")
    depends_on("openssl")
    depends_on("python+pythoncmd", type="build")
    depends_on("scons@2.3.0:", type="build")
    depends_on("uuid")
    depends_on("zlib-api")

    patch("py3syntax.patch", when="@:1.3.9")
    patch("py3-hashbang.patch")

    def build_args(self, spec, prefix):
        args = {
            "PREFIX": prefix,
            "APR": spec["apr"].prefix,
            "APU": spec["apr-util"].prefix,
            "OPENSSL": spec["openssl"].prefix,
            "ZLIB": spec["zlib-api"].prefix,
            "DEBUG": "yes" if "+debug" in spec else "no",
        }

        # SCons doesn't pass Spack environment variables to the
        # execution environment. Therefore, we can't use Spack's compiler
        # wrappers. Use the actual compilers. SCons seems to RPATH things
        # on its own anyway.
        args["CC"] = self.compiler.cc

        # Old versions of serf ignore the ZLIB variable on non-Windows platforms.
        # Also, there is no UUID variable to specify its installation location.
        # Pass explicit link flags for both.
        library_dirs = []
        include_dirs = []
        for dep in spec.dependencies(deptype="link"):
            query = self.spec[dep.name]
            library_dirs.extend(query.libs.directories)
            include_dirs.extend(query.headers.directories)

        rpath = self.compiler.cc_rpath_arg
        args["LINKFLAGS"] = "-L" + " -L".join(library_dirs)
        args["LINKFLAGS"] += " " + rpath + (" " + rpath).join(library_dirs)
        args["CPPFLAGS"] = "-I" + " -I".join(include_dirs)

        return [key + "=" + value for key, value in args.items()]

    def build_test(self):
        # FIXME: Several test failures:
        #
        # There were 14 failures:
        # 1) test_ssl_trust_rootca
        # 2) test_ssl_certificate_chain_with_anchor
        # 3) test_ssl_certificate_chain_all_from_server
        # 4) test_ssl_no_servercert_callback_allok
        # 5) test_ssl_large_response
        # 6) test_ssl_large_request
        # 7) test_ssl_client_certificate
        # 8) test_ssl_future_server_cert
        # 9) test_setup_ssltunnel
        # 10) test_ssltunnel_basic_auth
        # 11) test_ssltunnel_basic_auth_server_has_keepalive_off
        # 12) test_ssltunnel_basic_auth_proxy_has_keepalive_off
        # 13) test_ssltunnel_basic_auth_proxy_close_conn_on_200resp
        # 14) test_ssltunnel_digest_auth
        #
        # These seem to be related to:
        # https://groups.google.com/forum/#!topic/serf-dev/YEFTTdF1Qwc
        scons("check")
