# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil
import tempfile


class Singularity(Package):
    '''Singularity is a container technology focused on building portable
       encapsulated environments to support "Mobility of Compute" For older
       versions of Singularity (pre 3.0) you should use singularity-legacy,
       which has a different install base (Autotools).
    '''

    homepage = "https://www.sylabs.io/singularity/"
    url      = "https://github.com/sylabs/singularity/releases/download/v3.1.0/singularity-3.1.0.tar.gz"
    git      = "https://github.com/singularityware/singularity.git"

    # ##########################################################################
    # 3.1.0 Release Branch (GoLang)

    version('develop', branch='master')
    version('3.1.0', 'd3a963ae85c527521434723b1cf8dda9594bf6c6')

    # Shared dependencies

    depends_on('go')
    depends_on('libuuid')
    depends_on('libgpg-error')
    depends_on('squashfs', type='run')
    depends_on('git')

    phases = ['configure', 'build', 'install']

    def configure(self, spec, prefix):

        # $GOPATH/src/github.com/sylabs/singularity
        tmpgo = prepare_gopath()

        # Remove old install
        if os.path.exists(tmpgo):
            shutil.rmtree(tmpgo)

        shutil.move(os.getcwd(), tmpgo)

        with working_dir(tmpgo):
            configure = Executable('./mconfig --prefix=%s' % prefix)
            configure()

    def build(self, spec, prefix):

        # $GOPATH/src/github.com/sylabs/singularity
        tmpgo = prepare_gopath()

        # The package needs to be in GOPATH in order for it to be found
        with working_dir(tmpgo):
            make('-C', 'builddir', parallel=False)

    def install(self, spec, prefix):
        with working_dir(prepare_gopath()):
            make('install', '-C', 'builddir', parallel=False)


def prepare_gopath():
    '''The repository needed to be cloned into
          $GOPATH/src/github.com/sylabs/singularity to begin with. To
       mimic this, we create the structure in a temporary directory and
       work from there. If we don't do that, when we cd into the builddir
       to make, the entire set of source files aren't found on GOPATH. But
       we cannot add the default cloned source to the GOPATH because it
       will append the default src/github.com. If we lose working from the
       present working directory, we also risk losing the vendor folder.
    '''
    gopath = os.path.join(tempfile.gettempdir(), 'go')
    tmpgo = os.path.join(gopath, 'src', 'github.com', 'sylabs', 'singularity')

    # Create gopath
    if not os.path.exists(gopath):
        os.makedirs(gopath)

    # If the user has go installed (and previous libraries, use them)
    user_gopath = os.environ.get('GOPATH')
    if user_gopath is not None:
        gopath = gopath + ':' + user_gopath

    os.environ['GOPATH'] = gopath
    return tmpgo
