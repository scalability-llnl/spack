# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import tempfile


class PyDmTree(PythonPackage):
    """tree is a library for working with nested data structures. In a
    way, tree generalizes the builtin map() function which only
    supports flat sequences, and allows to apply a function to each
    leaf preserving the overall structure."""

    homepage = "https://github.com/deepmind/tree"
    pypi = "dm-tree/dm-tree-0.1.5.tar.gz"

    maintainers = ['aweits']

    version('0.1.5', sha256='a951d2239111dfcc468071bc8ff792c7b1e3192cab5a3c94d33a8b2bda3127fa')

    depends_on('py-setuptools', type='build')
    depends_on('bazel', type='build')
    depends_on('py-six@1.12.0:', type=('build', 'run'))

    @run_after('install')
    def clean(self):
        remove_linked_tree(self.tmp_path)

    def patch(self):
        self.tmp_path = tempfile.mkdtemp(dir='/tmp', prefix='spack')
        env['TEST_TMPDIR'] = self.tmp_path
        env['HOME'] = self.tmp_path
        args = [
            # Don't allow user or system .bazelrc to override build settings
            "'--nohome_rc',\n",
            "'--nosystem_rc',\n",
            # Bazel does not work properly on NFS, switch to /tmp
            "'--output_user_root={0}',\n".format(self.tmp_path),
            "'build',\n",
            # Spack logs don't handle colored output well
            "'--color=no',\n",
            "'--jobs={0}',\n".format(make_jobs),
            # Enable verbose output for failures
            "'--verbose_failures',\n",
            # Show (formatted) subcommands being executed
            "'--subcommands=pretty_print',\n",
            "'--spawn_strategy=local',\n",
            # Ask bazel to explain what it's up to
            # Needs a filename as argument
            "'--explain=explainlogfile.txt',\n",
            # Increase verbosity of explanation,
            "'--verbose_explanations',\n",
            # bazel uses system PYTHONPATH instead of spack paths
            "'--action_env', 'PYTHONPATH={0}',\n".format(env['PYTHONPATH']),
        ]
        filter_file("'build',",
                    ' '.join(args),
                    'setup.py')
