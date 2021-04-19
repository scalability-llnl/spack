# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest
import os
import shutil
import llnl.util.filesystem as fs

import spack.spec
import spack.environment as ev
from spack.main import SpackCommand
from spack.environment import SpackEnvironmentError

develop = SpackCommand('develop')
env = SpackCommand('env')


@pytest.mark.usefixtures(
    'mutable_mock_env_path', 'mock_packages', 'mock_fetch')
class TestDevelop(object):
    def check_develop(self, env, spec, path=None):
        path = path or spec.name

        # check in memory representation
        matching = [entry for entry in env.dev_specs
                    if spack.spec.Spec(entry['spec']).satisfies(spec)]
        assert len(matching) == 1
        dev_specs_entry = matching[0]
        assert dev_specs_entry['path'] == path
        assert dev_specs_entry['spec'] == str(spec)

        # check yaml representation
        yaml = ev.config_dict(env.yaml)
        yaml_matching = [entry for entry in yaml['develop']
                         if spack.spec.Spec(entry['spec']).satisfies(spec)]
        assert len(yaml_matching) == 1
        yaml_entry = yaml_matching[0]
        assert yaml_entry['spec'] == str(spec)
        if path == spec.name:
            # default paths aren't written out
            assert 'path' not in yaml_entry
        else:
            assert yaml_entry['path'] == path

    def test_develop_no_path_no_clone(self):
        env('create', 'test')
        with ev.read('test') as e:
            # develop checks that the path exists
            fs.mkdirp(os.path.join(e.path, 'mpich'))
            develop('--no-clone', 'mpich@1.0')
            self.check_develop(e, spack.spec.Spec('mpich@1.0'))

    def test_develop_no_clone(self, tmpdir):
        env('create', 'test')
        with ev.read('test') as e:
            develop('--no-clone', '-p', str(tmpdir), 'mpich@1.0')
            self.check_develop(e, spack.spec.Spec('mpich@1.0'), str(tmpdir))

    def test_develop(self):
        env('create', 'test')
        with ev.read('test') as e:
            develop('mpich@1.0')
            self.check_develop(e, spack.spec.Spec('mpich@1.0'))

    def test_develop_no_args(self):
        env('create', 'test')
        with ev.read('test') as e:
            # develop and remove it
            develop('mpich@1.0')
            shutil.rmtree(os.path.join(e.path, 'mpich'))

            # test develop with no args
            develop()
            self.check_develop(e, spack.spec.Spec('mpich@1.0'))

    def test_develop_twice(self):
        env('create', 'test')
        with ev.read('test') as e:
            develop('mpich@1.0')
            self.check_develop(e, spack.spec.Spec('mpich@1.0'))

            develop('mpich@1.0')
            # disk representation isn't updated unless we write
            # second develop command doesn't change it, so we don't write
            # but we check disk representation
            e.write()
            self.check_develop(e, spack.spec.Spec('mpich@1.0'))
            assert len(e.dev_specs) == 1

    def test_develop_update_path(self, tmpdir):
        env('create', 'test')
        with ev.read('test') as e:
            develop('mpich@1.0')
            develop('-p', str(tmpdir), 'mpich@1.0')
            self.check_develop(e, spack.spec.Spec('mpich@1.0'), str(tmpdir))
            assert len(e.dev_specs) == 1

    def test_develop_same_package_different_spec(self):
        """We allow for the same package listed multiple times"""
        env('create', 'test')
        with ev.read('test') as e:
            develop('mpich@1.2.3 +shared')
            develop('mpich@1.2.3 ~shared')
            self.check_develop(e, spack.spec.Spec('mpich@1.2.3 +shared'))
            self.check_develop(e, spack.spec.Spec('mpich@1.2.3 ~shared'))

    def test_develop_more_specific_spec_errors(self):
        """When a new develop spec is included in an existing one we error"""
        env('create', 'test')
        with ev.read('test'):
            develop('mpich@1.0.0')
            develop('mpich@1')

            msg = "mpich@1.1 is included in mpich@1"
            with pytest.raises(SpackEnvironmentError, match=msg):
                develop('mpich@1.1')
