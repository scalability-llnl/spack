# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil
import sys

from six.moves.urllib.parse import urlencode

import llnl.util.tty as tty

import spack.binary_distribution as bindist
import spack.ci as spack_ci
import spack.cmd.buildcache as buildcache
import spack.environment as ev
import spack.hash_types as ht
import spack.util.executable as exe
import spack.util.url as url_util


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
    generate.set_defaults(func=ci_generate)

    # Check a spec against mirror. Rebuild, create buildcache and push to
    # mirror (if necessary).
    rebuild = subparsers.add_parser('rebuild', help=ci_rebuild.__doc__)
    rebuild.set_defaults(func=ci_rebuild)

    # Rebuild the buildcache index associated with the mirror in the
    # active, gitlab-enabled environment.
    index = subparsers.add_parser('rebuild-index', help=ci_reindex.__doc__)
    index.set_defaults(func=ci_reindex)


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
        use_dependencies=use_dependencies)

    if copy_yaml_to:
        copy_to_dir = os.path.dirname(copy_yaml_to)
        if not os.path.exists(copy_to_dir):
            os.makedirs(copy_to_dir)
        shutil.copyfile(output_file, copy_yaml_to)


def ci_rebuild(args):
    """This command represents a gitlab-ci job, corresponding to a single
       release spec.  As such it must first decide whether or not the spec it
       has been assigned to build is up to date on the remote binary mirror.
       If it is not (i.e. the full_hash of the spec as computed locally does
       not match the one stored in the metadata on the mirror), this script
       will build the package, create a binary cache for it, and then push all
       related files to the remote binary mirror.  This script also
       communicates with a remote CDash instance to share status on the package
       build process.

       The spec to be built by this job is represented by essentially two
       pieces of information: 1) a root spec (possibly already concrete, but
       maybe still needing to be concretized) and 2) a package name used to
       index that root spec (once the root is, for certain, concrete)."""
    env = ev.get_env(args, 'ci rebuild', required=True)
    yaml_root = ev.config_dict(env.yaml)

    # The following environment variables should defined in the CI
    # infrastructre (or some other external source) in the case that the
    # remote mirror is an S3 bucket.  The AWS keys are used to upload
    # buildcache entries to S3 using the boto3 api.
    #
    # AWS_ACCESS_KEY_ID
    # AWS_SECRET_ACCESS_KEY
    # S3_ENDPOINT_URL (only needed for non-AWS S3 implementations)
    #
    # If present, we will import the  SPACK_SIGNING_KEY using the
    # "spack gpg trust" command, so it can be used both for verifying
    # dependency buildcache entries and signing the buildcache entry we create
    # for our target pkg.
    #
    # SPACK_SIGNING_KEY

    ci_artifact_dir = get_env_var('CI_PROJECT_DIR')
    ci_pipeline_id = get_env_var('CI_PIPELINE_ID')
    signing_key = get_env_var('SPACK_SIGNING_KEY')
    root_spec = get_env_var('SPACK_ROOT_SPEC')
    job_spec_pkg_name = get_env_var('SPACK_JOB_SPEC_PKG_NAME')
    compiler_action = get_env_var('SPACK_COMPILER_ACTION')
    cdash_build_name = get_env_var('SPACK_CDASH_BUILD_NAME')
    related_builds = get_env_var('SPACK_RELATED_BUILDS_CDASH')
    pr_env_var = get_env_var('SPACK_IS_PR_PIPELINE')
    pr_mirror_url = get_env_var('SPACK_PR_MIRROR_URL')

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

    remote_mirror_url = None
    if 'mirrors' in yaml_root:
        ci_mirrors = yaml_root['mirrors']
        mirror_urls = [url for url in ci_mirrors.values()]
        remote_mirror_url = mirror_urls[0]

    if not remote_mirror_url:
        tty.die('spack ci rebuild requires an env containing a mirror')

    tty.debug('ci_artifact_dir = {0}'.format(ci_artifact_dir))
    tty.debug('root_spec = {0}'.format(root_spec))
    tty.debug('remote_mirror_url = {0}'.format(remote_mirror_url))
    tty.debug('job_spec_pkg_name = {0}'.format(job_spec_pkg_name))
    tty.debug('compiler_action = {0}'.format(compiler_action))

    cdash_report_dir = os.path.join(ci_artifact_dir, 'cdash_report')
    temp_dir = os.path.join(ci_artifact_dir, 'jobs_scratch_dir')
    job_log_dir = os.path.join(temp_dir, 'logs')
    spec_dir = os.path.join(temp_dir, 'specs')

    local_mirror_dir = os.path.join(ci_artifact_dir, 'local_mirror')
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

    # Clean out scratch directory from last stage
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    if os.path.exists(cdash_report_dir):
        shutil.rmtree(cdash_report_dir)

    os.makedirs(job_log_dir)
    os.makedirs(spec_dir)

    job_spec_yaml_path = os.path.join(
        spec_dir, '{0}.yaml'.format(job_spec_pkg_name))
    job_log_file = os.path.join(job_log_dir, 'pipeline_log.txt')

    cdash_build_id = None
    cdash_build_stamp = None

    with open(job_log_file, 'w') as log_fd:
        os.dup2(log_fd.fileno(), sys.stdout.fileno())
        os.dup2(log_fd.fileno(), sys.stderr.fileno())

        current_directory = os.getcwd()
        tty.debug('Current working directory: {0}, Contents:'.format(
            current_directory))
        directory_list = os.listdir(current_directory)
        for next_entry in directory_list:
            tty.debug('  {0}'.format(next_entry))

        tty.debug('job concrete spec path: {0}'.format(job_spec_yaml_path))

        if signing_key:
            spack_ci.import_signing_key(signing_key)

        can_sign = spack_ci.can_sign_binaries()
        sign_binaries = can_sign and spack_is_pr_pipeline is False

        can_verify = spack_ci.can_verify_binaries()
        verify_binaries = can_verify and spack_is_pr_pipeline is False

        spack_ci.configure_compilers(compiler_action)

        spec_map = spack_ci.get_concrete_specs(
            root_spec, job_spec_pkg_name, related_builds, compiler_action)

        job_spec = spec_map[job_spec_pkg_name]

        tty.debug('Here is the concrete spec: {0}'.format(job_spec))

        with open(job_spec_yaml_path, 'w') as fd:
            fd.write(job_spec.to_yaml(hash=ht.build_hash))

        tty.debug('Done writing concrete spec')

        # DEBUG
        with open(job_spec_yaml_path) as fd:
            tty.debug('Wrote spec file, read it back.  Contents:')
            tty.debug(fd.read())

        # DEBUG the root spec
        root_spec_yaml_path = os.path.join(spec_dir, 'root.yaml')
        with open(root_spec_yaml_path, 'w') as fd:
            fd.write(spec_map['root'].to_yaml(hash=ht.build_hash))

        # TODO: Refactor the spack install command so it's easier to use from
        # python modules.  Currently we use "exe.which('spack')" to make it
        # easier to install packages from here, but it introduces some
        # problems, e.g. if we want the spack command to have access to the
        # mirrors we're configuring, then we have to use the "spack" command
        # to add the mirrors too, which in turn means that any code here *not*
        # using the spack command does *not* have access to the mirrors.
        spack_cmd = exe.which('spack')
        mirrors_to_check = {
            'ci_remote_mirror': remote_mirror_url,
        }

        def add_mirror(mirror_name, mirror_url):
            m_args = ['mirror', 'add', mirror_name, mirror_url]
            tty.debug('Adding mirror: spack {0}'.format(m_args))
            mirror_add_output = spack_cmd(*m_args)
            # Workaround: Adding the mirrors above, using "spack_cmd" makes
            # sure they're available later when we use "spack_cmd" to install
            # the package.  But then we also need to add them to this dict
            # below, so they're available in this process (we end up having to
            # pass them to "bindist.get_mirrors_for_spec()")
            mirrors_to_check[mirror_name] = mirror_url
            tty.debug('spack mirror add output: {0}'.format(mirror_add_output))

        # Configure mirrors
        if pr_mirror_url:
            add_mirror('ci_pr_mirror', pr_mirror_url)

        if pipeline_mirror_url:
            add_mirror(spack_ci.TEMP_STORAGE_MIRROR_NAME, pipeline_mirror_url)

        tty.debug('listing spack mirrors:')
        spack_cmd('mirror', 'list')
        spack_cmd('config', 'blame', 'mirrors')

        # Checks all mirrors for a built spec with a matching full hash
        matches = bindist.get_mirrors_for_spec(
            job_spec, full_hash_match=True, mirrors_to_check=mirrors_to_check,
            index_only=False)

        if matches:
            # Got at full hash match on at least one configured mirror.  All
            # matches represent the fully up-to-date spec, so should all be
            # equivalent.  If artifacts mirror is enabled, we just pick one
            # of the matches and download the buildcache files from there to
            # the artifacts, so they're available to be used by dependent
            # jobs in subsequent stages.
            tty.debug('No need to rebuild {0}'.format(job_spec_pkg_name))
            if enable_artifacts_mirror:
                matching_mirror = matches[0]['mirror_url']
                tty.debug('Getting {0} buildcache from {1}'.format(
                    job_spec_pkg_name, matching_mirror))
                tty.debug('Downloading to {0}'.format(build_cache_dir))
                buildcache.download_buildcache_files(
                    job_spec, build_cache_dir, True, matching_mirror)
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

            install_args.append(job_spec_yaml_path)

            tty.debug('Installing {0} from source'.format(job_spec.name))

            try:
                tty.debug('spack install arguments: {0}'.format(
                    install_args))
                spack_cmd(*install_args)
            finally:
                spack_ci.copy_stage_logs_to_artifacts(job_spec, job_log_dir)

            # Create buildcache on remote mirror, either on pr-specific
            # mirror or on mirror defined in spack environment
            if spack_is_pr_pipeline:
                buildcache_mirror_url = pr_mirror_url
            else:
                buildcache_mirror_url = remote_mirror_url

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

            # Relate this build to its dependencies on CDash (if enabled)
            if enable_cdash:
                spack_ci.relate_cdash_builds(
                    spec_map, cdash_base_url, cdash_build_id, cdash_project,
                    pipeline_mirror_url or pr_mirror_url or remote_mirror_url)


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


def ci(parser, args):
    if args.func:
        args.func(args)
