# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import os
import shutil
import stat
import sys
import tempfile

from six.moves.urllib.parse import urlencode

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.ci as spack_ci
import spack.cmd.buildcache as buildcache
import spack.environment as ev
import spack.hash_types as ht
import spack.spec as spack_spec
import spack.util.url as url_util
import spack.util.web as web_util


description = "manage continuous integration pipelines"
section = "build"
level = "long"


def get_env_var(variable_name):
    if variable_name in os.environ:
        return os.environ.get(variable_name)
    return None


def setup_parser(subparser):
    setup_parser.parser = subparser
    subparsers = subparser.add_subparsers(help='CI sub-commands')

    # Dynamic generation of the jobs yaml from a spack environment
    generate = subparsers.add_parser('generate', help=ci_generate.__doc__)
    generate.add_argument(
        '--output-file', default=None,
        help="Path to file where generated jobs file should be " +
             "written.  The default is .gitlab-ci.yml in the root of the " +
             "repository.")
    generate.add_argument(
        '--copy-to', default=None,
        help="Absolute path of additional location where generated jobs " +
             "yaml file should be copied.  Default is not to copy.")
    generate.add_argument(
        '--optimize', action='store_true', default=False,
        help="(Experimental) run the generated document through a series of "
             "optimization passes designed to reduce the size of the "
             "generated file.")
    generate.add_argument(
        '--dependencies', action='store_true', default=False,
        help="(Experimental) disable DAG scheduling; use "
             ' "plain" dependencies.')
    prune_group = generate.add_mutually_exclusive_group()
    prune_group.add_argument(
        '--prune-dag', action='store_true', dest='prune_dag',
        default=True, help="""Do not generate jobs for specs already up to
date on the mirror""")
    prune_group.add_argument(
        '--no-prune-dag', action='store_false', dest='prune_dag',
        default=True, help="""Generate jobs for specs already up to date
on the mirror""")
    generate.add_argument(
        '--check-index-only', action='store_true', dest='index_only',
        default=False, help="""Spack always check specs against configured
binary mirrors when generating the pipeline, regardless of whether or not
DAG pruning is enabled.  This flag controls whether it might attempt to
fetch remote spec.yaml files directly (ensuring no spec is rebuilt if it is
present on the mirror), or whether it should reduce pipeline generation time
by assuming all remote buildcache indices are up to date and only use those
to determine whether a given spec is up to date on mirrors.  In the latter
case, specs might be needlessly rebuilt if remote buildcache indices are out
of date.""")
    generate.add_argument(
        '--artifacts-root', default=None,
        help="""Path to root of artifacts directory.  If provided, concrete
environment files (spack.yaml, spack.lock) will be generated under this
path and their location sent to generated child jobs via the custom job
variable SPACK_CONCRETE_ENVIRONMENT_PATH.""")
    generate.set_defaults(func=ci_generate)

    # Rebuild the buildcache index associated with the mirror in the
    # active, gitlab-enabled environment.
    index = subparsers.add_parser('rebuild-index', help=ci_reindex.__doc__)
    index.set_defaults(func=ci_reindex)

    # Prepare for a spack install and generate the command line
    prebuild = subparsers.add_parser('prebuild', help=ci_prebuild.__doc__)
    prebuild.set_defaults(func=ci_prebuild)

    # Execute post install steps
    postbuild = subparsers.add_parser('postbuild', help=ci_postbuild.__doc__)
    postbuild.set_defaults(func=ci_postbuild)

    reproduce = subparsers.add_parser('reproduce-build',
                                      help=ci_reproduce.__doc__)
    reproduce.add_argument('job_url', help='Url of job artifacts bundle')
    reproduce.add_argument('--working-dir', help="Where to unpack artifacts",
                           default=os.path.join(os.getcwd(), 'ci_reproduction'))

    reproduce.set_defaults(func=ci_reproduce)


def ci_generate(args):
    """Generate jobs file from a spack environment file containing CI info.
       Before invoking this command, you can set the environment variable
       SPACK_CDASH_AUTH_TOKEN to contain the CDash authorization token
       for creating a build group for the generated workload and registering
       all generated jobs under that build group.  If this environment
       variable is not set, no build group will be created on CDash."""
    env = ev.get_env(args, 'ci generate', required=True)

    output_file = args.output_file
    copy_yaml_to = args.copy_to
    run_optimizer = args.optimize
    use_dependencies = args.dependencies
    prune_dag = args.prune_dag
    index_only = args.index_only
    artifacts_root = args.artifacts_root

    if not output_file:
        output_file = os.path.abspath(".gitlab-ci.yml")
    else:
        output_file_path = os.path.abspath(output_file)
        gen_ci_dir = os.path.dirname(output_file_path)
        if not os.path.exists(gen_ci_dir):
            os.makedirs(gen_ci_dir)

    # Generate the jobs
    spack_ci.generate_gitlab_ci_yaml(
        env, True, output_file, prune_dag=prune_dag,
        check_index_only=index_only, run_optimizer=run_optimizer,
        use_dependencies=use_dependencies, artifacts_root=artifacts_root)

    if copy_yaml_to:
        copy_to_dir = os.path.dirname(copy_yaml_to)
        if not os.path.exists(copy_to_dir):
            os.makedirs(copy_to_dir)
        shutil.copyfile(output_file, copy_yaml_to)


def ci_reindex(args):
    """Rebuild the buildcache index associated with the mirror in the
       active, gitlab-enabled environment. """
    env = ev.get_env(args, 'ci rebuild-index', required=True)
    yaml_root = ev.config_dict(env.yaml)

    if 'mirrors' not in yaml_root or len(yaml_root['mirrors'].values()) < 1:
        tty.die('spack ci rebuild-index requires an env containing a mirror')

    ci_mirrors = yaml_root['mirrors']
    mirror_urls = [url for url in ci_mirrors.values()]
    remote_mirror_url = mirror_urls[0]

    buildcache.update_index(remote_mirror_url, update_keys=True)


def ci_prebuild(args):
    env = ev.get_env(args, 'ci prebuild', required=True)
    yaml_root = ev.config_dict(env.yaml)

    pipeline_artifacts_dir = get_env_var('SPACK_ARTIFACTS_ROOT')
    job_log_dir = get_env_var('SPACK_JOB_LOG_DIR')
    repro_dir = get_env_var('SPACK_JOB_REPRO_DIR')
    local_mirror_dir = get_env_var('SPACK_LOCAL_MIRROR_DIR')
    concrete_env_dir = get_env_var('SPACK_CONCRETE_ENV_DIR')
    ci_pipeline_id = get_env_var('CI_PIPELINE_ID')
    ci_job_name = get_env_var('CI_JOB_NAME')
    signing_key = get_env_var('SPACK_SIGNING_KEY')
    root_spec = get_env_var('SPACK_ROOT_SPEC')
    # TODO: eventually use DAG hash to identify spec to install
    # spec_dag_hash = get_env_var('SPACK_JOB_SPEC_DAG_HASH')
    job_spec_pkg_name = get_env_var('SPACK_JOB_SPEC_PKG_NAME')
    compiler_action = get_env_var('SPACK_COMPILER_ACTION')
    cdash_build_name = get_env_var('SPACK_CDASH_BUILD_NAME')
    related_builds = get_env_var('SPACK_RELATED_BUILDS_CDASH')
    pr_env_var = get_env_var('SPACK_IS_PR_PIPELINE')
    remote_mirror_url = get_env_var('SPACK_REMOTE_MIRROR_URL')

    gitlab_ci = None
    if 'gitlab-ci' in yaml_root:
        gitlab_ci = yaml_root['gitlab-ci']

    if not gitlab_ci:
        tty.die('spack ci rebuild requires an env containing gitlab-ci cfg')

    enable_cdash = False
    if 'cdash' in yaml_root:
        enable_cdash = True
        ci_cdash = yaml_root['cdash']
        job_spec_buildgroup = ci_cdash['build-group']
        cdash_base_url = ci_cdash['url']
        cdash_project = ci_cdash['project']
        proj_enc = urlencode({'project': cdash_project})
        eq_idx = proj_enc.find('=') + 1
        cdash_project_enc = proj_enc[eq_idx:]
        cdash_site = ci_cdash['site']
        tty.debug('cdash_base_url = {0}'.format(cdash_base_url))
        tty.debug('cdash_project = {0}'.format(cdash_project))
        tty.debug('cdash_project_enc = {0}'.format(cdash_project_enc))
        tty.debug('cdash_build_name = {0}'.format(cdash_build_name))
        tty.debug('cdash_site = {0}'.format(cdash_site))
        tty.debug('related_builds = {0}'.format(related_builds))
        tty.debug('job_spec_buildgroup = {0}'.format(job_spec_buildgroup))

    tty.debug('pipeline_artifacts_dir = {0}'.format(pipeline_artifacts_dir))
    tty.debug('root_spec = {0}'.format(root_spec))
    tty.debug('remote_mirror_url = {0}'.format(remote_mirror_url))
    tty.debug('job_spec_pkg_name = {0}'.format(job_spec_pkg_name))
    tty.debug('compiler_action = {0}'.format(compiler_action))

    cdash_report_dir = os.path.join(pipeline_artifacts_dir, 'cdash_report')
    build_cache_dir = os.path.join(local_mirror_dir, 'build_cache')

    spack_is_pr_pipeline = True if pr_env_var == 'True' else False

    pipeline_mirror_url = None
    temp_storage_url_prefix = None
    if 'temporary-storage-url-prefix' in gitlab_ci:
        temp_storage_url_prefix = gitlab_ci['temporary-storage-url-prefix']
        pipeline_mirror_url = url_util.join(
            temp_storage_url_prefix, ci_pipeline_id)

    enable_artifacts_mirror = False
    if 'enable-artifacts-buildcache' in gitlab_ci:
        enable_artifacts_mirror = gitlab_ci['enable-artifacts-buildcache']
        if (enable_artifacts_mirror or (spack_is_pr_pipeline and
            not enable_artifacts_mirror and not temp_storage_url_prefix)):
            # If you explicitly enabled the artifacts buildcache feature, or
            # if this is a PR pipeline but you did not enable either of the
            # per-pipeline temporary storage features, we force the use of
            # artifacts buildcache.  Otherwise jobs will not have binary
            # dependencies from previous stages available since we do not
            # allow pushing binaries to the remote mirror during PR pipelines.
            enable_artifacts_mirror = True
            pipeline_mirror_url = 'file://' + local_mirror_dir
            mirror_msg = 'artifact buildcache enabled, mirror url: {0}'.format(
                pipeline_mirror_url)
            tty.debug(mirror_msg)

    # Clean out cdash reports, logs, specs from last stage
    if os.path.exists(job_log_dir):
        shutil.rmtree(job_log_dir)

    if os.path.exists(repro_dir):
        shutil.rmtree(repro_dir)

    if os.path.exists(cdash_report_dir):
        shutil.rmtree(cdash_report_dir)

    os.makedirs(job_log_dir)
    os.makedirs(repro_dir)

    # Copy the concrete environment files to the repro directory so we can
    # expose them as artifacts and not conflict with the concrete environment
    # files we got as artifacts from the upstream pipeline generation job.
    # Try to cast a slightly wider net too, and hopefully get the generated
    # pipeline yaml.  If we miss it, the user will still be able to go to the
    # pipeline generation job and get it from there.
    target_dirs = [
        concrete_env_dir,
        pipeline_artifacts_dir
    ]

    for dir_to_list in target_dirs:
        for file_name in os.listdir(dir_to_list):
            src_file = os.path.join(dir_to_list, file_name)
            if os.path.isfile(src_file):
                dst_file = os.path.join(repro_dir, file_name)
                shutil.copyfile(src_file, dst_file)

    cdash_build_id = None
    cdash_build_stamp = None

    current_directory = os.getcwd()
    tty.debug('Current working directory: {0}, Contents:'.format(
        current_directory))
    directory_list = os.listdir(current_directory)
    for next_entry in directory_list:
        tty.debug('  {0}'.format(next_entry))

    if signing_key:
        spack_ci.import_signing_key(signing_key)

    can_verify = spack_ci.can_verify_binaries()
    verify_binaries = can_verify and spack_is_pr_pipeline is False

    spack_ci.configure_compilers(compiler_action)

    spec_map = spack_ci.get_concrete_specs(
        env, root_spec, job_spec_pkg_name, related_builds, compiler_action)

    job_spec = spec_map[job_spec_pkg_name]

    job_spec_yaml_file = '{0}.yaml'.format(job_spec_pkg_name)
    job_spec_yaml_path = os.path.join(repro_dir, job_spec_yaml_file)

    tty.debug('job concrete spec path: {0}'.format(job_spec_yaml_path))

    with open(job_spec_yaml_path, 'w') as fd:
        fd.write(job_spec.to_yaml(hash=ht.build_hash))

    tty.debug('Done writing concrete spec')

    # DEBUG
    with open(job_spec_yaml_path) as fd:
        tty.debug('Wrote spec file, read it back.  Contents:')
        tty.debug(fd.read())

    # DEBUG the root spec
    root_spec_yaml_path = os.path.join(repro_dir, 'root.yaml')
    with open(root_spec_yaml_path, 'w') as fd:
        fd.write(spec_map['root'].to_yaml(hash=ht.build_hash))

    # Write some information to aid in reproduction into an artifact
    repro_file = os.path.join(repro_dir, 'repro.json')
    repro_details = {
        'job_name': ci_job_name,
        'job_spec_yaml': job_spec_yaml_file,
        'root_spec_yaml': 'root.yaml'
    }
    with open(repro_file, 'w') as fd:
        fd.write(json.dumps(repro_details))

    # Write information about spack into an artifact
    spack_info = spack_ci.get_spack_info()
    spack_info_file = os.path.join(repro_dir, 'spack_info.txt')
    with open(spack_info_file, 'w') as fd:
        fd.write('\n{0}\n'.format(spack_info))

    if pipeline_mirror_url:
        spack_ci.add_mirror(spack_ci.TEMP_STORAGE_MIRROR_NAME, pipeline_mirror_url)

    # Checks all mirrors for a built spec with a matching full hash
    matches = bindist.get_mirrors_for_spec(
        job_spec, full_hash_match=True, index_only=False)

    if matches:
        # Got at full hash match on at least one configured mirror.  All
        # matches represent the fully up-to-date spec, so should all be
        # equivalent.  If artifacts mirror is enabled, we just pick one
        # of the matches and download the buildcache files from there to
        # the artifacts, so they're available to be used by dependent
        # jobs in subsequent stages.
        install_msg = 'No need to rebuild {0}'.format(job_spec_pkg_name)
        tty.debug('No need to rebuild {0}'.format(job_spec_pkg_name))
        if enable_artifacts_mirror:
            matching_mirror = matches[0]['mirror_url']
            tty.debug('Getting {0} buildcache from {1}'.format(
                job_spec_pkg_name, matching_mirror))
            tty.debug('Downloading to {0}'.format(build_cache_dir))
            buildcache.download_buildcache_files(
                job_spec, build_cache_dir, True, matching_mirror)

        # Write a no-op command to a shell script
        with open('install.sh', 'w') as fd:
            fd.write('#!/bin/bash\n\n')
            fd.write('echo {0}\n'.format(install_msg))
    else:
        # No full hash match anywhere means we need to rebuild spec

        # Build up common install arguments
        install_args = [
            '-d', '-v', '-k', 'install',
            '--keep-stage',
            '--require-full-hash-match',
        ]

        if not verify_binaries:
            install_args.append('--no-check-signature')

        # Add arguments to create + register a new build on CDash (if
        # enabled)
        if enable_cdash:
            tty.debug('Registering build with CDash')
            (cdash_build_id,
                cdash_build_stamp) = spack_ci.register_cdash_build(
                cdash_build_name, cdash_base_url, cdash_project,
                cdash_site, job_spec_buildgroup)

            cdash_upload_url = '{0}/submit.php?project={1}'.format(
                cdash_base_url, cdash_project_enc)

            install_args.extend([
                '--cdash-upload-url', cdash_upload_url,
                '--cdash-build', cdash_build_name,
                '--cdash-site', cdash_site,
                '--cdash-buildstamp', cdash_build_stamp,
            ])

            os.environ['SPACK_CDASH_BUILD_ID'] = cdash_build_id

        # TODO: once we have the concrete spec registry, use the DAG
        # hash to identify the spec to install, rather than the concrete
        # spec yaml file.
        # install_args.extend(['--no-add', '/{0}'.format(spec_dag_hash)])
        install_args.extend(['--no-add', '-f', job_spec_yaml_path])

        tty.debug('Installing {0} from source'.format(job_spec.name))
        tty.debug('spack install arguments: {0}'.format(
            install_args))

        # Write the install command to a shell script
        with open('install.sh', 'w') as fd:
            fd.write('#!/bin/bash\n\n')
            fd.write('\n# spack install command\n')
            fd.write('spack ')
            fd.write(' '.join(['"{0}"'.format(i) for i in install_args]))
            fd.write('\n')

    st = os.stat('install.sh')
    os.chmod('install.sh', st.st_mode | stat.S_IEXEC)

    install_copy_path = os.path.join(repro_dir, 'install.sh')
    shutil.copyfile('install.sh', install_copy_path)


def ci_postbuild(args):
    tty.debug('spack install exited {0}'.format(
        os.environ.get('SPACK_INSTALL_EXIT_ERROR')))

    env = ev.get_env(args, 'ci prebuild', required=True)

    yaml_root = ev.config_dict(env.yaml)
    gitlab_ci = yaml_root['gitlab-ci']

    job_log_dir = get_env_var('SPACK_JOB_LOG_DIR')
    repro_dir = get_env_var('SPACK_JOB_REPRO_DIR')
    ci_pipeline_id = get_env_var('CI_PIPELINE_ID')
    root_spec = get_env_var('SPACK_ROOT_SPEC')
    job_spec_pkg_name = get_env_var('SPACK_JOB_SPEC_PKG_NAME')
    compiler_action = get_env_var('SPACK_COMPILER_ACTION')
    pr_env_var = get_env_var('SPACK_IS_PR_PIPELINE')
    dev_env_var = get_env_var('SPACK_IS_DEVELOP_PIPELINE')
    pr_mirror_url = get_env_var('SPACK_PR_MIRROR_URL')
    related_builds = get_env_var('SPACK_RELATED_BUILDS_CDASH')
    remote_mirror_url = get_env_var('SPACK_REMOTE_MIRROR_URL')

    install_exit_code = int(os.environ.get('SPACK_INSTALL_EXIT_ERROR', 0))

    tty.debug('coerced exit code {0}'.format(install_exit_code))

    spack_is_pr_pipeline = True if pr_env_var == 'True' else False
    spack_is_develop_pipeline = True if dev_env_var == 'True' else False

    spec_map = spack_ci.get_concrete_specs(
        env, root_spec, job_spec_pkg_name, related_builds, compiler_action)

    job_spec_yaml_path = os.path.join(
        repro_dir, '{0}.yaml'.format(job_spec_pkg_name))

    with open(job_spec_yaml_path) as fd:
        job_spec = spack_spec.Spec.from_yaml(fd.read())

    # If a spec fails to build in a spack develop pipeline, we add it to a
    # list of known broken full hashes.  This allows spack PR pipelines to
    # avoid wasting compute cycles attempting to build those hashes.
    if install_exit_code != 0 and spack_is_develop_pipeline:
        if 'broken-specs-url' in gitlab_ci:
            broken_specs_url = gitlab_ci['broken-specs-url']
            dev_fail_hash = job_spec.full_hash()
            broken_spec_path = url_util.join(broken_specs_url, dev_fail_hash)
            tmpdir = tempfile.mkdtemp()
            empty_file_path = os.path.join(tmpdir, 'empty.txt')

            try:
                with open(empty_file_path, 'w') as efd:
                    efd.write('')
                web_util.push_to_url(
                    empty_file_path,
                    broken_spec_path,
                    keep_original=False,
                    extra_args={'ContentType': 'text/plain'})
            except Exception as err:
                # If we got some kind of S3 (access denied or other connection
                # error), the first non boto-specific class in the exception
                # hierarchy is Exception.  Just print a warning and return
                msg = 'Error writing to broken specs list {0}: {1}'.format(
                    broken_spec_path, err)
                tty.warn(msg)
            finally:
                shutil.rmtree(tmpdir)

    spack_ci.copy_stage_logs_to_artifacts(job_spec, job_log_dir)

    pipeline_mirror_url = None
    temp_storage_url_prefix = None
    if 'temporary-storage-url-prefix' in gitlab_ci:
        temp_storage_url_prefix = gitlab_ci['temporary-storage-url-prefix']
        pipeline_mirror_url = url_util.join(
            temp_storage_url_prefix, ci_pipeline_id)

    cdash_build_id = get_env_var('SPACK_CDASH_BUILD_ID')
    if cdash_build_id:
        related_builds = get_env_var('SPACK_RELATED_BUILDS_CDASH')
        ci_cdash = yaml_root['cdash']
        cdash_base_url = ci_cdash['url']
        cdash_project = ci_cdash['project']

    # Create buildcache on remote mirror, either on pr-specific
    # mirror or on mirror defined in spack environment
    if spack_is_pr_pipeline:
        buildcache_mirror_url = pr_mirror_url
    else:
        buildcache_mirror_url = remote_mirror_url

    if install_exit_code == 0:
        can_sign = spack_ci.can_sign_binaries()
        sign_binaries = can_sign and spack_is_pr_pipeline is False

        # Create buildcache in either the main remote mirror, or in the
        # per-PR mirror, if this is a PR pipeline
        spack_ci.push_mirror_contents(
            env, job_spec, job_spec_yaml_path, buildcache_mirror_url,
            cdash_build_id, sign_binaries)

        # Create another copy of that buildcache in the per-pipeline
        # temporary storage mirror (this is only done if either artifacts
        # buildcache is enabled or a temporary storage url prefix is set)
        spack_ci.push_mirror_contents(
            env, job_spec, job_spec_yaml_path, pipeline_mirror_url,
            cdash_build_id, sign_binaries)
    else:
        tty.debug('spack install exited non-zero, will not create buildcache')

        api_root_url = get_env_var('CI_API_V4_URL')
        ci_project_id = get_env_var('CI_PROJECT_ID')
        ci_job_id = get_env_var('CI_JOB_ID')

        repro_job_url = '{0}/projects/{1}/jobs/{2}/artifacts'.format(
            api_root_url, ci_project_id, ci_job_id)

        reproduce_msg = """

To reproduce this build locally, run:

  spack ci reproduce-build {0} [--working-dir <dir>]

If this project does not have public pipelines, you will need to first:

  export GITLAB_PRIVATE_TOKEN=<generated_token>

... then follow the printed instructions.

""".format(repro_job_url)

        print(reproduce_msg)

    # Relate this build to its dependencies on CDash (if enabled)
    if cdash_build_id:
        spack_ci.relate_cdash_builds(
            spec_map, cdash_base_url, cdash_build_id, cdash_project,
            pipeline_mirror_url or pr_mirror_url or remote_mirror_url)

    sys.exit(install_exit_code)


def ci_reproduce(args):
    job_url = args.job_url
    work_dir = args.working_dir

    spack_ci.reproduce_ci_job(job_url, work_dir)


def ci(parser, args):
    if args.func:
        args.func(args)
