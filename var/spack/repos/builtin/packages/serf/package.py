# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Serf(SConsPackage):
    """Apache Serf - a high performance C-based HTTP client library
    built upon the Apache Portable Runtime (APR) library"""

    homepage  = 'https://serf.apache.org/'
    url       = 'https://archive.apache.org/dist/serf/serf-1.3.9.tar.bz2'

    version('1.3.9', sha256='549c2d21c577a8a9c0450facb5cca809f26591f048e466552240947bdf7a87cc')
    version('1.3.8', sha256='e0500be065dbbce490449837bb2ab624e46d64fc0b090474d9acaa87c82b2590')

    variant('debug', default=False,
            description='Enable debugging info and strict compile warnings')

    depends_on('scons@2.3.0:', type='build')

    depends_on('apr')
    depends_on('apr-util')
    depends_on('openssl')
    depends_on('zlib')

    patch('py3syntax.patch')

    def build_args(self, spec, prefix):
        args = [
            'PREFIX={0}'.format(prefix),
            'APR={0}'.format(spec['apr'].prefix),
            'APU={0}'.format(spec['apr-util'].prefix),
            'OPENSSL={0}'.format(spec['openssl'].prefix),
            'ZLIB={0}'.format(spec['zlib'].prefix),
        ]

        # ZLIB variable is ignored on non-Windows platforms before and
        # including the version 1.3.9:
        # https://www.mail-archive.com/dev@serf.apache.org/msg01359.html
        # The issue is fixed in the trunk. Hopefully, the next stable version
        # will work properly.
        if '@:1.3.9' in self.spec:
            zlib_spec = self.spec['zlib']
            link_flags = [zlib_spec.libs.search_flags]
            link_flags.extend([self.compiler.cc_rpath_arg + d
                               for d in zlib_spec.libs.directories])
            args.append('LINKFLAGS=' + ' '.join(link_flags))
            args.append('CPPFLAGS=' + zlib_spec.headers.cpp_flags)

        if '+debug' in spec:
            args.append('DEBUG=yes')
        else:
            args.append('DEBUG=no')

        # SCons doesn't pass Spack environment variables to the
        # execution environment. Therefore, we can't use Spack's compiler
        # wrappers. Use the actual compilers. SCons seems to RPATH things
        # on its own anyway.
        args.append('CC={0}'.format(self.compiler.cc))

        return args

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
        scons('check')
