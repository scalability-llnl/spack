# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class AperturePhotometry(Package):
    """Aperture Photometry Tool APT is software for astronomical research"""

    homepage = "http://www.aperturephotometry.org/aptool/"
    url      = "http://www.aperturephotometry.org/aptool/wp-content/plugins/download-monitor/download.php?id=1"

    version('2.8.4', '28ae136c708a3ebcb83632230e119a03ca1a65499006ab69dc76e21b4921f465', extension='tar.gz')
    version('2.8.2', 'cb29eb39a630dc5d17c02fb824c69571fe1870a910a6acf9115c5f76fd89dd7e', extension='tar.gz')

    depends_on('java')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'APT.jar'
        install(jar_file, prefix.bin)
        java = join_path(self.spec['java'].prefix, 'bin', 'java')
        script_sh = join_path(os.path.dirname(__file__), "APT.sh")
        script = join_path(prefix.bin, "apt")
        install(script_sh, script)
        set_executable(script)
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('APT.jar', join_path(prefix.bin, 'APT.jar'),
                    script, **kwargs)
