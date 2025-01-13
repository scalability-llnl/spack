# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import copy
import os
import shutil
from typing import List, Optional

import ruamel.yaml

import llnl.util.tty as tty

import spack
import spack.binary_distribution as bindist
import spack.config as cfg
import spack.mirrors.mirror
import spack.schema
import spack.spec
import spack.util.spack_yaml as syaml

from .common import (
    SPACK_RESERVED_TAGS,
    PipelineDag,
    PipelineOptions,
    PipelineType,
    SpackCIConfig,
    SpackCIError,
    ensure_expected_target_path,
    unpack_script,
    update_env_scopes,
    write_pipeline_manifest,
)
from .generator_registry import generator

# See https://docs.gitlab.com/ee/ci/yaml/#retry for descriptions of conditions
JOB_RETRY_CONDITIONS = [
    # "always",
    "unknown_failure",
    "script_failure",
    "api_failure",
    "stuck_or_timeout_failure",
    "runner_system_failure",
    "runner_unsupported",
    "stale_schedule",
    # "job_execution_timeout",
    "archived_failure",
    "unmet_prerequisites",
    "scheduler_failure",
    "data_integrity_failure",
]
JOB_NAME_FORMAT = "{name}{@version} {/hash}"


def _remove_reserved_tags(tags):
    """Convenience function to strip reserved tags from jobs"""
    return [tag for tag in tags if tag not in SPACK_RESERVED_TAGS]


def get_job_name(spec: spack.spec.Spec, build_group: Optional[str] = None) -> str:
    """Given a spec and possibly a build group, return the job name. If the
    resulting name is longer than 255 characters, it will be truncated.

    Arguments:
        spec: Spec job will build
        build_group: Name of build group this job belongs to (a CDash notion)

    Returns: The job name
    """
    job_name = spec.format(JOB_NAME_FORMAT)

    if build_group:
        job_name = f"{job_name} {build_group}"

    return job_name[:255]


def maybe_generate_manifest(pipeline: PipelineDag, options: PipelineOptions, manifest_path):
    # TODO: Consider including only hashes of rebuilt specs in the manifest,
    # instead of full source and destination urls.  Also, consider renaming
    # the variable that controls whether or not to write the manifest from
    # "SPACK_COPY_BUILDCACHE" to "SPACK_WRITE_PIPELINE_MANIFEST" or similar.
    spack_buildcache_copy = os.environ.get("SPACK_COPY_BUILDCACHE", None)
    if spack_buildcache_copy:
        buildcache_copy_src_prefix = options.buildcache_destination.fetch_url
        buildcache_copy_dest_prefix = spack_buildcache_copy

        if options.pipeline_type == PipelineType.COPY_ONLY:
            manifest_specs = [s for s in options.env.all_specs() if not s.external]
        else:
            manifest_specs = [n.spec for _, n in pipeline.traverse_nodes(direction="children")]

        write_pipeline_manifest(
            manifest_specs, buildcache_copy_src_prefix, buildcache_copy_dest_prefix, manifest_path
        )


@generator("gitlab")
def generate_gitlab_yaml(pipeline: PipelineDag, spack_ci: SpackCIConfig, options: PipelineOptions):
    """Given a pipeline graph, job attributes, and pipeline options,
    write a pipeline that can be consumed by GitLab to the given output file.

    Arguments:
        pipeline: An already pruned graph of jobs representing all the specs to build
        spack_ci: An object containing the configured attributes of all jobs in the pipeline
        options: An object containing all the pipeline options gathered from yaml, env, etc...
    """
    ci_project_dir = os.environ.get("CI_PROJECT_DIR") or os.getcwd()
    generate_job_name = os.environ.get("CI_JOB_NAME", "job-does-not-exist")
    generate_pipeline_id = os.environ.get("CI_PIPELINE_ID", "pipeline-does-not-exist")
    artifacts_root = options.artifacts_root
    if artifacts_root.startswith(ci_project_dir):
        artifacts_root = os.path.relpath(artifacts_root, ci_project_dir)
    pipeline_artifacts_dir = os.path.join(ci_project_dir, artifacts_root)
    output_file = options.output_file

    if not output_file:
        output_file = os.path.abspath(".gitlab-ci.yml")
    else:
        output_file_path = os.path.abspath(output_file)
        gen_ci_dir = os.path.dirname(output_file_path)
        if not os.path.exists(gen_ci_dir):
            os.makedirs(gen_ci_dir)

    spack_ci_ir = spack_ci.generate_ir()

    concrete_env_dir = os.path.join(pipeline_artifacts_dir, "concrete_environment")

    # Now that we've added the mirrors we know about, they should be properly
    # reflected in the environment manifest file, so copy that into the
    # concrete environment directory, along with the spack.lock file.
    if not os.path.exists(concrete_env_dir):
        os.makedirs(concrete_env_dir)
    shutil.copyfile(options.env.manifest_path, os.path.join(concrete_env_dir, "spack.yaml"))
    shutil.copyfile(options.env.lock_path, os.path.join(concrete_env_dir, "spack.lock"))

    update_env_scopes(
        options.env,
        [
            os.path.relpath(s.path, concrete_env_dir)
            for s in cfg.scopes().values()
            if not s.writable
            and isinstance(s, (cfg.DirectoryConfigScope))
            and os.path.exists(s.path)
        ],
        os.path.join(concrete_env_dir, "spack.yaml"),
        # Here transforming windows paths is only required in the special case
        # of copy_only_pipelines, a unique scenario where the generate job and
        # child pipelines are run on different platforms. To make this compatible
        # w/ Windows, we cannot write Windows style path separators that will be
        # consumed on by the Posix copy job runner.
        #
        # TODO (johnwparent): Refactor config + cli read/write to deal only in
        # posix style paths
        transform_windows_paths=(options.pipeline_type == PipelineType.COPY_ONLY),
    )

    job_log_dir = os.path.join(pipeline_artifacts_dir, "logs")
    job_repro_dir = os.path.join(pipeline_artifacts_dir, "reproduction")
    job_test_dir = os.path.join(pipeline_artifacts_dir, "tests")
    user_artifacts_dir = os.path.join(pipeline_artifacts_dir, "user_data")

    # We communicate relative paths to the downstream jobs to avoid issues in
    # situations where the CI_PROJECT_DIR varies between the pipeline
    # generation job and the rebuild jobs.  This can happen when gitlab
    # checks out the project into a runner-specific directory, for example,
    # and different runners are picked for generate and rebuild jobs.

    rel_concrete_env_dir = os.path.relpath(concrete_env_dir, ci_project_dir)
    rel_job_log_dir = os.path.relpath(job_log_dir, ci_project_dir)
    rel_job_repro_dir = os.path.relpath(job_repro_dir, ci_project_dir)
    rel_job_test_dir = os.path.relpath(job_test_dir, ci_project_dir)
    rel_user_artifacts_dir = os.path.relpath(user_artifacts_dir, ci_project_dir)

    def main_script_replacements(cmd):
        return cmd.replace("{env_dir}", rel_concrete_env_dir)

    output_object = {}
    job_id = 0
    stage_id = 0
    stages: List[List] = []
    stage_names = []

    max_length_needs = 0
    max_needs_job = ""

    if not options.pipeline_type == PipelineType.COPY_ONLY:
        for level, node in pipeline.traverse_nodes(direction="parents"):
            stage_id = level
            if len(stages) == stage_id:
                stages.append([])
            stages[stage_id].append(node.spec)
            stage_name = f"stage-{level}"

            if stage_name not in stage_names:
                stage_names.append(stage_name)

            release_spec = node.spec
            release_spec_dag_hash = release_spec.dag_hash()

            job_object = spack_ci_ir["jobs"][release_spec_dag_hash]["attributes"]

            if not job_object:
                tty.warn(f"No match found for {release_spec}, skipping it")
                continue

            if options.pipeline_type is not None:
                # For spack pipelines "public" and "protected" are reserved tags
                job_object["tags"] = _remove_reserved_tags(job_object.get("tags", []))
                if options.pipeline_type == PipelineType.PROTECTED_BRANCH:
                    job_object["tags"].extend(["protected"])
                elif options.pipeline_type == PipelineType.PULL_REQUEST:
                    job_object["tags"].extend(["public"])

            if "script" not in job_object:
                raise AttributeError

            job_object["script"] = unpack_script(job_object["script"], op=main_script_replacements)

            if "before_script" in job_object:
                job_object["before_script"] = unpack_script(job_object["before_script"])

            if "after_script" in job_object:
                job_object["after_script"] = unpack_script(job_object["after_script"])

            build_group = options.cdash_handler.build_group if options.cdash_handler else None
            job_name = get_job_name(release_spec, build_group)

            dep_nodes = pipeline.get_dependencies(node)
            job_object["needs"] = [
                {"job": get_job_name(dep_node.spec, build_group), "artifacts": False}
                for dep_node in dep_nodes
            ]

            job_object["needs"].append(
                {"job": generate_job_name, "pipeline": f"{generate_pipeline_id}"}
            )

            job_vars = job_object["variables"]

            # Let downstream jobs know whether the spec needed rebuilding, regardless
            # whether DAG pruning was enabled or not.
            already_built = bindist.get_mirrors_for_spec(spec=release_spec, index_only=True)
            job_vars["SPACK_SPEC_NEEDS_REBUILD"] = "False" if already_built else "True"

            if options.cdash_handler:
                build_name = options.cdash_handler.build_name(release_spec)
                job_vars["SPACK_CDASH_BUILD_NAME"] = build_name
                build_stamp = options.cdash_handler.build_stamp
                job_vars["SPACK_CDASH_BUILD_STAMP"] = build_stamp

            job_object["artifacts"] = spack.schema.merge_yaml(
                job_object.get("artifacts", {}),
                {
                    "when": "always",
                    "paths": [
                        rel_job_log_dir,
                        rel_job_repro_dir,
                        rel_job_test_dir,
                        rel_user_artifacts_dir,
                    ],
                },
            )

            job_object["stage"] = stage_name
            job_object["retry"] = {"max": 2, "when": JOB_RETRY_CONDITIONS}
            job_object["interruptible"] = True

            length_needs = len(job_object["needs"])
            if length_needs > max_length_needs:
                max_length_needs = length_needs
                max_needs_job = job_name

            output_object[job_name] = job_object
            job_id += 1

        tty.debug(f"{job_id} build jobs generated in {stage_id} stages")

    if job_id > 0:
        tty.debug(f"The max_needs_job is {max_needs_job}, with {max_length_needs} needs")

    service_job_retries = {
        "max": 2,
        "when": ["runner_system_failure", "stuck_or_timeout_failure", "script_failure"],
    }

    # In some cases, pipeline generation should write a manifest.  Currently
    # the only purpose is to specify a list of sources and destinations for
    # everything that should be copied.
    distinguish_stack = options.stack_name if options.stack_name else "rebuilt"
    manifest_path = os.path.join(
        pipeline_artifacts_dir, "specs_to_copy", f"copy_{distinguish_stack}_specs.json"
    )
    maybe_generate_manifest(pipeline, options, manifest_path)

    if options.pipeline_type == PipelineType.COPY_ONLY:
        stage_names.append("copy")
        sync_job = copy.deepcopy(spack_ci_ir["jobs"]["copy"]["attributes"])
        sync_job["stage"] = "copy"
        sync_job["needs"] = [{"job": generate_job_name, "pipeline": f"{generate_pipeline_id}"}]

        if "variables" not in sync_job:
            sync_job["variables"] = {}

        sync_job["variables"][
            "SPACK_COPY_ONLY_DESTINATION"
        ] = options.buildcache_destination.fetch_url

        pipeline_mirrors = spack.mirrors.mirror.MirrorCollection(binary=True)
        if "buildcache-source" not in pipeline_mirrors:
            raise SpackCIError("Copy-only pipelines require a mirror named 'buildcache-source'")

        buildcache_source = pipeline_mirrors["buildcache-source"].fetch_url
        sync_job["variables"]["SPACK_BUILDCACHE_SOURCE"] = buildcache_source
        sync_job["dependencies"] = []

        output_object["copy"] = sync_job
        job_id += 1

    if job_id > 0:
        if (
            "script" in spack_ci_ir["jobs"]["signing"]["attributes"]
            and options.pipeline_type == PipelineType.PROTECTED_BRANCH
        ):
            # External signing: generate a job to check and sign binary pkgs
            stage_names.append("stage-sign-pkgs")
            signing_job = spack_ci_ir["jobs"]["signing"]["attributes"]

            signing_job["script"] = unpack_script(signing_job["script"])

            signing_job["stage"] = "stage-sign-pkgs"
            signing_job["when"] = "always"
            signing_job["retry"] = {"max": 2, "when": ["always"]}
            signing_job["interruptible"] = True
            if "variables" not in signing_job:
                signing_job["variables"] = {}
            signing_job["variables"][
                "SPACK_BUILDCACHE_DESTINATION"
            ] = options.buildcache_destination.push_url
            signing_job["dependencies"] = []

            output_object["sign-pkgs"] = signing_job

        if options.rebuild_index:
            # Add a final job to regenerate the index
            stage_names.append("stage-rebuild-index")
            final_job = spack_ci_ir["jobs"]["reindex"]["attributes"]

            final_job["stage"] = "stage-rebuild-index"
            target_mirror = options.buildcache_destination.push_url
            final_job["script"] = unpack_script(
                final_job["script"],
                op=lambda cmd: cmd.replace("{index_target_mirror}", target_mirror),
            )

            final_job["when"] = "always"
            final_job["retry"] = service_job_retries
            final_job["interruptible"] = True
            final_job["dependencies"] = []

            output_object["rebuild-index"] = final_job

        output_object["stages"] = stage_names

        # Capture the version of Spack used to generate the pipeline, that can be
        # passed to `git checkout` for version consistency. If we aren't in a Git
        # repository, presume we are a Spack release and use the Git tag instead.
        spack_version = spack.get_version()
        version_to_clone = spack.get_spack_commit() or f"v{spack.spack_version}"

        rebuild_everything = not options.prune_up_to_date and not options.prune_untouched

        output_object["variables"] = {
            "SPACK_ARTIFACTS_ROOT": artifacts_root,
            "SPACK_CONCRETE_ENV_DIR": rel_concrete_env_dir,
            "SPACK_VERSION": spack_version,
            "SPACK_CHECKOUT_VERSION": version_to_clone,
            "SPACK_JOB_LOG_DIR": rel_job_log_dir,
            "SPACK_JOB_REPRO_DIR": rel_job_repro_dir,
            "SPACK_JOB_TEST_DIR": rel_job_test_dir,
            "SPACK_PIPELINE_TYPE": options.pipeline_type.name if options.pipeline_type else "None",
            "SPACK_CI_STACK_NAME": os.environ.get("SPACK_CI_STACK_NAME", "None"),
            "SPACK_REBUILD_CHECK_UP_TO_DATE": str(options.prune_up_to_date),
            "SPACK_REBUILD_EVERYTHING": str(rebuild_everything),
            "SPACK_REQUIRE_SIGNING": str(options.require_signing),
        }

        if options.stack_name:
            output_object["variables"]["SPACK_CI_STACK_NAME"] = options.stack_name

        output_vars = output_object["variables"]
        for item, val in output_vars.items():
            output_vars[item] = ensure_expected_target_path(val)

    else:
        # No jobs were generated
        noop_job = spack_ci_ir["jobs"]["noop"]["attributes"]
        # If this job fails ignore the status and carry on
        noop_job["retry"] = 0
        noop_job["allow_failure"] = True

        tty.debug("No specs to rebuild, generating no-op job")
        output_object = {"no-specs-to-rebuild": noop_job}

    # Ensure the child pipeline always runs
    output_object["workflow"] = {"rules": [{"when": "always"}]}

    sorted_output = {}
    for output_key, output_value in sorted(output_object.items()):
        sorted_output[output_key] = output_value

    # Minimize yaml output size through use of anchors
    syaml.anchorify(sorted_output)

    with open(output_file, "w", encoding="utf-8") as f:
        ruamel.yaml.YAML().dump(sorted_output, f)
