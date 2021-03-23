# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import pytest
from six.moves.urllib.error import URLError

import spack.ci as ci
import spack.main as spack_main
import spack.config as cfg
import spack.paths as spack_paths
import spack.spec as spec
import spack.util.web as web_util
import spack.util.gpg

import spack.ci_optimization as ci_opt
import spack.ci_needs_workaround as cinw
import spack.util.spack_yaml as syaml
import itertools as it
import collections
try:
    # dynamically import to keep vermin from complaining
    collections_abc = __import__('collections.abc')
except ImportError:
    collections_abc = collections


@pytest.fixture
def tmp_scope():
    """Creates a temporary configuration scope"""
    base_name = 'internal-testing-scope'
    current_overrides = set(
        x.name for x in
        cfg.config.matching_scopes(r'^{0}'.format(base_name)))

    num_overrides = 0
    scope_name = base_name
    while scope_name in current_overrides:
        scope_name = '{0}{1}'.format(base_name, num_overrides)
        num_overrides += 1

    with cfg.override(cfg.InternalConfigScope(scope_name)):
        yield scope_name


def test_urlencode_string():
    s = 'Spack Test Project'

    s_enc = ci.url_encode_string(s)

    assert(s_enc == 'Spack+Test+Project')


@pytest.mark.skipif(not spack.util.gpg.has_gpg(),
                    reason='This test requires gpg')
def test_import_signing_key(mock_gnupghome):
    signing_key_dir = spack_paths.mock_gpg_keys_path
    signing_key_path = os.path.join(signing_key_dir, 'package-signing-key')
    with open(signing_key_path) as fd:
        signing_key = fd.read()

    # Just make sure this does not raise any exceptions
    ci.import_signing_key(signing_key)


def test_configure_compilers(mutable_config):

    def assert_missing(config):
        assert('install_missing_compilers' not in config or
               config['install_missing_compilers'] is False)

    def assert_present(config):
        assert('install_missing_compilers' in config and
               config['install_missing_compilers'] is True)

    original_config = cfg.get('config')
    assert_missing(original_config)

    ci.configure_compilers('FIND_ANY', scope='site')

    second_config = cfg.get('config')
    assert_missing(second_config)

    ci.configure_compilers('INSTALL_MISSING')
    last_config = cfg.get('config')
    assert_present(last_config)


def test_get_concrete_specs(config, mock_packages):
    root_spec = (
        'eJztkk1uwyAQhfc5BbuuYjWObSKuUlURYP5aDBjjBPv0RU7iRI6qpKuqUtnxzZvRwHud'
        'YxSt1oCMyuVoBdI5MN8paxDYZK/ZbkLYU3kqAuA0Dtz6BgGtTB8XdG87BCgzwXbwXArY'
        'CxYQiLtqXxUTpLZxSjN/mWlwwxAQlJ7v8wpFtsvK1UXSOUyTjvRKB2Um7LBPhZD0l1md'
        'xJ7VCATfszOiXGOR9np7vwDn7lCMS8SXQNf3RCtyBTVzzNTMUMXmfWrFeR+UngEAEncS'
        'ASjKwZcid7ERNldthBxjX46mMD2PsJnlYXDs2rye3l+vroOkJJ54SXgZPklLRQmx61sm'
        'cgKNVFRO0qlpf2pojq1Ro7OG56MY+Bgc1PkIo/WkaT8OVcrDYuvZkJdtBl/+XCZ+NQBJ'
        'oKg1h6X/VdXRoyE2OWeH6lCXZdHGrauUZAWFw/YJ/0/39OefN3F4Kle3cXjYsF684ZqG'
        'Tbap/uPwbRx+YPStIQ8bvgA7G6YE'
    )

    dep_builds = 'diffutils;libiconv'
    spec_map = ci.get_concrete_specs(root_spec, 'bzip2', dep_builds, 'NONE')

    assert('root' in spec_map and 'deps' in spec_map)

    nonconc_root_spec = 'archive-files'
    dep_builds = ''
    spec_map = ci.get_concrete_specs(
        nonconc_root_spec, 'archive-files', dep_builds, 'FIND_ANY')

    assert('root' in spec_map and 'deps' in spec_map)
    assert('archive-files' in spec_map)


@pytest.mark.maybeslow
def test_register_cdash_build():
    build_name = 'Some pkg'
    base_url = 'http://cdash.fake.org'
    project = 'spack'
    site = 'spacktests'
    track = 'Experimental'

    with pytest.raises(URLError):
        ci.register_cdash_build(build_name, base_url, project, site, track)


def test_relate_cdash_builds(config, mock_packages):
    root_spec = (
        'eJztkk1uwyAQhfc5BbuuYjWObSKuUlURYP5aDBjjBPv0RU7iRI6qpKuqUtnxzZvRwHud'
        'YxSt1oCMyuVoBdI5MN8paxDYZK/ZbkLYU3kqAuA0Dtz6BgGtTB8XdG87BCgzwXbwXArY'
        'CxYQiLtqXxUTpLZxSjN/mWlwwxAQlJ7v8wpFtsvK1UXSOUyTjvRKB2Um7LBPhZD0l1md'
        'xJ7VCATfszOiXGOR9np7vwDn7lCMS8SXQNf3RCtyBTVzzNTMUMXmfWrFeR+UngEAEncS'
        'ASjKwZcid7ERNldthBxjX46mMD2PsJnlYXDs2rye3l+vroOkJJ54SXgZPklLRQmx61sm'
        'cgKNVFRO0qlpf2pojq1Ro7OG56MY+Bgc1PkIo/WkaT8OVcrDYuvZkJdtBl/+XCZ+NQBJ'
        'oKg1h6X/VdXRoyE2OWeH6lCXZdHGrauUZAWFw/YJ/0/39OefN3F4Kle3cXjYsF684ZqG'
        'Tbap/uPwbRx+YPStIQ8bvgA7G6YE'
    )

    dep_builds = 'diffutils;libiconv'
    spec_map = ci.get_concrete_specs(root_spec, 'bzip2', dep_builds, 'NONE')
    cdash_api_url = 'http://cdash.fake.org'
    job_build_id = '42'
    cdash_project = 'spack'
    cdashids_mirror_url = 'https://my.fake.mirror'

    with pytest.raises(web_util.SpackWebError):
        ci.relate_cdash_builds(spec_map, cdash_api_url, job_build_id,
                               cdash_project, cdashids_mirror_url)

    # Just make sure passing None for build id doesn't throw exceptions
    ci.relate_cdash_builds(spec_map, cdash_api_url, None, cdash_project,
                           cdashids_mirror_url)


def test_read_write_cdash_ids(config, tmp_scope, tmpdir, mock_packages):
    working_dir = tmpdir.join('working_dir')
    mirror_dir = working_dir.join('mirror')
    mirror_url = 'file://{0}'.format(mirror_dir.strpath)

    mirror_cmd = spack_main.SpackCommand('mirror')
    mirror_cmd('add', '--scope', tmp_scope, 'test_mirror', mirror_url)

    mock_spec = spec.Spec('archive-files').concretized()
    orig_cdashid = '42'

    ci.write_cdashid_to_mirror(orig_cdashid, mock_spec, mirror_url)

    # Now read it back
    read_cdashid = ci.read_cdashid_from_mirror(mock_spec, mirror_url)

    assert(str(read_cdashid) == orig_cdashid)


def test_ci_workarounds():
    fake_root_spec = 'x' * 544
    fake_spack_ref = 'x' * 40

    common_variables = {
        'SPACK_COMPILER_ACTION': 'NONE',
        'SPACK_IS_PR_PIPELINE': 'False',
    }

    common_before_script = [
        'git clone "https://github.com/spack/spack"',
        ' && '.join((
            'pushd ./spack',
            'git checkout "{ref}"'.format(ref=fake_spack_ref),
            'popd')),
        '. "./spack/share/spack/setup-env.sh"'
    ]

    def make_build_job(name, deps, stage, use_artifact_buildcache, optimize,
                       use_dependencies):
        variables = common_variables.copy()
        variables['SPACK_JOB_SPEC_PKG_NAME'] = name

        result = {
            'stage': stage,
            'tags': ['tag-0', 'tag-1'],
            'artifacts': {
                'paths': [
                    'jobs_scratch_dir',
                    'cdash_report',
                    name + '.spec.yaml',
                    name + '.cdashid',
                    name
                ],
                'when': 'always'
            },
            'retry': {'max': 2, 'when': ['always']},
            'after_script': ['rm -rf "./spack"'],
            'script': ['spack ci rebuild'],
            'image': {'name': 'spack/centos7', 'entrypoint': ['']}
        }

        if optimize:
            result['extends'] = ['.c0', '.c1']
        else:
            variables['SPACK_ROOT_SPEC'] = fake_root_spec
            result['before_script'] = common_before_script

        result['variables'] = variables

        if use_dependencies:
            result['dependencies'] = (
                list(deps) if use_artifact_buildcache
                else [])
        else:
            result['needs'] = [
                {'job': dep, 'artifacts': use_artifact_buildcache}
                for dep in deps]

        return {name: result}

    def make_rebuild_index_job(
            use_artifact_buildcache, optimize, use_dependencies):

        result = {
            'stage': 'stage-rebuild-index',
            'script': 'spack buildcache update-index -d s3://mirror',
            'tags': ['tag-0', 'tag-1'],
            'image': {'name': 'spack/centos7', 'entrypoint': ['']},
            'after_script': ['rm -rf "./spack"'],
        }

        if optimize:
            result['extends'] = '.c0'
        else:
            result['before_script'] = common_before_script

        return {'rebuild-index': result}

    def make_factored_jobs(optimize):
        return {
            '.c0': {'before_script': common_before_script},
            '.c1': {'variables': {'SPACK_ROOT_SPEC': fake_root_spec}}
        } if optimize else {}

    def make_stage_list(num_build_stages):
        return {
            'stages': (
                ['-'.join(('stage', str(i))) for i in range(num_build_stages)]
                + ['stage-rebuild-index'])}

    def make_yaml_obj(use_artifact_buildcache, optimize, use_dependencies):
        result = {}

        result.update(make_build_job(
            'pkg-a', [], 'stage-0', use_artifact_buildcache, optimize,
            use_dependencies))

        result.update(make_build_job(
            'pkg-b', ['pkg-a'], 'stage-1', use_artifact_buildcache, optimize,
            use_dependencies))

        result.update(make_build_job(
            'pkg-c', ['pkg-a', 'pkg-b'], 'stage-2', use_artifact_buildcache,
            optimize, use_dependencies))

        result.update(make_rebuild_index_job(
            use_artifact_buildcache, optimize, use_dependencies))

        result.update(make_factored_jobs(optimize))

        result.update(make_stage_list(3))

        return result

    # test every combination of:
    #     use artifact buildcache: true or false
    #     run optimization pass: true or false
    #     convert needs to dependencies: true or false
    for use_ab in (False, True):
        original = make_yaml_obj(
            use_artifact_buildcache=use_ab,
            optimize=False,
            use_dependencies=False)

        for opt, deps in it.product(*(((False, True),) * 2)):
            # neither optimizing nor converting needs->dependencies
            if not (opt or deps):
                # therefore, nothing to test
                continue

            predicted = make_yaml_obj(
                use_artifact_buildcache=use_ab,
                optimize=opt,
                use_dependencies=deps)

            actual = original.copy()
            if opt:
                actual = ci_opt.optimizer(actual)
            if deps:
                actual = cinw.needs_to_dependencies(actual)

            predicted = syaml.dump_config(
                ci_opt.sort_yaml_obj(predicted), default_flow_style=True)
            actual = syaml.dump_config(
                ci_opt.sort_yaml_obj(actual), default_flow_style=True)

            assert(predicted == actual)
