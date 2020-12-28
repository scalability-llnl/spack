# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os.path

from spack.package import *


class Cromwell(Package):
    """Cromwell is a Workflow Management System geared towards scientific
       workflows.
    """

    homepage = "http://cromwell.readthedocs.io/"
    url      = "https://github.com/broadinstitute/cromwell/releases/download/44/cromwell-44.jar"

    version('44', sha256='8b411673f6b3c835c6031db3094a7404b9a371133794046fd295719d61e56db0', expand=False)

    depends_on('java@8', type='run')

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        jar_file = 'cromwell-{0}.jar'.format(self.version)
        install(jar_file, prefix.bin)

        # Set up a helper script to call java on the jar file,
        # explicitly codes the path for java and the jar file.
        script_sh = join_path(os.path.dirname(__file__), "cromwell.sh")
        script = prefix.bin.cromwell
        install(script_sh, script)
        set_executable(script)

        # Munge the helper script to explicitly point to java and the
        # jar file.
        java = self.spec['java'].prefix.bin.java
        kwargs = {'ignore_absent': False, 'backup': False, 'string': False}
        filter_file('^java', java, script, **kwargs)
        filter_file('cromwell.jar', join_path(prefix.bin, jar_file),
                    script, **kwargs)
