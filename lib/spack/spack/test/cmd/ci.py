# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import filecmp
import json
import os
import pytest
from jsonschema import validate, ValidationError

import spack
import spack.ci as ci
import spack.compilers as compilers
import spack.config
import spack.environment as ev
import spack.hash_types as ht
import spack.main
import spack.paths as spack_paths
import spack.repo as repo
from spack.schema.buildcache_spec import schema as spec_yaml_schema
from spack.schema.database_index import schema as db_idx_schema
from spack.schema.gitlab_ci import schema as gitlab_ci_schema
from spack.spec import Spec, CompilerSpec
from spack.util.mock_package import MockPackageMultiRepo
import spack.util.executable as exe
import spack.util.spack_yaml as syaml
import spack.util.gpg


ci_cmd = spack.main.SpackCommand('ci')
env_cmd = spack.main.SpackCommand('env')
mirror_cmd = spack.main.SpackCommand('mirror')
gpg_cmd = spack.main.SpackCommand('gpg')
install_cmd = spack.main.SpackCommand('install')
uninstall_cmd = spack.main.SpackCommand('uninstall')
buildcache_cmd = spack.main.SpackCommand('buildcache')
git = exe.which('git', required=True)


pytestmark = pytest.mark.maybeslow


@pytest.fixture()
def env_deactivate():
    yield
    spack.environment._active_environment = None
    os.environ.pop('SPACK_ENV', None)


def set_env_var(key, val):
    os.environ[key] = val


def test_specs_staging(config):
    """Make sure we achieve the best possible staging for the following
spec DAG::

        a
       /|
      c b
        |\
        e d
          |\
          f g

In this case, we would expect 'c', 'e', 'f', and 'g' to be in the first stage,
and then 'd', 'b', and 'a' to be put in the next three stages, respectively.

"""
    default = ('build', 'link')

    mock_repo = MockPackageMultiRepo()
    g = mock_repo.add_package('g', [], [])
    f = mock_repo.add_package('f', [], [])
    e = mock_repo.add_package('e', [], [])
    d = mock_repo.add_package('d', [f, g], [default, default])
    c = mock_repo.add_package('c', [], [])
    b = mock_repo.add_package('b', [d, e], [default, default])
    mock_repo.add_package('a', [b, c], [default, default])

    with repo.use_repositories(mock_repo):
        spec_a = Spec('a')
        spec_a.concretize()

        spec_a_label = ci.spec_deps_key(spec_a)
        spec_b_label = ci.spec_deps_key(spec_a['b'])
        spec_c_label = ci.spec_deps_key(spec_a['c'])
        spec_d_label = ci.spec_deps_key(spec_a['d'])
        spec_e_label = ci.spec_deps_key(spec_a['e'])
        spec_f_label = ci.spec_deps_key(spec_a['f'])
        spec_g_label = ci.spec_deps_key(spec_a['g'])

        spec_labels, dependencies, stages = ci.stage_spec_jobs([spec_a])

        assert (len(stages) == 4)

        assert (len(stages[0]) == 4)
        assert (spec_c_label in stages[0])
        assert (spec_e_label in stages[0])
        assert (spec_f_label in stages[0])
        assert (spec_g_label in stages[0])

        assert (len(stages[1]) == 1)
        assert (spec_d_label in stages[1])

        assert (len(stages[2]) == 1)
        assert (spec_b_label in stages[2])

        assert (len(stages[3]) == 1)
        assert (spec_a_label in stages[3])


def test_ci_generate_with_env(tmpdir, mutable_mock_env_path, env_deactivate,
                              install_mockery, mock_packages):
    """Make sure we can get a .gitlab-ci.yml from an environment file
       which has the gitlab-ci, cdash, and mirrors sections."""
    mirror_url = 'https://my.fake.mirror'
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  definitions:
    - bootstrap:
      - cmake@3.4.3
    - old-gcc-pkgs:
      - archive-files
      - callpath
      # specify ^openblas-with-lapack to ensure that builtin.mock repo flake8
      # package (which can also provide lapack) is not chosen, as it violates
      # a package-level check which requires exactly one fetch strategy (this
      # is apparently not an issue for other tests that use it).
      - hypre@0.2.15 ^openblas-with-lapack
  specs:
    - matrix:
      - [$old-gcc-pkgs]
  mirrors:
    some-mirror: {0}
  gitlab-ci:
    bootstrap:
      - name: bootstrap
        compiler-agnostic: true
    mappings:
      - match:
          - arch=test-debian6-core2
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
    service-job-attributes:
      image: donotcare
      tags: [donotcare]
  cdash:
    build-group: Not important
    url: https://my.fake.cdash
    project: Not used
    site: Nothing
""".format(mirror_url))
    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            found_spec = False
            for ci_key in yaml_contents.keys():
                if '(bootstrap)' in ci_key:
                    found_spec = True
                    assert('cmake' in ci_key)
            assert(found_spec)
            assert('stages' in yaml_contents)
            assert(len(yaml_contents['stages']) == 6)
            assert(yaml_contents['stages'][0] == 'stage-0')
            assert(yaml_contents['stages'][5] == 'stage-rebuild-index')

            assert('rebuild-index' in yaml_contents)
            rebuild_job = yaml_contents['rebuild-index']
            expected = 'spack buildcache update-index --keys -d {0}'.format(
                mirror_url)
            assert(rebuild_job['script'][0] == expected)


def _validate_needs_graph(yaml_contents, needs_graph, artifacts):
    for job_name, job_def in yaml_contents.items():
        for needs_def_name, needs_list in needs_graph.items():
            if job_name.startswith(needs_def_name):
                # check job needs against the expected needs definition
                j_needs = job_def['needs']
                print('job {0} needs:'.format(needs_def_name))
                print([j['job'] for j in j_needs])
                print('expected:')
                print([nl for nl in needs_list])
                assert all([job_needs['job'][:job_needs['job'].index('/')]
                           in needs_list for job_needs in j_needs])
                assert(all([nl in
                           [n['job'][:n['job'].index('/')] for n in j_needs]
                           for nl in needs_list]))
                assert all([job_needs['artifacts'] == artifacts
                           for job_needs in j_needs])
                break


def test_ci_generate_bootstrap_gcc(tmpdir, mutable_mock_env_path,
                                   env_deactivate, install_mockery,
                                   mock_packages):
    """Test that we can bootstrap a compiler and use it as the
    compiler for a spec in the environment"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  definitions:
    - bootstrap:
      - gcc@3.0
      - gcc@2.0
  specs:
    - dyninst%gcc@3.0
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    bootstrap:
      - name: bootstrap
        compiler-agnostic: true
    mappings:
      - match:
          - arch=test-debian6-x86_64
        runner-attributes:
          tags:
            - donotcare
""")

    needs_graph = {
        '(bootstrap) conflict': [],
        '(bootstrap) gcc': [
            '(bootstrap) conflict',
        ],
        '(specs) libelf': [
            '(bootstrap) gcc',
        ],
        '(specs) libdwarf': [
            '(bootstrap) gcc',
            '(specs) libelf',
        ],
        '(specs) dyninst': [
            '(bootstrap) gcc',
            '(specs) libelf',
            '(specs) libdwarf',
        ],
    }

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            _validate_needs_graph(yaml_contents, needs_graph, False)


def test_ci_generate_bootstrap_artifacts_buildcache(tmpdir,
                                                    mutable_mock_env_path,
                                                    env_deactivate,
                                                    install_mockery,
                                                    mock_packages):
    """Test that we can bootstrap a compiler when artifacts buildcache
    is turned on"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  definitions:
    - bootstrap:
      - gcc@3.0
  specs:
    - dyninst%gcc@3.0
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    bootstrap:
      - name: bootstrap
        compiler-agnostic: true
    mappings:
      - match:
          - arch=test-debian6-x86_64
        runner-attributes:
          tags:
            - donotcare
    enable-artifacts-buildcache: True
""")

    needs_graph = {
        '(bootstrap) conflict': [],
        '(bootstrap) gcc': [
            '(bootstrap) conflict',
        ],
        '(specs) libelf': [
            '(bootstrap) gcc',
            '(bootstrap) conflict',
        ],
        '(specs) libdwarf': [
            '(bootstrap) gcc',
            '(bootstrap) conflict',
            '(specs) libelf',
        ],
        '(specs) dyninst': [
            '(bootstrap) gcc',
            '(bootstrap) conflict',
            '(specs) libelf',
            '(specs) libdwarf',
        ],
    }

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            yaml_contents = syaml.load(contents)
            _validate_needs_graph(yaml_contents, needs_graph, True)


def test_ci_generate_with_env_missing_section(tmpdir, mutable_mock_env_path,
                                              env_deactivate, install_mockery,
                                              mock_packages):
    """Make sure we get a reasonable message if we omit gitlab-ci section"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
""")

    expect_out = 'Error: Environment yaml does not have "gitlab-ci" section'

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')

        with ev.read('test'):
            output = ci_cmd('generate', fail_on_error=False, output=str)
            assert(expect_out in output)


def test_ci_generate_with_cdash_token(tmpdir, mutable_mock_env_path,
                                      env_deactivate, install_mockery,
                                      mock_packages):
    """Make sure we it doesn't break if we configure cdash"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    enable-artifacts-buildcache: True
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
  cdash:
    build-group: Not important
    url: https://my.fake.cdash
    project: Not used
    site: Nothing
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')

        with ev.read('test'):
            fake_token = 'notreallyatokenbutshouldnotmatter'
            os.environ['SPACK_CDASH_AUTH_TOKEN'] = fake_token
            copy_to_file = str(tmpdir.join('backup-ci.yml'))
            try:
                output = ci_cmd('generate', '--copy-to', copy_to_file, output=str)
            finally:
                del os.environ['SPACK_CDASH_AUTH_TOKEN']
            # That fake token should still have resulted in being unable to
            # register build group with cdash, but the workload should
            # still have been generated.
            expect = 'Problem populating buildgroup'
            assert(expect in output)

            dir_contents = os.listdir(tmpdir.strpath)

            print(dir_contents)

            assert('backup-ci.yml' in dir_contents)

            orig_file = str(tmpdir.join('.gitlab-ci.yml'))

            assert(filecmp.cmp(orig_file, copy_to_file) is True)


def test_ci_generate_with_custom_scripts(tmpdir, mutable_mock_env_path,
                                         env_deactivate, install_mockery,
                                         mock_packages, monkeypatch):
    """Test use of user-provided scripts"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          variables:
            ONE: plain-string-value
            TWO: ${INTERP_ON_BUILD}
          before_script:
            - mkdir /some/path
            - pushd /some/path
            - git clone ${SPACK_REPO}
            - cd spack
            - git checkout ${SPACK_REF}
            - popd
          script:
            - spack -d ci rebuild
          after_script:
            - rm -rf /some/path/spack
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            monkeypatch.setattr(spack.main, 'get_version', lambda: '0.15.3')
            ci_cmd('generate', '--output-file', outputfile)

            with open(outputfile) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)

                found_it = False

                assert('variables' in yaml_contents)
                global_vars = yaml_contents['variables']
                assert('SPACK_VERSION' in global_vars)
                assert(global_vars['SPACK_VERSION'] == '0.15.3')
                assert('SPACK_CHECKOUT_VERSION' in global_vars)
                assert(global_vars['SPACK_CHECKOUT_VERSION'] == 'v0.15.3')

                for ci_key in yaml_contents.keys():
                    ci_obj = yaml_contents[ci_key]
                    if 'archive-files' in ci_key:
                        # Ensure we have variables, possibly interpolated
                        assert('variables' in ci_obj)
                        var_d = ci_obj['variables']
                        assert('ONE' in var_d)
                        assert(var_d['ONE'] == 'plain-string-value')
                        assert('TWO' in var_d)
                        assert(var_d['TWO'] == '${INTERP_ON_BUILD}')

                        # Ensure we have scripts verbatim
                        assert('before_script' in ci_obj)
                        before_script = ci_obj['before_script']
                        assert(before_script[0] == 'mkdir /some/path')
                        assert(before_script[1] == 'pushd /some/path')
                        assert(before_script[2] == 'git clone ${SPACK_REPO}')
                        assert(before_script[3] == 'cd spack')
                        assert(before_script[4] == 'git checkout ${SPACK_REF}')
                        assert(before_script[5] == 'popd')

                        assert('script' in ci_obj)
                        assert(ci_obj['script'][0] == 'spack -d ci rebuild')

                        assert('after_script' in ci_obj)
                        after_script = ci_obj['after_script'][0]
                        assert(after_script == 'rm -rf /some/path/spack')

                        found_it = True

            assert(found_it)


def test_ci_generate_pkg_with_deps(tmpdir, mutable_mock_env_path,
                                   env_deactivate, install_mockery,
                                   mock_packages):
    """Test pipeline generation for a package w/ dependencies"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - flatten-deps
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    enable-artifacts-buildcache: True
    mappings:
      - match:
          - flatten-deps
        runner-attributes:
          tags:
            - donotcare
      - match:
          - dependency-install
        runner-attributes:
          tags:
            - donotcare
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            print('generated contents: ')
            print(contents)
            yaml_contents = syaml.load(contents)
            found = []
            for ci_key in yaml_contents.keys():
                ci_obj = yaml_contents[ci_key]
                if 'dependency-install' in ci_key:
                    assert('stage' in ci_obj)
                    assert(ci_obj['stage'] == 'stage-0')
                    found.append('dependency-install')
                if 'flatten-deps' in ci_key:
                    assert('stage' in ci_obj)
                    assert(ci_obj['stage'] == 'stage-1')
                    found.append('flatten-deps')

            assert('flatten-deps' in found)
            assert('dependency-install' in found)


def test_ci_generate_for_pr_pipeline(tmpdir, mutable_mock_env_path,
                                     env_deactivate, install_mockery,
                                     mock_packages, monkeypatch):
    """Test that PR pipelines do not include a final stage job for
    rebuilding the mirror index, even if that job is specifically
    configured"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - flatten-deps
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    enable-artifacts-buildcache: True
    mappings:
      - match:
          - flatten-deps
        runner-attributes:
          tags:
            - donotcare
      - match:
          - dependency-install
        runner-attributes:
          tags:
            - donotcare
    service-job-attributes:
      image: donotcare
      tags: [donotcare]
    rebuild-index: False
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            os.environ['SPACK_IS_PR_PIPELINE'] = 'True'
            os.environ['SPACK_PR_BRANCH'] = 'fake-test-branch'
            monkeypatch.setattr(
                ci, 'SPACK_PR_MIRRORS_ROOT_URL', r"file:///fake/mirror")
            try:
                ci_cmd('generate', '--output-file', outputfile)
            finally:
                del os.environ['SPACK_IS_PR_PIPELINE']
                del os.environ['SPACK_PR_BRANCH']

        with open(outputfile) as f:
            contents = f.read()
            print('generated contents: ')
            print(contents)
            yaml_contents = syaml.load(contents)

            assert('rebuild-index' not in yaml_contents)

            for ci_key in yaml_contents.keys():
                if ci_key.startswith('(specs) '):
                    job_object = yaml_contents[ci_key]
                    job_vars = job_object['variables']
                    assert('SPACK_IS_PR_PIPELINE' in job_vars)
                    assert(job_vars['SPACK_IS_PR_PIPELINE'] == 'True')


def test_ci_generate_with_external_pkg(tmpdir, mutable_mock_env_path,
                                       env_deactivate, install_mockery,
                                       mock_packages, monkeypatch):
    """Make sure we do not generate jobs for external pkgs"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
    - externaltest
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    mappings:
      - match:
          - archive-files
          - externaltest
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            monkeypatch.setattr(
                ci, 'SPACK_PR_MIRRORS_ROOT_URL', r"file:///fake/mirror")
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            yaml_contents = syaml.load(f)

        # Check that the "externaltool" package was not erroneously staged
        assert not any('externaltool' in key for key in yaml_contents)


def test_ci_rebuild_basic(tmpdir, mutable_mock_env_path, env_deactivate,
                          install_mockery, mock_packages,
                          mock_gnupghome):
    working_dir = tmpdir.join('working_dir')

    mirror_dir = working_dir.join('mirror')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    signing_key_dir = spack_paths.mock_gpg_keys_path
    signing_key_path = os.path.join(signing_key_dir, 'package-signing-key')
    with open(signing_key_path) as fd:
        signing_key = fd.read()

    spack_yaml_contents = """
spack:
 definitions:
   - packages: [archive-files]
 specs:
   - $packages
 mirrors:
   test-mirror: {0}
 gitlab-ci:
   enable-artifacts-buildcache: True
   mappings:
     - match:
         - archive-files
       runner-attributes:
         tags:
           - donotcare
         image: donotcare
 cdash:
   build-group: Not important
   url: https://my.fake.cdash
   project: Not used
   site: Nothing
""".format(mirror_url)

    print('spack.yaml:\n{0}\n'.format(spack_yaml_contents))

    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        with ev.read('test'):
            root_spec = ('eJyNjsGOwyAMRO/5Ct96alRFFK34ldUqcohJ6BJAQFHUry9Nk66'
                         'UXNY3v5mxJ3qSojoDBjnqTGelDUVRQZlMIWpnBZya+nJa0Mv1Fg'
                         'G8waRcmAQkimkHWxcF9NRptHyVEoaBkoD5i7ecLVC6yZd/YTtpc'
                         'SIBg5Tr/mnA6mt9qTZL9CiLr7trk7StJyd/F81jKGoqoe2gVAaH'
                         '0uT7ZwPeH9A875HaA9MfidHdHxgxjgJuTGVtIrvfHGtynjkGyzi'
                         'xRrkHy94t1lftvv1n4AkVK3kQ')

            # Create environment variables as gitlab would do it
            set_env_var('CI_PROJECT_DIR', working_dir.strpath)
            set_env_var('SPACK_SIGNING_KEY', signing_key)
            set_env_var('SPACK_ROOT_SPEC', root_spec)
            set_env_var('SPACK_JOB_SPEC_PKG_NAME', 'archive-files')
            set_env_var('SPACK_COMPILER_ACTION', 'NONE')
            set_env_var('SPACK_CDASH_BUILD_NAME', '(specs) archive-files')
            set_env_var('SPACK_RELATED_BUILDS_CDASH', '')

            rebuild_output = ci_cmd(
                'rebuild', fail_on_error=False, output=str)

            print(rebuild_output)


@pytest.mark.disable_clean_stage_check
@pytest.mark.skipif(not spack.util.gpg.has_gpg(),
                    reason='This test requires gpg')
def test_push_mirror_contents(tmpdir, mutable_mock_env_path, env_deactivate,
                              install_mockery, mock_packages, mock_fetch,
                              mock_stage, mock_gnupghome):
    working_dir = tmpdir.join('working_dir')

    mirror_dir = working_dir.join('mirror')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    signing_key_dir = spack_paths.mock_gpg_keys_path
    signing_key_path = os.path.join(signing_key_dir, 'package-signing-key')
    with open(signing_key_path) as fd:
        signing_key = fd.read()

    ci.import_signing_key(signing_key)

    spack_yaml_contents = """
spack:
 definitions:
   - packages: [patchelf]
 specs:
   - $packages
 mirrors:
   test-mirror: {0}
 gitlab-ci:
   enable-artifacts-buildcache: True
   mappings:
     - match:
         - patchelf
       runner-attributes:
         tags:
           - donotcare
         image: donotcare
   service-job-attributes:
     tags:
       - nonbuildtag
     image: basicimage
""".format(mirror_url)

    print('spack.yaml:\n{0}\n'.format(spack_yaml_contents))

    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        with ev.read('test') as env:
            spec_map = ci.get_concrete_specs(
                'patchelf', 'patchelf', '', 'FIND_ANY')
            concrete_spec = spec_map['patchelf']
            spec_yaml = concrete_spec.to_yaml(hash=ht.build_hash)
            yaml_path = str(tmpdir.join('spec.yaml'))
            with open(yaml_path, 'w') as ypfd:
                ypfd.write(spec_yaml)

            install_cmd('--keep-stage', yaml_path)

            # env, spec, yaml_path, mirror_url, build_id, sign_binaries
            ci.push_mirror_contents(
                env, concrete_spec, yaml_path, mirror_url, '42', True)

            buildcache_path = os.path.join(mirror_dir.strpath, 'build_cache')

            # Now test the --prune-dag (default) option of spack ci generate
            mirror_cmd('add', 'test-ci', mirror_url)

            outputfile_pruned = str(tmpdir.join('pruned_pipeline.yml'))
            ci_cmd('generate', '--output-file', outputfile_pruned)

            with open(outputfile_pruned) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)
                assert('no-specs-to-rebuild' in yaml_contents)
                # Make sure there are no other spec jobs or rebuild-index
                assert(len(yaml_contents.keys()) == 1)
                the_elt = yaml_contents['no-specs-to-rebuild']
                assert('tags' in the_elt)
                assert('nonbuildtag' in the_elt['tags'])
                assert('image' in the_elt)
                assert(the_elt['image'] == 'basicimage')

            outputfile_not_pruned = str(tmpdir.join('unpruned_pipeline.yml'))
            ci_cmd('generate', '--no-prune-dag', '--output-file',
                   outputfile_not_pruned)

            # Test the --no-prune-dag option of spack ci generate
            with open(outputfile_not_pruned) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)

                found_spec_job = False

                for ci_key in yaml_contents.keys():
                    if '(specs) patchelf' in ci_key:
                        the_elt = yaml_contents[ci_key]
                        assert('variables' in the_elt)
                        job_vars = the_elt['variables']
                        assert('SPACK_SPEC_NEEDS_REBUILD' in job_vars)
                        assert(job_vars['SPACK_SPEC_NEEDS_REBUILD'] == 'False')
                        found_spec_job = True

                assert(found_spec_job)

            mirror_cmd('rm', 'test-ci')

            # Test generating buildcache index while we have bin mirror
            buildcache_cmd('update-index', '--mirror-url', mirror_url)
            index_path = os.path.join(buildcache_path, 'index.json')
            with open(index_path) as idx_fd:
                index_object = json.load(idx_fd)
                validate(index_object, db_idx_schema)

            # Now that index is regenerated, validate "buildcache list" output
            buildcache_list_output = buildcache_cmd('list', output=str)
            assert('patchelf' in buildcache_list_output)

            # Also test buildcache_spec schema
            bc_files_list = os.listdir(buildcache_path)
            for file_name in bc_files_list:
                if file_name.endswith('.spec.yaml'):
                    spec_yaml_path = os.path.join(buildcache_path, file_name)
                    with open(spec_yaml_path) as yaml_fd:
                        yaml_object = syaml.load(yaml_fd)
                        validate(yaml_object, spec_yaml_schema)

            logs_dir = working_dir.join('logs_dir')
            if not os.path.exists(logs_dir.strpath):
                os.makedirs(logs_dir.strpath)

            ci.copy_stage_logs_to_artifacts(concrete_spec, logs_dir.strpath)

            logs_dir_list = os.listdir(logs_dir.strpath)

            assert('spack-build-out.txt' in logs_dir_list)

            # Also just make sure that if something goes wrong with the
            # stage logs copy, no exception is thrown
            ci.copy_stage_logs_to_artifacts(None, logs_dir.strpath)

            dl_dir = working_dir.join('download_dir')
            if not os.path.exists(dl_dir.strpath):
                os.makedirs(dl_dir.strpath)

            buildcache_cmd('download', '--spec-yaml', yaml_path, '--path',
                           dl_dir.strpath, '--require-cdashid')

            dl_dir_list = os.listdir(dl_dir.strpath)

            assert(len(dl_dir_list) == 3)


def test_push_mirror_contents_exceptions(monkeypatch, capsys):
    def faked(env, spec_yaml=None, packages=None, add_spec=True,
              add_deps=True, output_location=os.getcwd(),
              signing_key=None, force=False, make_relative=False,
              unsigned=False, allow_root=False, rebuild_index=False):
        raise Exception('Error: Access Denied')

    import spack.cmd.buildcache as buildcache
    monkeypatch.setattr(buildcache, '_createtarball', faked)

    url = 'fakejunk'
    ci.push_mirror_contents(None, None, None, url, None, None)

    captured = capsys.readouterr()
    std_out = captured[0]
    expect_msg = 'Permission problem writing to {0}'.format(url)

    assert(expect_msg in std_out)


def test_ci_generate_override_runner_attrs(tmpdir, mutable_mock_env_path,
                                           env_deactivate, install_mockery,
                                           mock_packages, monkeypatch):
    """Test that we get the behavior we want with respect to the provision
       of runner attributes like tags, variables, and scripts, both when we
       inherit them from the top level, as well as when we override one or
       more at the runner level"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - flatten-deps
    - a
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    tags:
      - toplevel
    variables:
      ONE: toplevelvarone
      TWO: toplevelvartwo
    before_script:
      - pre step one
      - pre step two
    script:
      - main step
    after_script:
      - post step one
    mappings:
      - match:
          - flatten-deps
        runner-attributes:
          tags:
            - specific-one
          variables:
            THREE: specificvarthree
      - match:
          - dependency-install
      - match:
          - a
        runner-attributes:
          tags:
            - specific-a
            - toplevel
          variables:
            ONE: specificvarone
            TWO: specificvartwo
          before_script:
            - custom pre step one
          script:
            - custom main step
          after_script:
            - custom post step one
    service-job-attributes:
      image: donotcare
      tags: [donotcare]
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            monkeypatch.setattr(
                spack.main, 'get_version', lambda: '0.15.3-416-12ad69eb1')
            monkeypatch.setattr(
                ci, 'SPACK_PR_MIRRORS_ROOT_URL', r"file:///fake/mirror")
            ci_cmd('generate', '--output-file', outputfile)

        with open(outputfile) as f:
            contents = f.read()
            print('generated contents: ')
            print(contents)
            yaml_contents = syaml.load(contents)

            assert('variables' in yaml_contents)
            global_vars = yaml_contents['variables']
            assert('SPACK_VERSION' in global_vars)
            assert(global_vars['SPACK_VERSION'] == '0.15.3-416-12ad69eb1')
            assert('SPACK_CHECKOUT_VERSION' in global_vars)
            assert(global_vars['SPACK_CHECKOUT_VERSION'] == '12ad69eb1')

            for ci_key in yaml_contents.keys():
                if '(specs) b' in ci_key:
                    print('Should not have staged "b" w/out a match')
                    assert(False)
                if '(specs) a' in ci_key:
                    # Make sure a's attributes override variables, and all the
                    # scripts.  Also, make sure the 'toplevel' tag doesn't
                    # appear twice, but that a's specific extra tag does appear
                    the_elt = yaml_contents[ci_key]
                    assert(the_elt['variables']['ONE'] == 'specificvarone')
                    assert(the_elt['variables']['TWO'] == 'specificvartwo')
                    assert('THREE' not in the_elt['variables'])
                    assert(len(the_elt['tags']) == 2)
                    assert('specific-a' in the_elt['tags'])
                    assert('toplevel' in the_elt['tags'])
                    assert(len(the_elt['before_script']) == 1)
                    assert(the_elt['before_script'][0] ==
                           'custom pre step one')
                    assert(len(the_elt['script']) == 1)
                    assert(the_elt['script'][0] == 'custom main step')
                    assert(len(the_elt['after_script']) == 1)
                    assert(the_elt['after_script'][0] ==
                           'custom post step one')
                if '(specs) dependency-install' in ci_key:
                    # Since the dependency-install match omits any
                    # runner-attributes, make sure it inherited all the
                    # top-level attributes.
                    the_elt = yaml_contents[ci_key]
                    assert(the_elt['variables']['ONE'] == 'toplevelvarone')
                    assert(the_elt['variables']['TWO'] == 'toplevelvartwo')
                    assert('THREE' not in the_elt['variables'])
                    assert(len(the_elt['tags']) == 1)
                    assert(the_elt['tags'][0] == 'toplevel')
                    assert(len(the_elt['before_script']) == 2)
                    assert(the_elt['before_script'][0] == 'pre step one')
                    assert(the_elt['before_script'][1] == 'pre step two')
                    assert(len(the_elt['script']) == 1)
                    assert(the_elt['script'][0] == 'main step')
                    assert(len(the_elt['after_script']) == 1)
                    assert(the_elt['after_script'][0] == 'post step one')
                if '(specs) flatten-deps' in ci_key:
                    # The flatten-deps match specifies that we keep the two
                    # top level variables, but add a third specifc one.  It
                    # also adds a custom tag which should be combined with
                    # the top-level tag.
                    the_elt = yaml_contents[ci_key]
                    assert(the_elt['variables']['ONE'] == 'toplevelvarone')
                    assert(the_elt['variables']['TWO'] == 'toplevelvartwo')
                    assert(the_elt['variables']['THREE'] == 'specificvarthree')
                    assert(len(the_elt['tags']) == 2)
                    assert('specific-one' in the_elt['tags'])
                    assert('toplevel' in the_elt['tags'])
                    assert(len(the_elt['before_script']) == 2)
                    assert(the_elt['before_script'][0] == 'pre step one')
                    assert(the_elt['before_script'][1] == 'pre step two')
                    assert(len(the_elt['script']) == 1)
                    assert(the_elt['script'][0] == 'main step')
                    assert(len(the_elt['after_script']) == 1)
                    assert(the_elt['after_script'][0] == 'post step one')


def test_ci_generate_with_workarounds(tmpdir, mutable_mock_env_path,
                                      env_deactivate, install_mockery,
                                      mock_packages, monkeypatch):
    """Make sure the post-processing cli workarounds do what they should"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - callpath%gcc@3.0
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    mappings:
      - match: ['%gcc@3.0']
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
    enable-artifacts-buildcache: true
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            monkeypatch.setattr(
                ci, 'SPACK_PR_MIRRORS_ROOT_URL', r"file:///fake/mirror")
            ci_cmd('generate', '--output-file', outputfile, '--dependencies')

            with open(outputfile) as f:
                contents = f.read()
                yaml_contents = syaml.load(contents)

                found_one = False

                for ci_key in yaml_contents.keys():
                    if ci_key.startswith('(specs) '):
                        found_one = True
                        job_obj = yaml_contents[ci_key]
                        assert('needs' not in job_obj)
                        assert('dependencies' in job_obj)

                assert(found_one is True)


@pytest.mark.disable_clean_stage_check
def test_ci_rebuild_index(tmpdir, mutable_mock_env_path, env_deactivate,
                          install_mockery, mock_packages, mock_fetch,
                          mock_stage):
    working_dir = tmpdir.join('working_dir')

    mirror_dir = working_dir.join('mirror')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    spack_yaml_contents = """
spack:
 specs:
   - callpath
 mirrors:
   test-mirror: {0}
 gitlab-ci:
   mappings:
     - match:
         - patchelf
       runner-attributes:
         tags:
           - donotcare
         image: donotcare
""".format(mirror_url)

    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write(spack_yaml_contents)

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        with ev.read('test'):
            spec_map = ci.get_concrete_specs(
                'callpath', 'callpath', '', 'FIND_ANY')
            concrete_spec = spec_map['callpath']
            spec_yaml = concrete_spec.to_yaml(hash=ht.build_hash)
            yaml_path = str(tmpdir.join('spec.yaml'))
            with open(yaml_path, 'w') as ypfd:
                ypfd.write(spec_yaml)

            install_cmd('--keep-stage', '-f', yaml_path)
            buildcache_cmd('create', '-u', '-a', '-f', '--mirror-url',
                           mirror_url, 'callpath')
            ci_cmd('rebuild-index')

            buildcache_path = os.path.join(mirror_dir.strpath, 'build_cache')
            index_path = os.path.join(buildcache_path, 'index.json')
            with open(index_path) as idx_fd:
                index_object = json.load(idx_fd)
                validate(index_object, db_idx_schema)


def test_ci_generate_bootstrap_prune_dag(
        install_mockery_mutable_config, mock_packages, mock_fetch,
        mock_archive, mutable_config, monkeypatch, tmpdir,
        mutable_mock_env_path, env_deactivate):
    """Test compiler bootstrapping with DAG pruning.  Specifically, make
       sure that if we detect the bootstrapped compiler needs to be rebuilt,
       we ensure the spec we want to build with that compiler is scheduled
       for rebuild as well."""

    # Create a temp mirror directory for buildcache usage
    mirror_dir = tmpdir.join('mirror_dir')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    # Install a compiler, because we want to put it in a buildcache
    install_cmd('gcc@10.1.0%gcc@4.5.0')

    # Put installed compiler in the buildcache
    buildcache_cmd('create', '-u', '-a', '-f', '-d', mirror_dir.strpath,
                   'gcc@10.1.0%gcc@4.5.0')

    # Now uninstall the compiler
    uninstall_cmd('-y', 'gcc@10.1.0%gcc@4.5.0')

    monkeypatch.setattr(spack.concretize.Concretizer,
                        'check_for_compiler_existence', False)
    spack.config.set('config:install_missing_compilers', True)
    assert CompilerSpec('gcc@10.1.0') not in compilers.all_compiler_specs()

    # Configure the mirror where we put that buildcache w/ the compiler
    mirror_cmd('add', 'test-mirror', mirror_url)

    install_cmd('--no-check-signature', 'a%gcc@10.1.0')

    # Put spec built with installed compiler in the buildcache
    buildcache_cmd('create', '-u', '-a', '-f', '-d', mirror_dir.strpath,
                   'a%gcc@10.1.0')

    # Now uninstall the spec
    uninstall_cmd('-y', 'a%gcc@10.1.0')

    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  definitions:
    - bootstrap:
      - gcc@10.1.0%gcc@4.5.0
  specs:
    - a%gcc@10.1.0
  mirrors:
    atestm: {0}
  gitlab-ci:
    bootstrap:
      - name: bootstrap
        compiler-agnostic: true
    mappings:
      - match:
          - arch=test-debian6-x86_64
        runner-attributes:
          tags:
            - donotcare
      - match:
          - arch=test-debian6-core2
        runner-attributes:
          tags:
            - meh
""".format(mirror_url))

    # Without this monkeypatch, pipeline generation process would think that
    # nothing in the environment needs rebuilding.  With the monkeypatch, the
    # process sees the compiler as needing a rebuild, which should then result
    # in the specs built with that compiler needing a rebuild too.
    def fake_get_mirrors_for_spec(spec=None, full_hash_match=False,
                                  mirrors_to_check=None, index_only=False):
        if spec.name == 'gcc':
            return []
        else:
            return [{
                'spec': spec,
                'mirror_url': mirror_url,
            }]

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            monkeypatch.setattr(
                ci, 'SPACK_PR_MIRRORS_ROOT_URL', r"file:///fake/mirror")

            ci_cmd('generate', '--output-file', outputfile)

            with open(outputfile) as of:
                yaml_contents = of.read()
                original_yaml_contents = syaml.load(yaml_contents)

            # without the monkeypatch, everything appears up to date and no
            # rebuild jobs are generated.
            assert(original_yaml_contents)
            assert('no-specs-to-rebuild' in original_yaml_contents)

            monkeypatch.setattr(spack.binary_distribution,
                                'get_mirrors_for_spec',
                                fake_get_mirrors_for_spec)

            ci_cmd('generate', '--output-file', outputfile)

            with open(outputfile) as of:
                yaml_contents = of.read()
                new_yaml_contents = syaml.load(yaml_contents)

            assert(new_yaml_contents)

            # This 'needs' graph reflects that even though specs 'a' and 'b' do
            # not otherwise need to be rebuilt (thanks to DAG pruning), they
            # both end up in the generated pipeline because the compiler they
            # depend on is bootstrapped, and *does* need to be rebuilt.
            needs_graph = {
                '(bootstrap) gcc': [],
                '(specs) b': [
                    '(bootstrap) gcc',
                ],
                '(specs) a': [
                    '(bootstrap) gcc',
                    '(specs) b',
                ],
            }

            _validate_needs_graph(new_yaml_contents, needs_graph, False)


def test_ci_subcommands_without_mirror(tmpdir, mutable_mock_env_path,
                                       env_deactivate, mock_packages,
                                       install_mockery):
    """Make sure we catch if there is not a mirror and report an error"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
  gitlab-ci:
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        with ev.read('test'):
            # Check the 'generate' subcommand
            output = ci_cmd('generate', '--output-file', outputfile,
                            output=str, fail_on_error=False)
            ex = 'spack ci generate requires an env containing a mirror'
            assert(ex in output)

            # Also check the 'rebuild-index' subcommand
            output = ci_cmd('rebuild-index', output=str, fail_on_error=False)
            ex = 'spack ci rebuild-index requires an env containing a mirror'
            assert(ex in output)


def test_ensure_only_one_temporary_storage():
    """Make sure 'gitlab-ci' section of env does not allow specification of
    both 'enable-artifacts-buildcache' and 'temporary-storage-url-prefix'."""
    gitlab_ci_template = """
  gitlab-ci:
    {0}
    mappings:
      - match:
          - notcheckedhere
        runner-attributes:
          tags:
            - donotcare
"""

    enable_artifacts = 'enable-artifacts-buildcache: True'
    temp_storage = 'temporary-storage-url-prefix: file:///temp/mirror'
    specify_both = """{0}
    {1}
""".format(enable_artifacts, temp_storage)
    specify_neither = ''

    # User can specify "enable-artifacts-buildcache" (boolean)
    yaml_obj = syaml.load(gitlab_ci_template.format(enable_artifacts))
    validate(yaml_obj, gitlab_ci_schema)

    # User can also specify "temporary-storage-url-prefix" (string)
    yaml_obj = syaml.load(gitlab_ci_template.format(temp_storage))
    validate(yaml_obj, gitlab_ci_schema)

    # However, specifying both should fail to validate
    yaml_obj = syaml.load(gitlab_ci_template.format(specify_both))
    with pytest.raises(ValidationError):
        validate(yaml_obj, gitlab_ci_schema)

    # Specifying neither should be fine too, as neither of these properties
    # should be required
    yaml_obj = syaml.load(gitlab_ci_template.format(specify_neither))
    validate(yaml_obj, gitlab_ci_schema)


def test_ci_generate_temp_storage_url(tmpdir, mutable_mock_env_path,
                                      env_deactivate, install_mockery,
                                      mock_packages, monkeypatch):
    """Verify correct behavior when using temporary-storage-url-prefix"""
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - archive-files
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    temporary-storage-url-prefix: file:///work/temp/mirror
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
""")

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        outputfile = str(tmpdir.join('.gitlab-ci.yml'))

        monkeypatch.setattr(
            ci, 'SPACK_PR_MIRRORS_ROOT_URL', r"file:///fake/mirror")

        with ev.read('test'):
            ci_cmd('generate', '--output-file', outputfile)

            with open(outputfile) as of:
                pipeline_doc = syaml.load(of.read())

                print(pipeline_doc)

                assert('cleanup' in pipeline_doc)
                cleanup_job = pipeline_doc['cleanup']

                assert('script' in cleanup_job)
                cleanup_task = cleanup_job['script'][0]

                assert(cleanup_task.startswith('spack -d mirror destroy'))

                assert('stages' in pipeline_doc)
                stages = pipeline_doc['stages']

                # Cleanup job should be 2nd to last, just before rebuild-index
                assert('stage' in cleanup_job)
                assert(cleanup_job['stage'] == stages[-2])


def test_ci_generate_read_broken_specs_url(tmpdir, mutable_mock_env_path,
                                           env_deactivate, install_mockery,
                                           mock_packages, monkeypatch):
    """Verify that `broken-specs-url` works as intended"""
    spec_a = Spec('a')
    spec_a.concretize()
    a_full_hash = spec_a.full_hash()

    spec_flattendeps = Spec('flatten-deps')
    spec_flattendeps.concretize()
    flattendeps_full_hash = spec_flattendeps.full_hash()

    # Mark 'a' as broken (but not 'flatten-deps')
    broken_spec_a_path = str(tmpdir.join(a_full_hash))
    with open(broken_spec_a_path, 'w') as bsf:
        bsf.write('')

    # Test that `spack ci generate` notices this broken spec and fails.
    filename = str(tmpdir.join('spack.yaml'))
    with open(filename, 'w') as f:
        f.write("""\
spack:
  specs:
    - flatten-deps
    - a
  mirrors:
    some-mirror: https://my.fake.mirror
  gitlab-ci:
    broken-specs-url: "{0}"
    mappings:
      - match:
          - archive-files
        runner-attributes:
          tags:
            - donotcare
          image: donotcare
""".format(tmpdir.strpath))

    with tmpdir.as_cwd():
        env_cmd('create', 'test', './spack.yaml')
        with ev.read('test'):
            # Check output of the 'generate' subcommand
            output = ci_cmd('generate', output=str, fail_on_error=False)
            assert('known to be broken' in output)

            ex = '({0})'.format(a_full_hash)
            assert(ex in output)

            ex = '({0})'.format(flattendeps_full_hash)
            assert(ex not in output)
