##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
from spack import *


class Git(Package):
    """Git is a free and open source distributed version control
       system designed to handle everything from small to very large
       projects with speed and efficiency."""
    homepage = "http://git-scm.com"
    url      = "https://github.com/git/git/tarball/v2.7.1"

    # See here for info on vulnerable Git versions:
    # http://www.theregister.co.uk/2016/03/16/git_server_client_patch_now/
    # All the following are vulnerable
    # version('2.6.3', 'b711be7628a4a2c25f38d859ee81b423')
    # version('2.6.2', 'da293290da69f45a86a311ad3cd43dc8')
    # version('2.6.1', '4c62ee9c5991fe93d99cf2a6b68397fd')
    # version('2.6.0', 'eb76a07148d94802a1745d759716a57e')
    # version('2.5.4', '3eca2390cf1fa698b48e2a233563a76b')
    # version('2.2.1', 'ff41fdb094eed1ec430aed8ee9b9849c')

    releases = [
        {
            'version': '2.11.1',
            'md5': '2cf960f19e56f27248816809ae896794',
            'md5_manpages': 'ade1e458a34a89d03dda9a6de85976bd',
        },
        {
            'version': '2.11.0',
            'md5': 'c63fb83b86431af96f8e9722ebb3ca01',
            'md5_manpages': '72718851626e5b2267877cc2194a1ac9',
        },
        {
            'version': '2.9.3',
            'md5': 'b0edfc0f3cb046aec7ed68a4b7282a75',
            'md5_manpages': '337165a3b2bbe4814c73075cb6854ca2',
        },
        {
            'version': '2.9.2',
            'md5': '3ff8a9b30fd5c99a02e6d6585ab543fc',
            'md5_manpages': 'c4f415b4fc94cf75a1deb651ba769594',
        },
        {
            'version': '2.9.1',
            'md5': 'a5d806743a992300b45f734d1667ddd2',
            'md5_manpages': '2aa797ff70c704a563c910e04c0f620a',
        },
        {
            'version': '2.9.0',
            'md5': 'bf33a13c2adc05bc9d654c415332bc65',
            'md5_manpages': 'c840c968062251b768ba9852fd29054c',
        },
        {
            'version': '2.8.4',
            'md5': '86afb10254c3803894c9863fb5896bb6',
            'md5_manpages': '8340e772d60ccd04a5da88fa9c976dad',
        },
        {
            'version': '2.8.3',
            'md5': '0e19f31f96f9364fd247b8dc737dacfd',
            'md5_manpages': '553827e1b6c422ecc485499c1a1ae28d',
        },
        {
            'version': '2.8.2',
            'md5': '3d55550880af98f6e35c7f1d7c5aecfe',
            'md5_manpages': '33330463af27eb1238cbc2b4ca100b3a',
        },
        {
            'version': '2.8.1',
            'md5': '1308448d95afa41a4135903f22262fc8',
            'md5_manpages': '87bc202c6f6ae32c1c46c2dda3134ed1',
        },
        {
            'version': '2.8.0',
            'md5': 'eca687e46e9750121638f258cff8317b',
            'md5_manpages': 'd67a7db0f363e8c3b2960cd84ad0373f',
        },
        {
            'version': '2.7.3',
            'md5': 'fa1c008b56618c355a32ba4a678305f6',
            'md5_manpages': '97a525cca7fe38ff6bd7aaa4f0438896',
        },
        {
            'version': '2.7.1',
            'md5': 'bf0706b433a8dedd27a63a72f9a66060',
            'md5_manpages': '19881ca231f73dec91fb456d74943950',
        },
    ]

    for release in releases:
        version(release['version'], release['md5'])
        resource(
            name="git-manpages",
            url="https://www.kernel.org/pub/software/scm/git/"
            "git-manpages-{}.tar.xz".format(release['version']),
            md5=release['md5_manpages'],
            placement="git-manpages",
            when="@{}".format(release['version']))

    depends_on("autoconf", type='build')
    depends_on("curl")
    depends_on("expat")
    depends_on("gettext")
    depends_on("libiconv")
    depends_on("openssl")
    depends_on("pcre")
    depends_on("perl")
    depends_on("zlib")

    def install(self, spec, prefix):
        env['LDFLAGS'] = "-L%s" % spec['gettext'].prefix.lib + " -lintl"
        configure_args = [
            "--prefix=%s" % prefix,
            "--with-curl=%s" % spec['curl'].prefix,
            "--with-expat=%s" % spec['expat'].prefix,
            "--with-iconv=%s" % spec['libiconv'].prefix,
            "--with-libpcre=%s" % spec['pcre'].prefix,
            "--with-openssl=%s" % spec['openssl'].prefix,
            "--with-perl=%s" % join_path(spec['perl'].prefix.bin, 'perl'),
            "--with-zlib=%s" % spec['zlib'].prefix,
        ]

        which('autoreconf')('-i')
        configure(*configure_args)
        if sys.platform == "darwin":
            # Don't link with -lrt; the system has no (and needs no) librt
            filter_file(r' -lrt$', '', 'Makefile')
        make()
        make("install")

        with working_dir("git-manpages"):
            install_tree("man1", prefix.share_man1)
            install_tree("man5", prefix.share_man5)
            install_tree("man7", prefix.share_man7)
