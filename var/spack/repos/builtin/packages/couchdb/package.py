# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Couchdb(AutotoolsPackage):
    """A CouchDB server hosts named databases, which store documents. Each document
    is uniquely named in the database, and CouchDB provides a RESTful HTTP API
    for reading and updating (add, edit, delete) database documents."""

    homepage = "https://couchdb.apache.org/"
    url      = "http://archive.apache.org/dist/couchdb/source/3.1.0/apache-couchdb-3.1.0.tar.gz"

    version('3.1.0', sha256='4867c796a1ff6f0794b7bd3863089ea6397bd5c47544f9b97db8cdacff90f8ed')
    version('3.0.1', sha256='08d61d5c779957d074d5097f28a2dfc9eb518af3c479d5318135ff31212cc522')
    version('3.0.0', sha256='d109bb1a70fe746c04a9bf79a2bb1096cb949c750c29dbd196e9c2efd4167fd9')

    depends_on('icu4c')
    depends_on('openssl')
    depends_on('curl')
    depends_on('node-js@6:')
    depends_on('mozjs@1.8.5')
    depends_on('gmake',    type='build')
    depends_on('help2man', type='build')
    depends_on('python',   type=('build', 'run'))
    depends_on('erlang@:22.99', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.set('CPATH', self.spec['mozjs'].prefix.include.js)

    def configure_args(self):
        args = ['--disable-docs']
        return args

    def install(self, spec, prefix):
        make('release')
        with working_dir('rel/couchdb/'):
            install_tree('.', prefix)
