# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Unison(Package):
    """Unison is a file-synchronization tool for OSX, Unix, and
       Windows. It allows two replicas of a collection of files and
       directories to be stored on different hosts (or different disks
       on the same host), modified separately, and then brought up to
       date by propagating the changes in each replica to the
       other."""

    homepage = "https://www.cis.upenn.edu/~bcpierce/unison/"
    url      = "https://github.com/bcpierce00/unison/archive/v2.51.2.tar.gz"
    maintainers = ["hseara"]

    version('2.51.2', sha256='a2efcbeab651be6df69cc9b253011a07955ecb91fb407a219719451197849d5e')
    version('2.48.15v4', sha256='f8c7e982634bbe1ed6510fe5b36b6c5c55c06caefddafdd9edc08812305fdeec')

    depends_on('ocaml@4.10.0:~force-safe-string', type='build')

    patch('large.patch', level=0)
    patch('4.08-compatibility.patch', when='^ocaml@4.08:')

    parallel = False

    def install(self, spec, prefix):
        make('UISTYLE=text DEBUGGING=false THREADS=true')

        mkdirp(prefix.bin)
        install('src/unison', prefix.bin)
        set_executable(join_path(prefix.bin, 'unison'))
