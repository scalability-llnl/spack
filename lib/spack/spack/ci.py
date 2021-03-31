# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import base64
import copy
import datetime
import json
import os
import re
import shutil
import stat
import tempfile
import zipfile

from six import iteritems
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.parse import urlencode
from six.moves.urllib.request import build_opener, HTTPHandler, Request

import llnl.util.tty as tty
import llnl.util.filesystem as fs

import spack
import spack.binary_distribution as bindist
import spack.cmd
import spack.compilers as compilers
import spack.config as cfg
import spack.environment as ev
from spack.error import SpackError
import spack.main
import spack.paths
import spack.repo
from spack.spec import Spec
import spack.util.executable as exe
import spack.util.spack_yaml as syaml
import spack.util.web as web_util
import spack.util.gpg as gpg_util
import spack.util.url as url_util


JOB_RETRY_CONDITIONS = [
    'always',
]

SPACK_PR_MIRRORS_ROOT_URL = 's3://spack-binaries-prs'
TEMP_STORAGE_MIRROR_NAME = 'ci_temporary_mirror'

spack_gpg = spack.main.SpackCommand('gpg')
spack_compiler = spack.main.SpackCommand('compiler')


class TemporaryDirectory(object):
    def __init__(self):
        self.temporary_directory = tempfile.mkdtemp()

    def __enter__(self):
        return self.temporary_directory

    def __exit__(self, exc_type, exc_value, exc_traceback):
        shutil.rmtree(self.temporary_directory)
        return False


def _create_buildgroup(opener, headers, url, project, group_name, group_type):
    data = {
        "newbuildgroup": group_name,
        "project": project,
        "type": group_type
    }

    enc_data = json.dumps(data).encode('utf-8')

    request = Request(url, data=enc_data, headers=headers)

    response = opener.open(request)
    response_code = response.getcode()

    if response_code != 200 and response_code != 201:
        msg = 'Creating buildgroup failed (response code = {0}'.format(
            response_code)
        raise SpackError(msg)

    response_text = response.read()
    response_json = json.loads(response_text)
    build_group_id = response_json['id']

    return build_group_id


def populate_buildgroup(job_names, group_name, project, site,
                        credentials, cdash_url):
    url = "{0}/api/v1/buildgroup.php".format(cdash_url)

    headers = {
        'Authorization': 'Bearer {0}'.format(credentials),
        'Content-Type': 'application/json',
    }

    opener = build_opener(HTTPHandler)

    parent_group_id = _create_buildgroup(
        opener, headers, url, project, group_name, 'Daily')
    group_id = _create_buildgroup(
        opener, headers, url, project, 'Latest {0}'.format(group_name),
        'Latest')

    if not parent_group_id or not group_id:
        msg = 'Failed to create or retrieve buildgroups for {0}'.format(
            group_name)
        raise SpackError(msg)

    data = {
        'project': project,
        'buildgroupid': group_id,
        'dynamiclist': [{
            'match': name,
            'parentgroupid': parent_group_id,
            'site': site
        } for name in job_names]
    }

    enc_data = json.dumps(data).encode('utf-8')

    request = Request(url, data=enc_data, headers=headers)
    request.get_method = lambda: 'PUT'

    response = opener.open(request)
    response_code = response.getcode()

    if response_code != 200:
        msg = 'Error response code ({0}) in populate_buildgroup'.format(
            response_code)
        raise SpackError(msg)


def is_main_phase(phase_name):
    return True if phase_name == 'specs' else False


def get_job_name(phase, strip_compiler, spec, osarch, build_group):
    item_idx = 0
    format_str = ''
    format_args = []

    if phase:
        format_str += '({{{0}}})'.format(item_idx)
        format_args.append(phase)
        item_idx += 1

    format_str += ' {{{0}}}'.format(item_idx)
    format_args.append(spec.name)
    item_idx += 1

    format_str += '/{{{0}}}'.format(item_idx)
    format_args.append(spec.dag_hash(7))
    item_idx += 1

    format_str += ' {{{0}}}'.format(item_idx)
    format_args.append(spec.version)
    item_idx += 1

    if is_main_phase(phase) is True or strip_compiler is False:
        format_str += ' {{{0}}}'.format(item_idx)
        format_args.append(spec.compiler)
        item_idx += 1

    format_str += ' {{{0}}}'.format(item_idx)
    format_args.append(osarch)
    item_idx += 1

    if build_group:
        format_str += ' {{{0}}}'.format(item_idx)
        format_args.append(build_group)
        item_idx += 1

    return format_str.format(*format_args)


def get_cdash_build_name(spec, build_group):
    return '{0}@{1}%{2} arch={3} ({4})'.format(
        spec.name, spec.version, spec.compiler, spec.architecture, build_group)


def get_spec_string(spec):
    format_elements = [
        '{name}{@version}',
        '{%compiler}',
    ]

    if spec.architecture:
        format_elements.append(' {arch=architecture}')

    return spec.format(''.join(format_elements))


def format_root_spec(spec, main_phase, strip_compiler):
    if main_phase is False and strip_compiler is True:
        return '{0}@{1} arch={2}'.format(
            spec.name, spec.version, spec.architecture)
    else:
        return spec.build_hash()


def spec_deps_key(s):
    return '{0}/{1}'.format(s.name, s.dag_hash(7))


def _add_dependency(spec_label, dep_label, deps):
    if spec_label == dep_label:
        return
    if spec_label not in deps:
        deps[spec_label] = set()
    deps[spec_label].add(dep_label)


def get_spec_dependencies(specs, deps, spec_labels, check_index_only=False):
    spec_deps_obj = compute_spec_deps(specs, check_index_only=check_index_only)

    if spec_deps_obj:
        dependencies = spec_deps_obj['dependencies']
        specs = spec_deps_obj['specs']

        for entry in specs:
            spec_labels[entry['label']] = {
                'spec': Spec(entry['spec']),
                'rootSpec': entry['root_spec'],
                'needs_rebuild': entry['needs_rebuild'],
            }

        for entry in dependencies:
            _add_dependency(entry['spec'], entry['depends'], deps)


def stage_spec_jobs(specs, check_index_only=False):
    """Take a set of release specs and generate a list of "stages", where the
        jobs in any stage are dependent only on jobs in previous stages.  This
        allows us to maximize build parallelism within the gitlab-ci framework.

    Arguments:
        specs (Iterable): Specs to build
        check_index_only (bool): Regardless of whether DAG pruning is enabled,
            all configured mirrors are searched to see if binaries for specs
            are up to date on those mirrors.  This flag limits that search to
            the binary cache indices on those mirrors to speed the process up,
            even though there is no garantee the index is up to date.

    Returns: A tuple of information objects describing the specs, dependencies
        and stages:

        spec_labels: A dictionary mapping the spec labels which are made of
            (pkg-name/hash-prefix), to objects containing "rootSpec" and "spec"
            keys.  The root spec is the spec of which this spec is a dependency
            and the spec is the formatted spec string for this spec.

        deps: A dictionary where the keys should also have appeared as keys in
            the spec_labels dictionary, and the values are the set of
            dependencies for that spec.

        stages: An ordered list of sets, each of which contains all the jobs to
            built in that stage.  The jobs are expressed in the same format as
            the keys in the spec_labels and deps objects.

    """

    # The convenience method below, "remove_satisfied_deps()", does not modify
    # the "deps" parameter.  Instead, it returns a new dictionary where only
    # dependencies which have not yet been satisfied are included in the
    # return value.
    def remove_satisfied_deps(deps, satisfied_list):
        new_deps = {}

        for key, value in iteritems(deps):
            new_value = set([v for v in value if v not in satisfied_list])
            if new_value:
                new_deps[key] = new_value

        return new_deps

    deps = {}
    spec_labels = {}

    get_spec_dependencies(
        specs, deps, spec_labels, check_index_only=check_index_only)

    # Save the original deps, as we need to return them at the end of the
    # function.  In the while loop below, the "dependencies" variable is
    # overwritten rather than being modified each time through the loop,
    # thus preserving the original value of "deps" saved here.
    dependencies = deps
    unstaged = set(spec_labels.keys())
    stages = []

    while dependencies:
        dependents = set(dependencies.keys())
        next_stage = unstaged.difference(dependents)
        stages.append(next_stage)
        unstaged.difference_update(next_stage)
        # Note that "dependencies" is a dictionary mapping each dependent
        # package to the set of not-yet-handled dependencies.  The final step
        # below removes all the dependencies that are handled by this stage.
        dependencies = remove_satisfied_deps(dependencies, next_stage)

    if unstaged:
        stages.append(unstaged.copy())

    return spec_labels, deps, stages


def print_staging_summary(spec_labels, dependencies, stages):
    if not stages:
        return

    tty.msg('  Staging summary:')
    stage_index = 0
    for stage in stages:
        tty.msg('    stage {0} ({1} jobs):'.format(stage_index, len(stage)))

        for job in sorted(stage):
            s = spec_labels[job]['spec']
            tty.msg('      [{1}] {0} -> {2}'.format(
                job,
                'x' if spec_labels[job]['needs_rebuild'] else ' ',
                get_spec_string(s)))

        stage_index += 1


def compute_spec_deps(spec_list, check_index_only=False):
    """
    Computes all the dependencies for the spec(s) and generates a JSON
    object which provides both a list of unique spec names as well as a
    comprehensive list of all the edges in the dependency graph.  For
    example, given a single spec like 'readline@7.0', this function
    generates the following JSON object:

    .. code-block:: JSON

       {
           "dependencies": [
               {
                   "depends": "readline/ip6aiun",
                   "spec": "readline/ip6aiun"
               },
               {
                   "depends": "ncurses/y43rifz",
                   "spec": "readline/ip6aiun"
               },
               {
                   "depends": "ncurses/y43rifz",
                   "spec": "readline/ip6aiun"
               },
               {
                   "depends": "pkgconf/eg355zb",
                   "spec": "ncurses/y43rifz"
               },
               {
                   "depends": "pkgconf/eg355zb",
                   "spec": "readline/ip6aiun"
               }
           ],
           "specs": [
               {
                 "root_spec": "readline@7.0%apple-clang@9.1.0 arch=darwin-...",
                 "spec": "readline@7.0%apple-clang@9.1.0 arch=darwin-highs...",
                 "label": "readline/ip6aiun"
               },
               {
                 "root_spec": "readline@7.0%apple-clang@9.1.0 arch=darwin-...",
                 "spec": "ncurses@6.1%apple-clang@9.1.0 arch=darwin-highsi...",
                 "label": "ncurses/y43rifz"
               },
               {
                 "root_spec": "readline@7.0%apple-clang@9.1.0 arch=darwin-...",
                 "spec": "pkgconf@1.5.4%apple-clang@9.1.0 arch=darwin-high...",
                 "label": "pkgconf/eg355zb"
               }
           ]
       }

    """
    spec_labels = {}

    specs = []
    dependencies = []

    def append_dep(s, d):
        dependencies.append({
            'spec': s,
            'depends': d,
        })

    for spec in spec_list:
        spec.concretize()

        # root_spec = get_spec_string(spec)
        root_spec = spec

        for s in spec.traverse(deptype=all):
            if s.external:
                tty.msg('Will not stage external pkg: {0}'.format(s))
                continue

            up_to_date_mirrors = bindist.get_mirrors_for_spec(
                spec=s, full_hash_match=True, index_only=check_index_only)

            skey = spec_deps_key(s)
            spec_labels[skey] = {
                'spec': get_spec_string(s),
                'root': root_spec,
                'needs_rebuild': not up_to_date_mirrors,
            }

            for d in s.dependencies(deptype=all):
                dkey = spec_deps_key(d)
                if d.external:
                    tty.msg('Will not stage external dep: {0}'.format(d))
                    continue

                append_dep(skey, dkey)

    for spec_label, spec_holder in spec_labels.items():
        specs.append({
            'label': spec_label,
            'spec': spec_holder['spec'],
            'root_spec': spec_holder['root'],
            'needs_rebuild': spec_holder['needs_rebuild'],
        })

    deps_json_obj = {
        'specs': specs,
        'dependencies': dependencies,
    }

    return deps_json_obj


def spec_matches(spec, match_string):
    return spec.satisfies(match_string)


def copy_attributes(attrs_list, src_dict, dest_dict):
    for runner_attr in attrs_list:
        if runner_attr in src_dict:
            if runner_attr in dest_dict and runner_attr == 'tags':
                # For 'tags', we combine the lists of tags, while
                # avoiding duplicates
                for tag in src_dict[runner_attr]:
                    if tag not in dest_dict[runner_attr]:
                        dest_dict[runner_attr].append(tag)
            elif runner_attr in dest_dict and runner_attr == 'variables':
                # For 'variables', we merge the dictionaries.  Any conflicts
                # (i.e. 'runner-attributes' has same variable key as the
                # higher level) we resolve by keeping the more specific
                # 'runner-attributes' version.
                for src_key, src_val in src_dict[runner_attr].items():
                    dest_dict[runner_attr][src_key] = copy.deepcopy(
                        src_dict[runner_attr][src_key])
            else:
                dest_dict[runner_attr] = copy.deepcopy(src_dict[runner_attr])


def find_matching_config(spec, gitlab_ci):
    runner_attributes = {}
    overridable_attrs = [
        'image',
        'tags',
        'variables',
        'before_script',
        'script',
        'after_script',
    ]

    copy_attributes(overridable_attrs, gitlab_ci, runner_attributes)

    ci_mappings = gitlab_ci['mappings']
    for ci_mapping in ci_mappings:
        for match_string in ci_mapping['match']:
            if spec_matches(spec, match_string):
                if 'runner-attributes' in ci_mapping:
                    copy_attributes(overridable_attrs,
                                    ci_mapping['runner-attributes'],
                                    runner_attributes)
                return runner_attributes
    else:
        return None

    return runner_attributes


def pkg_name_from_spec_label(spec_label):
    return spec_label[:spec_label.index('/')]


def format_job_needs(phase_name, strip_compilers, dep_jobs,
                     osname, build_group, prune_dag, stage_spec_dict,
                     enable_artifacts_buildcache):
    needs_list = []
    for dep_job in dep_jobs:
        dep_spec_key = spec_deps_key(dep_job)
        dep_spec_info = stage_spec_dict[dep_spec_key]

        if not prune_dag or dep_spec_info['needs_rebuild']:
            needs_list.append({
                'job': get_job_name(phase_name,
                                    strip_compilers,
                                    dep_job,
                                    osname,
                                    build_group),
                'artifacts': enable_artifacts_buildcache,
            })
    return needs_list


def add_mirror(name, url):
    cfg_scope = cfg.default_modify_scope()
    mirrors = cfg.get('mirrors', scope=cfg_scope)
    items = [(n, u) for n, u in mirrors.items()]
    items.insert(0, (name, url))
    cfg.set('mirrors', syaml.syaml_dict(items), scope=cfg_scope)


def remove_mirror(name):
    cfg_scope = cfg.default_modify_scope()
    mirrors = cfg.get('mirrors', scope=cfg_scope)
    mirrors.pop(name)
    cfg.set('mirrors', mirrors, scope=cfg_scope)


def generate_gitlab_ci_yaml(env, print_summary, output_file,
                            prune_dag=False, check_index_only=False,
                            run_optimizer=False, use_dependencies=False,
                            artifacts_root=None):
    # FIXME: What's the difference between one that opens with 'spack'
    # and one that opens with 'env'?  This will only handle the former.
    with spack.concretize.disable_compiler_existence_check():
        with env.write_transaction():
            env.concretize()
            env.write()

    yaml_root = ev.config_dict(env.yaml)

    if 'gitlab-ci' not in yaml_root:
        tty.die('Environment yaml does not have "gitlab-ci" section')

    gitlab_ci = yaml_root['gitlab-ci']

    build_group = None
    enable_cdash_reporting = False
    cdash_auth_token = None

    if 'cdash' in yaml_root:
        enable_cdash_reporting = True
        ci_cdash = yaml_root['cdash']
        build_group = ci_cdash['build-group']
        cdash_url = ci_cdash['url']
        cdash_project = ci_cdash['project']
        cdash_site = ci_cdash['site']

        if 'SPACK_CDASH_AUTH_TOKEN' in os.environ:
            tty.verbose("Using CDash auth token from environment")
            cdash_auth_token = os.environ.get('SPACK_CDASH_AUTH_TOKEN')

    generate_job_name = os.environ.get('CI_JOB_NAME', None)
    parent_pipeline_id = os.environ.get('CI_PIPELINE_ID', None)

    is_pr_pipeline = (
        os.environ.get('SPACK_IS_PR_PIPELINE', '').lower() == 'true'
    )

    spack_pr_branch = os.environ.get('SPACK_PR_BRANCH', None)
    pr_mirror_url = None
    if spack_pr_branch:
        pr_mirror_url = url_util.join(SPACK_PR_MIRRORS_ROOT_URL,
                                      spack_pr_branch)

    if 'mirrors' not in yaml_root or len(yaml_root['mirrors'].values()) < 1:
        tty.die('spack ci generate requires an env containing a mirror')

    ci_mirrors = yaml_root['mirrors']
    mirror_urls = [url for url in ci_mirrors.values()]
    remote_mirror_url = mirror_urls[0]

    # Check for a list of "known broken" specs that we should not bother
    # trying to build.
    broken_specs_url = ''
    known_broken_specs_encountered = []
    if 'broken-specs-url' in gitlab_ci:
        broken_specs_url = gitlab_ci['broken-specs-url']

    enable_artifacts_buildcache = False
    if 'enable-artifacts-buildcache' in gitlab_ci:
        enable_artifacts_buildcache = gitlab_ci['enable-artifacts-buildcache']

    rebuild_index_enabled = True
    if 'rebuild-index' in gitlab_ci and gitlab_ci['rebuild-index'] is False:
        rebuild_index_enabled = False

    temp_storage_url_prefix = None
    if 'temporary-storage-url-prefix' in gitlab_ci:
        temp_storage_url_prefix = gitlab_ci['temporary-storage-url-prefix']

    bootstrap_specs = []
    phases = []
    if 'bootstrap' in gitlab_ci:
        for phase in gitlab_ci['bootstrap']:
            try:
                phase_name = phase.get('name')
                strip_compilers = phase.get('compiler-agnostic')
            except AttributeError:
                phase_name = phase
                strip_compilers = False
            phases.append({
                'name': phase_name,
                'strip-compilers': strip_compilers,
            })

            for bs in env.spec_lists[phase_name]:
                bootstrap_specs.append({
                    'spec': bs,
                    'phase-name': phase_name,
                    'strip-compilers': strip_compilers,
                })

    phases.append({
        'name': 'specs',
        'strip-compilers': False,
    })

    # Add this mirror if it's enabled, as some specs might be up to date
    # here and thus not need to be rebuilt.
    if pr_mirror_url:
        add_mirror('ci_pr_mirror', pr_mirror_url)

    pipeline_artifacts_dir = artifacts_root
    if not pipeline_artifacts_dir:
        proj_dir = os.environ.get('CI_PROJECT_DIR', os.getcwd())
        pipeline_artifacts_dir = os.path.join(proj_dir, 'jobs_scratch_dir')

    pipeline_artifacts_dir = os.path.abspath(pipeline_artifacts_dir)
    concrete_env_dir = os.path.join(
        pipeline_artifacts_dir, 'concrete_environment')

    # Now that we've added the mirrors we know about, they should be properly
    # reflected in the environment manifest file, so copy that into the
    # concrete environment directory, along with the spack.lock file.
    if not os.path.exists(concrete_env_dir):
        os.makedirs(concrete_env_dir)
    shutil.copyfile(env.manifest_path,
                    os.path.join(concrete_env_dir, 'spack.yaml'))
    shutil.copyfile(env.lock_path,
                    os.path.join(concrete_env_dir, 'spack.lock'))

    job_log_dir = os.path.join(pipeline_artifacts_dir, 'logs')
    job_repro_dir = os.path.join(pipeline_artifacts_dir, 'reproduction')
    local_mirror_dir = os.path.join(pipeline_artifacts_dir, 'mirror')

    # Speed up staging by first fetching binary indices from all mirrors
    # (including the per-PR mirror we may have just added above).
    bindist.binary_index.update()

    staged_phases = {}
    try:
        for phase in phases:
            phase_name = phase['name']
            with spack.concretize.disable_compiler_existence_check():
                staged_phases[phase_name] = stage_spec_jobs(
                    env.spec_lists[phase_name],
                    check_index_only=check_index_only)
    finally:
        # Clean up PR mirror if enabled
        if pr_mirror_url:
            remove_mirror('ci_pr_mirror')

    all_job_names = []
    output_object = {}
    job_id = 0
    stage_id = 0

    stage_names = []

    max_length_needs = 0
    max_needs_job = ''

    before_script, after_script = None, None
    for phase in phases:
        phase_name = phase['name']
        strip_compilers = phase['strip-compilers']

        main_phase = is_main_phase(phase_name)
        spec_labels, dependencies, stages = staged_phases[phase_name]

        for stage_jobs in stages:
            stage_name = 'stage-{0}'.format(stage_id)
            stage_names.append(stage_name)
            stage_id += 1

            for spec_label in stage_jobs:
                spec_record = spec_labels[spec_label]
                root_spec = spec_record['rootSpec']
                pkg_name = pkg_name_from_spec_label(spec_label)
                release_spec = root_spec[pkg_name]

                # Check if this spec is in our list of known failures.
                if broken_specs_url:
                    full_hash = release_spec.full_hash()
                    broken_spec_path = url_util.join(broken_specs_url, full_hash)
                    if web_util.url_exists(broken_spec_path):
                        known_broken_specs_encountered.append('{0} ({1})'.format(
                            release_spec, full_hash))

                runner_attribs = find_matching_config(
                    release_spec, gitlab_ci)

                if not runner_attribs:
                    tty.warn('No match found for {0}, skipping it'.format(
                        release_spec))
                    continue

                tags = [tag for tag in runner_attribs['tags']]

                variables = {}
                if 'variables' in runner_attribs:
                    variables.update(runner_attribs['variables'])

                image_name = None
                image_entry = None
                if 'image' in runner_attribs:
                    build_image = runner_attribs['image']
                    try:
                        image_name = build_image.get('name')
                        entrypoint = build_image.get('entrypoint')
                        image_entry = [p for p in entrypoint]
                    except AttributeError:
                        image_name = build_image

                job_script = ['spack env activate --without-view .']

                if artifacts_root:
                    job_script.insert(0, 'cd {0}'.format(concrete_env_dir))

                job_script.extend([
                    'spack ci prebuild',
                    './install.sh',
                    'spack ci postbuild'
                ])

                if 'script' in runner_attribs:
                    job_script = [s for s in runner_attribs['script']]

                before_script = None
                if 'before_script' in runner_attribs:
                    before_script = [
                        s for s in runner_attribs['before_script']
                    ]

                after_script = None
                if 'after_script' in runner_attribs:
                    after_script = [s for s in runner_attribs['after_script']]

                osname = str(release_spec.architecture)
                job_name = get_job_name(phase_name, strip_compilers,
                                        release_spec, osname, build_group)

                compiler_action = 'NONE'
                if len(phases) > 1:
                    compiler_action = 'FIND_ANY'
                    if is_main_phase(phase_name):
                        compiler_action = 'INSTALL_MISSING'

                job_vars = {
                    'SPACK_ROOT_SPEC': format_root_spec(
                        root_spec, main_phase, strip_compilers),
                    'SPACK_JOB_SPEC_DAG_HASH': release_spec.dag_hash(),
                    'SPACK_JOB_SPEC_PKG_NAME': release_spec.name,
                    'SPACK_COMPILER_ACTION': compiler_action
                }

                job_dependencies = []
                if spec_label in dependencies:
                    if enable_artifacts_buildcache:
                        # Get dependencies transitively, so they're all
                        # available in the artifacts buildcache.
                        dep_jobs = [
                            d for d in release_spec.traverse(deptype=all,
                                                             root=False)
                        ]
                    else:
                        # In this case, "needs" is only used for scheduling
                        # purposes, so we only get the direct dependencies.
                        dep_jobs = []
                        for dep_label in dependencies[spec_label]:
                            dep_pkg = pkg_name_from_spec_label(dep_label)
                            dep_root = spec_labels[dep_label]['rootSpec']
                            dep_jobs.append(dep_root[dep_pkg])

                    job_dependencies.extend(
                        format_job_needs(phase_name, strip_compilers,
                                         dep_jobs, osname, build_group,
                                         prune_dag, spec_labels,
                                         enable_artifacts_buildcache))

                rebuild_spec = spec_record['needs_rebuild']

                # This next section helps gitlab make sure the right
                # bootstrapped compiler exists in the artifacts buildcache by
                # creating an artificial dependency between this spec and its
                # compiler.  So, if we are in the main phase, and if the
                # compiler we are supposed to use is listed in any of the
                # bootstrap spec lists, then we will add more dependencies to
                # the job (that compiler and maybe it's dependencies as well).
                if is_main_phase(phase_name):
                    spec_arch_family = (release_spec.architecture
                                                    .target
                                                    .microarchitecture
                                                    .family)
                    compiler_pkg_spec = compilers.pkg_spec_for_compiler(
                        release_spec.compiler)
                    for bs in bootstrap_specs:
                        c_spec = bs['spec']
                        bs_arch = c_spec.architecture
                        bs_arch_family = (bs_arch.target
                                                 .microarchitecture
                                                 .family)
                        if (c_spec.satisfies(compiler_pkg_spec) and
                            bs_arch_family == spec_arch_family):
                            # We found the bootstrap compiler this release spec
                            # should be built with, so for DAG scheduling
                            # purposes, we will at least add the compiler spec
                            # to the jobs "needs".  But if artifact buildcache
                            # is enabled, we'll have to add all transtive deps
                            # of the compiler as well.

                            # Here we check whether the bootstrapped compiler
                            # needs to be rebuilt.  Until compilers are proper
                            # dependencies, we artificially force the spec to
                            # be rebuilt if the compiler targeted to build it
                            # needs to be rebuilt.
                            bs_specs, _, _ = staged_phases[bs['phase-name']]
                            c_spec_key = spec_deps_key(c_spec)
                            rbld_comp = bs_specs[c_spec_key]['needs_rebuild']
                            rebuild_spec = rebuild_spec or rbld_comp
                            # Also update record so dependents do not fail to
                            # add this spec to their "needs"
                            spec_record['needs_rebuild'] = rebuild_spec

                            dep_jobs = [c_spec]
                            if enable_artifacts_buildcache:
                                dep_jobs = [
                                    d for d in c_spec.traverse(deptype=all)
                                ]

                            job_dependencies.extend(
                                format_job_needs(bs['phase-name'],
                                                 bs['strip-compilers'],
                                                 dep_jobs,
                                                 str(bs_arch),
                                                 build_group,
                                                 prune_dag,
                                                 bs_specs,
                                                 enable_artifacts_buildcache))
                        else:
                            debug_msg = ''.join([
                                'Considered compiler {0} for spec ',
                                '{1}, but rejected it either because it was ',
                                'not the compiler required by the spec, or ',
                                'because the target arch families of the ',
                                'spec and the compiler did not match'
                            ]).format(c_spec, release_spec)
                            tty.debug(debug_msg)

                if prune_dag and not rebuild_spec:
                    continue

                if artifacts_root:
                    job_dependencies.append({
                        'job': generate_job_name,
                        'pipeline': '{0}'.format(parent_pipeline_id)
                    })

                job_vars['SPACK_SPEC_NEEDS_REBUILD'] = str(rebuild_spec)

                if enable_cdash_reporting:
                    cdash_build_name = get_cdash_build_name(
                        release_spec, build_group)
                    all_job_names.append(cdash_build_name)

                    related_builds = []      # Used for relating CDash builds
                    if spec_label in dependencies:
                        related_builds = (
                            [spec_labels[d]['spec'].name
                                for d in dependencies[spec_label]])

                    job_vars['SPACK_CDASH_BUILD_NAME'] = cdash_build_name
                    job_vars['SPACK_RELATED_BUILDS_CDASH'] = ';'.join(
                        sorted(related_builds))

                variables.update(job_vars)

                artifact_paths = [
                    job_log_dir,
                    job_repro_dir
                ]

                if enable_artifacts_buildcache:
                    bc_root = os.path.join(
                        local_mirror_dir, 'build_cache')
                    artifact_paths.extend([os.path.join(bc_root, p) for p in [
                        bindist.tarball_name(release_spec, '.spec.yaml'),
                        bindist.tarball_name(release_spec, '.cdashid'),
                        bindist.tarball_directory_name(release_spec),
                    ]])

                job_object = {
                    'stage': stage_name,
                    'variables': variables,
                    'script': job_script,
                    'tags': tags,
                    'artifacts': {
                        'paths': artifact_paths,
                        'when': 'always',
                    },
                    'needs': sorted(job_dependencies, key=lambda d: d['job']),
                    'retry': {
                        'max': 2,
                        'when': JOB_RETRY_CONDITIONS,
                    },
                    'interruptible': True
                }

                length_needs = len(job_dependencies)
                if length_needs > max_length_needs:
                    max_length_needs = length_needs
                    max_needs_job = job_name

                if before_script:
                    job_object['before_script'] = before_script

                if after_script:
                    job_object['after_script'] = after_script

                if image_name:
                    job_object['image'] = image_name
                    if image_entry is not None:
                        job_object['image'] = {
                            'name': image_name,
                            'entrypoint': image_entry,
                        }

                output_object[job_name] = job_object
                job_id += 1

    if print_summary:
        for phase in phases:
            phase_name = phase['name']
            tty.msg('Stages for phase "{0}"'.format(phase_name))
            phase_stages = staged_phases[phase_name]
            print_staging_summary(*phase_stages)

    tty.debug('{0} build jobs generated in {1} stages'.format(
        job_id, stage_id))

    if job_id > 0:
        tty.debug('The max_needs_job is {0}, with {1} needs'.format(
            max_needs_job, max_length_needs))

    # Use "all_job_names" to populate the build group for this set
    if enable_cdash_reporting and cdash_auth_token:
        try:
            populate_buildgroup(all_job_names, build_group, cdash_project,
                                cdash_site, cdash_auth_token, cdash_url)
        except (SpackError, HTTPError, URLError) as err:
            tty.warn('Problem populating buildgroup: {0}'.format(err))
    else:
        tty.warn('Unable to populate buildgroup without CDash credentials')

    service_job_config = None
    if 'service-job-attributes' in gitlab_ci:
        service_job_config = gitlab_ci['service-job-attributes']

    default_attrs = [
        'image',
        'tags',
        'variables',
        'before_script',
        # 'script',
        'after_script',
    ]

    if job_id > 0:
        if temp_storage_url_prefix:
            # There were some rebuild jobs scheduled, so we will need to
            # schedule a job to clean up the temporary storage location
            # associated with this pipeline.
            stage_names.append('cleanup-temp-storage')
            cleanup_job = {}

            if service_job_config:
                copy_attributes(default_attrs,
                                service_job_config,
                                cleanup_job)

            cleanup_job['stage'] = 'cleanup-temp-storage'
            cleanup_job['script'] = [
                'spack -d mirror destroy --mirror-url {0}/$CI_PIPELINE_ID'.format(
                    temp_storage_url_prefix)
            ]
            cleanup_job['when'] = 'always'

            output_object['cleanup'] = cleanup_job

        if rebuild_index_enabled:
            # Add a final job to regenerate the index
            stage_names.append('stage-rebuild-index')
            final_job = {}

            if service_job_config:
                copy_attributes(default_attrs,
                                service_job_config,
                                final_job)

            index_target_mirror = mirror_urls[0]
            if is_pr_pipeline:
                index_target_mirror = pr_mirror_url

            final_job['stage'] = 'stage-rebuild-index'
            final_job['script'] = [
                'spack buildcache update-index --keys -d {0}'.format(
                    index_target_mirror)
            ]
            final_job['when'] = 'always'

            if artifacts_root:
                final_job['variables'] = {
                    'SPACK_CONCRETE_ENV_DIR': concrete_env_dir
                }

            output_object['rebuild-index'] = final_job

        output_object['stages'] = stage_names

        # Capture the version of spack used to generate the pipeline, transform it
        # into a value that can be passed to "git checkout", and save it in a
        # global yaml variable
        spack_version = spack.main.get_version()
        version_to_clone = None
        v_match = re.match(r"^\d+\.\d+\.\d+$", spack_version)
        if v_match:
            version_to_clone = 'v{0}'.format(v_match.group(0))
        else:
            v_match = re.match(r"^[^-]+-[^-]+-([a-f\d]+)$", spack_version)
            if v_match:
                version_to_clone = v_match.group(1)
            else:
                version_to_clone = spack_version

        output_object['variables'] = {
            'SPACK_ARTIFACTS_ROOT': pipeline_artifacts_dir,
            'SPACK_CONCRETE_ENV_DIR': concrete_env_dir,
            'SPACK_VERSION': spack_version,
            'SPACK_CHECKOUT_VERSION': version_to_clone,
            'SPACK_REMOTE_MIRROR_URL': remote_mirror_url,
            'SPACK_JOB_LOG_DIR': job_log_dir,
            'SPACK_JOB_REPRO_DIR': job_repro_dir,
            'SPACK_LOCAL_MIRROR_DIR': local_mirror_dir,
            'SPACK_IS_PR_PIPELINE': str(is_pr_pipeline)
        }

        if pr_mirror_url:
            output_object['variables']['SPACK_PR_MIRROR_URL'] = pr_mirror_url

        sorted_output = {}
        for output_key, output_value in sorted(output_object.items()):
            sorted_output[output_key] = output_value

        # TODO(opadron): remove this or refactor
        if run_optimizer:
            import spack.ci_optimization as ci_opt
            sorted_output = ci_opt.optimizer(sorted_output)

        # TODO(opadron): remove this or refactor
        if use_dependencies:
            import spack.ci_needs_workaround as cinw
            sorted_output = cinw.needs_to_dependencies(sorted_output)
    else:
        # No jobs were generated
        tty.debug('No specs to rebuild, generating no-op job')
        noop_job = {}

        if service_job_config:
            copy_attributes(default_attrs,
                            service_job_config,
                            noop_job)

        if 'script' not in noop_job:
            noop_job['script'] = [
                'echo "All specs already up to date, nothing to rebuild."',
            ]

        sorted_output = {'no-specs-to-rebuild': noop_job}

    if known_broken_specs_encountered:
        error_msg = (
            'Pipeline generation failed due to the presence of the '
            'following specs that are known to be broken in develop:\n')
        for broken_spec in known_broken_specs_encountered:
            error_msg += '* {0}\n'.format(broken_spec)
        tty.die(error_msg)

    with open(output_file, 'w') as outf:
        outf.write(syaml.dump_config(sorted_output, default_flow_style=True))


def url_encode_string(input_string):
    encoded_keyval = urlencode({'donotcare': input_string})
    eq_idx = encoded_keyval.find('=') + 1
    encoded_value = encoded_keyval[eq_idx:]
    return encoded_value


def import_signing_key(base64_signing_key):
    if not base64_signing_key:
        tty.warn('No key found for signing/verifying packages')
        return

    tty.debug('ci.import_signing_key() will attempt to import a key')

    # This command has the side-effect of creating the directory referred
    # to as GNUPGHOME in setup_environment()
    list_output = spack_gpg('list', output=str)

    tty.debug('spack gpg list:')
    tty.debug(list_output)

    decoded_key = base64.b64decode(base64_signing_key)
    if isinstance(decoded_key, bytes):
        decoded_key = decoded_key.decode('utf8')

    with TemporaryDirectory() as tmpdir:
        sign_key_path = os.path.join(tmpdir, 'signing_key')
        with open(sign_key_path, 'w') as fd:
            fd.write(decoded_key)

        key_import_output = spack_gpg('trust', sign_key_path, output=str)
        tty.debug('spack gpg trust {0}'.format(sign_key_path))
        tty.debug(key_import_output)

    # Now print the keys we have for verifying and signing
    trusted_keys_output = spack_gpg('list', '--trusted', output=str)
    signing_keys_output = spack_gpg('list', '--signing', output=str)

    tty.debug('spack gpg list --trusted')
    tty.debug(trusted_keys_output)
    tty.debug('spack gpg list --signing')
    tty.debug(signing_keys_output)


def can_sign_binaries():
    return len(gpg_util.signing_keys()) == 1


def can_verify_binaries():
    return len(gpg_util.public_keys()) >= 1


def configure_compilers(compiler_action, scope=None):
    if compiler_action == 'INSTALL_MISSING':
        tty.debug('Make sure bootstrapped compiler will be installed')
        config = cfg.get('config')
        config['install_missing_compilers'] = True
        cfg.set('config', config)
    elif compiler_action == 'FIND_ANY':
        tty.debug('Just find any available compiler')
        find_args = ['find']
        if scope:
            find_args.extend(['--scope', scope])
        output = spack_compiler(*find_args)
        tty.debug('spack compiler find')
        tty.debug(output)
        output = spack_compiler('list')
        tty.debug('spack compiler list')
        tty.debug(output)
    else:
        tty.debug('No compiler action to be taken')

    return None


def get_concrete_specs(env, root_spec, job_name, related_builds,
                       compiler_action):
    spec_map = {
        'root': None,
        'deps': {},
    }

    if compiler_action == 'FIND_ANY':
        # This corresponds to a bootstrapping phase where we need to
        # rely on any available compiler to build the package (i.e. the
        # compiler needed to be stripped from the spec when we generated
        # the job), and thus we need to concretize the root spec again.
        tty.debug('About to concretize {0}'.format(root_spec))
        concrete_root = Spec(root_spec).concretized()
        tty.debug('Resulting concrete root: {0}'.format(concrete_root))
    else:
        # in this case, either we're relying on Spack to install missing
        # compiler bootstrapped in a previous phase, or else we only had one
        # phase (like a site which already knows what compilers are available
        # on it's runners), so we don't want to concretize that root spec
        # again.  The reason we take this path in the first case (bootstrapped
        # compiler), is that we can't concretize a spec at this point if we're
        # going to ask spack to "install_missing_compilers".
        concrete_root = env.specs_by_hash[root_spec]

    spec_map['root'] = concrete_root
    spec_map[job_name] = concrete_root[job_name]

    if related_builds:
        for dep_job_name in related_builds.split(';'):
            spec_map['deps'][dep_job_name] = concrete_root[dep_job_name]

    return spec_map


def register_cdash_build(build_name, base_url, project, site, track):
    url = base_url + '/api/v1/addBuild.php'
    time_stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M')
    build_stamp = '{0}-{1}'.format(time_stamp, track)
    payload = {
        "project": project,
        "site": site,
        "name": build_name,
        "stamp": build_stamp,
    }

    tty.debug('Registering cdash build to {0}, payload:'.format(url))
    tty.debug(payload)

    enc_data = json.dumps(payload).encode('utf-8')

    headers = {
        'Content-Type': 'application/json',
    }

    opener = build_opener(HTTPHandler)

    request = Request(url, data=enc_data, headers=headers)

    response = opener.open(request)
    response_code = response.getcode()

    if response_code != 200 and response_code != 201:
        msg = 'Adding build failed (response code = {0}'.format(response_code)
        raise SpackError(msg)

    response_text = response.read()
    response_json = json.loads(response_text)
    build_id = response_json['buildid']

    return (build_id, build_stamp)


def relate_cdash_builds(spec_map, cdash_base_url, job_build_id, cdash_project,
                        cdashids_mirror_url):
    if not job_build_id:
        return

    dep_map = spec_map['deps']

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    cdash_api_url = '{0}/api/v1/relateBuilds.php'.format(cdash_base_url)

    for dep_pkg_name in dep_map:
        tty.debug('Fetching cdashid file for {0}'.format(dep_pkg_name))
        dep_spec = dep_map[dep_pkg_name]
        dep_build_id = read_cdashid_from_mirror(dep_spec, cdashids_mirror_url)

        payload = {
            "project": cdash_project,
            "buildid": job_build_id,
            "relatedid": dep_build_id,
            "relationship": "depends on"
        }

        enc_data = json.dumps(payload).encode('utf-8')

        opener = build_opener(HTTPHandler)

        request = Request(cdash_api_url, data=enc_data, headers=headers)

        response = opener.open(request)
        response_code = response.getcode()

        if response_code != 200 and response_code != 201:
            msg = 'Relate builds ({0} -> {1}) failed (resp code = {2})'.format(
                job_build_id, dep_build_id, response_code)
            raise SpackError(msg)

        response_text = response.read()
        tty.debug('Relate builds response: {0}'.format(response_text))


def write_cdashid_to_mirror(cdashid, spec, mirror_url):
    if not spec.concrete:
        tty.die('Can only write cdashid for concrete spec to mirror')

    with TemporaryDirectory() as tmpdir:
        local_cdash_path = os.path.join(tmpdir, 'job.cdashid')
        with open(local_cdash_path, 'w') as fd:
            fd.write(cdashid)

        buildcache_name = bindist.tarball_name(spec, '')
        cdashid_file_name = '{0}.cdashid'.format(buildcache_name)
        remote_url = os.path.join(
            mirror_url, bindist.build_cache_relative_path(), cdashid_file_name)

        tty.debug('pushing cdashid to url')
        tty.debug('  local file path: {0}'.format(local_cdash_path))
        tty.debug('  remote url: {0}'.format(remote_url))
        web_util.push_to_url(local_cdash_path, remote_url)


def read_cdashid_from_mirror(spec, mirror_url):
    if not spec.concrete:
        tty.die('Can only read cdashid for concrete spec from mirror')

    buildcache_name = bindist.tarball_name(spec, '')
    cdashid_file_name = '{0}.cdashid'.format(buildcache_name)
    url = os.path.join(
        mirror_url, bindist.build_cache_relative_path(), cdashid_file_name)

    resp_url, resp_headers, response = web_util.read_from_url(url)
    contents = response.fp.read()

    return int(contents)


def push_mirror_contents(env, spec, yaml_path, mirror_url, build_id,
                         sign_binaries):
    if mirror_url:
        try:
            unsigned = not sign_binaries
            tty.debug('Creating buildcache ({0})'.format(
                'unsigned' if unsigned else 'signed'))
            spack.cmd.buildcache._createtarball(
                env, spec_yaml=yaml_path, add_deps=False,
                output_location=mirror_url, force=True, allow_root=True,
                unsigned=unsigned)
            if build_id:
                tty.debug('Writing cdashid ({0}) to remote mirror: {1}'.format(
                    build_id, mirror_url))
                write_cdashid_to_mirror(build_id, spec, mirror_url)
        except Exception as inst:
            # If the mirror we're pushing to is on S3 and there's some
            # permissions problem, for example, we can't just target
            # that exception type here, since users of the
            # `spack ci rebuild' may not need or want any dependency
            # on boto3.  So we use the first non-boto exception type
            # in the heirarchy:
            #     boto3.exceptions.S3UploadFailedError
            #     boto3.exceptions.Boto3Error
            #     Exception
            #     BaseException
            #     object
            err_msg = 'Error msg: {0}'.format(inst)
            if 'Access Denied' in err_msg:
                tty.msg('Permission problem writing to {0}'.format(
                    mirror_url))
                tty.msg(err_msg)
            else:
                raise inst


def copy_stage_logs_to_artifacts(job_spec, job_log_dir):
    try:
        job_pkg = spack.repo.get(job_spec)
        tty.debug('job package: {0}'.format(job_pkg))
        stage_dir = job_pkg.stage.path
        tty.debug('stage dir: {0}'.format(stage_dir))
        build_out_src = os.path.join(stage_dir, 'spack-build-out.txt')
        build_out_dst = os.path.join(
            job_log_dir, 'spack-build-out.txt')
        tty.debug('Copying build log ({0}) to artifacts ({1})'.format(
            build_out_src, build_out_dst))
        shutil.copyfile(build_out_src, build_out_dst)
    except Exception as inst:
        msg = ('Unable to copy build logs from stage to artifacts '
               'due to exception: {0}').format(inst)
        tty.error(msg)


def download_and_extract_artifacts(url, work_dir):
    tty.msg('Fetching artifacts from: {0}\n'.format(url))

    headers = {
        'Content-Type': 'application/zip',
    }

    token = os.environ.get('GITLAB_PRIVATE_TOKEN', None)
    if token:
        headers['PRIVATE-TOKEN'] = token

    opener = build_opener(HTTPHandler)

    request = Request(url, headers=headers)
    request.get_method = lambda: 'GET'

    response = opener.open(request)
    response_code = response.getcode()

    if response_code != 200:
        msg = 'Error response code ({0}) in reproduce_ci_job'.format(
            response_code)
        raise SpackError(msg)

    artifacts_zip_path = os.path.join(work_dir, 'artifacts.zip')

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    with open(artifacts_zip_path, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

    with zipfile.ZipFile(artifacts_zip_path, 'r') as zip_ref:
        zip_ref.extractall(work_dir)

    os.remove(artifacts_zip_path)


def get_spack_info():
    git_path = os.path.join(spack.paths.prefix, ".git")
    if os.path.exists(git_path):
        git = exe.which("git")
        if git:
            with fs.working_dir(spack.paths.prefix):
                git_log = git("log", "-1",
                              output=str, error=os.devnull,
                              fail_on_error=False)

            return git_log

    return 'no git repo, use spack {0}'.format(spack.spack_version)


def setup_spack_repro_version(repro_dir, checkout_commit, merge_commit=None):
    # figure out the path to the spack git version being used for the
    # reproduction
    dot_git_path = os.path.join(spack.paths.prefix, ".git")
    if not os.path.exists(dot_git_path):
        tty.error('Unable to find the path to your local spack clone')
        return False

    spack_git_path = spack.paths.prefix

    git = exe.which("git")
    if not git:
        tty.error("reproduction of pipeline job requires git")
        return False

    # Check if we can find the tested commits in your local spack repo
    with fs.working_dir(spack_git_path):
        git("log", "-1", checkout_commit, output=str, error=os.devnull,
            fail_on_error=False)

        if git.returncode != 0:
            tty.error('Missing commit: {0}'.format(checkout_commit))
            return False

        if merge_commit:
            git("log", "-1", merge_commit, output=str, error=os.devnull,
                fail_on_error=False)

            if git.returncode != 0:
                tty.error('Missing commit: {0}'.format(merge_commit))
                return False

    # Next attempt to clone your local spack repo into the repro dir
    with fs.working_dir(repro_dir):
        clone_out = git("clone", spack_git_path,
                        output=str, error=os.devnull,
                        fail_on_error=False)

        if git.returncode != 0:
            tty.error('Unable to clone your local spac repo:')
            tty.msg(clone_out)
            return False

    # Finally, attempt to put the cloned repo into the same state used during
    # the pipeline build job
    repro_spack_path = os.path.join(repro_dir, 'spack')
    with fs.working_dir(repro_spack_path):
        co_out = git("checkout", checkout_commit,
                     output=str, error=os.devnull,
                     fail_on_error=False)

        if git.returncode != 0:
            tty.error('Unable to checkout {0}'.format(checkout_commit))
            tty.msg(co_out)
            return False

        if merge_commit:
            merge_out = git("-c", "user.name=cirepro", "-c",
                            "user.email=user@email.org", "merge",
                            "--no-edit", merge_commit,
                            output=str, error=os.devnull,
                            fail_on_error=False)

            if git.returncode != 0:
                tty.error('Unable to merge {0}'.format(merge_commit))
                tty.msg(merge_out)
                return False

    return True


def reproduce_ci_job(url, work_dir):
    download_and_extract_artifacts(url, work_dir)

    lock_file = fs.find(work_dir, 'spack.lock')[0]
    concrete_env_dir = os.path.dirname(lock_file)

    tty.debug('Concrete environment directory: {0}'.format(
        concrete_env_dir))

    yaml_files = fs.find(work_dir, ['*.yaml', '*.yml'])

    tty.debug('yaml files:')
    for yaml_file in yaml_files:
        tty.debug('  {0}'.format(yaml_file))

    pipeline_yaml = None
    pipeline_variables = None

    for yf in yaml_files:
        with open(yf) as y_fd:
            yaml_obj = syaml.load(y_fd)
            if 'variables' in yaml_obj and 'stages' in yaml_obj:
                pipeline_yaml = yaml_obj
                pipeline_variables = pipeline_yaml['variables']

    if pipeline_yaml:
        tty.debug('\n{0} is likely your pipeline file'.format(yf))

    # Find the install script in the unzipped artifacts and make it executable
    install_script = fs.find(work_dir, 'install.sh')[0]
    st = os.stat(install_script)
    os.chmod(install_script, st.st_mode | stat.S_IEXEC)

    # Find the repro details file
    repro_file = fs.find(work_dir, 'repro.json')[0]
    repro_details = None
    with open(repro_file) as fd:
        repro_details = json.load(fd)

    mount_as_dir = '/work'
    if pipeline_variables:
        artifacts_root = pipeline_variables['SPACK_ARTIFACTS_ROOT']
        mount_as_dir = os.path.dirname(artifacts_root)

    repro_dir = os.path.dirname(repro_file)
    rel_repro_dir = repro_dir.replace(work_dir, '').lstrip(os.path.sep)
    mounted_repro_dir = os.path.join(mount_as_dir, rel_repro_dir)

    spack_info_file = fs.find(work_dir, 'spack_info.txt')[0]
    with open(spack_info_file) as fd:
        spack_info = fd.read()

    commit_1 = None
    commit_2 = None
    commit_regex = re.compile(r"commit\s+([^\s]+)")
    merge_commit_regex = re.compile(r"Merge\s+([^\s]+)\s+into\s+([^\s]+)")

    # Try the more specific merge commit regex first
    m = merge_commit_regex.search(spack_info)
    if m:
        # This was a merge commit and we captured the parents
        commit_1 = m.group(1)
        commit_2 = m.group(2)
    else:
        # Not a merge commit, just get the commit sha
        m = commit_regex.search(spack_info)
        if m:
            commit_1 = m.group(1)

    setup_result = False
    if commit_1:
        if commit_2:
            setup_result = setup_spack_repro_version(
                work_dir, commit_2, merge_commit=commit_1)
        else:
            setup_result = setup_spack_repro_version(work_dir, commit_1)

    if not setup_result:
        setup_msg = """
    This can happen if the spack you are using to run this command is not a git
    repo, or if it is a git repo, but it does not have the commits needed to
    recreate the tested merge commit.  If you are trying to reproduce a spack
    PR pipeline job failure, try fetching the latest develop commits from
    mainline spack and make sure you have the most recent commit of the PR
    branch in your local spack repo.  Then run this command again.
    Alternatively, you can also manually clone spack if you know the version
    you want to test.
        """
        tty.error('Failed to automatically setup the tested version of spack '
                  'in your local reproduction directory.')
        print(setup_msg)

    job_name = repro_details['job_name']
    job_yaml = None

    if job_name in pipeline_yaml:
        job_yaml = pipeline_yaml[job_name]

    if job_yaml:
        tty.debug('Found job:')
        tty.debug(job_yaml)

    job_image = None
    if 'image' in job_yaml:
        job_image_elt = job_yaml['image']
        if 'name' in job_image_elt:
            job_image = job_image_elt['name']
        else:
            job_image = job_image_elt
        tty.msg('Job ran with the following image: {0}'.format(job_image))

    job_tags = None
    if 'tags' in job_yaml:
        job_tags = job_yaml['tags']
        tty.msg('Job ran with the following tags: {0}'.format(job_tags))

    inst_list = []

    if job_image:
        inst_list.append('\nRun the following command:\n\n')
        inst_list.append('    $ docker run --rm -v {0}:{1} -ti {2}\n'.format(
            work_dir, mount_as_dir, job_image))
        inst_list.append('\nOnce inside the container:\n\n')
    else:
        inst_list.append('\nOnce on the tagged runner:\n\n')

    if not setup_result:
        inst_list.append('    - Clone spack and acquire tested commit\n')
        inst_list.append('{0}'.format(spack_info))
        spack_root = '<spack-clone-path>'
    else:
        spack_root = '{0}/spack'.format(mount_as_dir)

    inst_list.append('    - Activate the environment\n\n')
    inst_list.append('        $ source {0}/share/spack/setup-env.sh\n'.format(
        spack_root))
    inst_list.append(
        '        $ spack env activate --without-view {0}\n\n'.format(
            mounted_repro_dir if job_image else repro_dir))
    inst_list.append('    - Run the install script\n\n')
    inst_list.append('        $ {0}\n'.format(
        os.path.join(mounted_repro_dir, 'install.sh')
        if job_image else install_script))

    print(''.join(inst_list))
