# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import base64
import codecs
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile
from collections import namedtuple
from typing import Callable, Dict, List, Set
from urllib.error import HTTPError, URLError
from urllib.request import HTTPHandler, Request, build_opener

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.tty.color import cescape, colorize

import spack
import spack.binary_distribution as bindist
import spack.builder
import spack.concretize
import spack.config as cfg
import spack.environment as ev
import spack.error
import spack.main
import spack.mirrors.mirror
import spack.paths
import spack.repo
import spack.spec
import spack.util.git
import spack.util.gpg as gpg_util
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.util.web as web_util
from spack import traverse
from spack.error import SpackError
from spack.reporters.cdash import SPACK_CDASH_TIMEOUT

from .common import (
    IS_WINDOWS,
    CDashHandler,
    PipelineDag,
    PipelineOptions,
    PipelineType,
    SpackCIConfig,
    SpackCIError,
    copy_files_to_artifacts,
)
from .generator_registry import UnknownGeneratorException, get_generator

# Import any modules with generator functions from here, so they get
# registered without introducing any import cycles.
from .gitlab import generate_gitlab_yaml  # noqa: F401

spack_gpg = spack.main.SpackCommand("gpg")
spack_compiler = spack.main.SpackCommand("compiler")

PushResult = namedtuple("PushResult", "success url")


def get_change_revisions():
    """If this is a git repo get the revisions to use when checking
    for changed packages and spack core modules."""
    git_dir = os.path.join(spack.paths.prefix, ".git")
    if os.path.exists(git_dir) and os.path.isdir(git_dir):
        # TODO: This will only find changed packages from the last
        # TODO: commit.  While this may work for single merge commits
        # TODO: when merging the topic branch into the base, it will
        # TODO: require more thought outside of that narrow case.
        return "HEAD^", "HEAD"
    return None, None


def get_stack_changed(env_path, rev1="HEAD^", rev2="HEAD"):
    """Given an environment manifest path and two revisions to compare, return
    whether or not the stack was changed.  Returns True if the environment
    manifest changed between the provided revisions (or additionally if the
    `.gitlab-ci.yml` file itself changed).  Returns False otherwise."""
    git = spack.util.git.git()
    if git:
        with fs.working_dir(spack.paths.prefix):
            git_log = git(
                "diff",
                "--name-only",
                rev1,
                rev2,
                output=str,
                error=os.devnull,
                fail_on_error=False,
            ).strip()
            lines = [] if not git_log else re.split(r"\s+", git_log)

            for path in lines:
                if ".gitlab-ci.yml" in path or path in env_path:
                    tty.debug(f"env represented by {env_path} changed")
                    tty.debug(f"touched file: {path}")
                    return True
    return False


def compute_affected_packages(rev1="HEAD^", rev2="HEAD"):
    """Determine which packages were added, removed or changed
    between rev1 and rev2, and return the names as a set"""
    return spack.repo.get_all_package_diffs("ARC", rev1=rev1, rev2=rev2)


def get_spec_filter_list(env, affected_pkgs, dependent_traverse_depth=None):
    """Given a list of package names and an active/concretized
       environment, return the set of all concrete specs from the
       environment that could have been affected by changing the
       list of packages.

       If a ``dependent_traverse_depth`` is given, it is used to limit
       upward (in the parent direction) traversal of specs of touched
       packages.  E.g. if 1 is provided, then only direct dependents
       of touched package specs are traversed to produce specs that
       could have been affected by changing the package, while if 0 is
       provided, only the changed specs themselves are traversed. If ``None``
       is given, upward traversal of touched package specs is done all
       the way to the environment roots.  Providing a negative number
       results in no traversals at all, yielding an empty set.

    Arguments:

        env (spack.environment.Environment): Active concrete environment
        affected_pkgs (List[str]): Affected package names
        dependent_traverse_depth: Optional integer to limit dependent
            traversal, or None to disable the limit.

    Returns:

        A set of concrete specs from the active environment including
        those associated with affected packages, their dependencies and
        dependents, as well as their dependents dependencies.
    """
    affected_specs = set()
    all_concrete_specs = env.all_specs()
    tty.debug("All concrete environment specs:")
    for s in all_concrete_specs:
        tty.debug(f"  {s.name}/{s.dag_hash()[:7]}")
    affected_pkgs = frozenset(affected_pkgs)
    env_matches = [s for s in all_concrete_specs if s.name in affected_pkgs]
    visited = set()
    dag_hash = lambda s: s.dag_hash()
    for depth, parent in traverse.traverse_nodes(
        env_matches, direction="parents", key=dag_hash, depth=True, order="breadth"
    ):
        if dependent_traverse_depth is not None and depth > dependent_traverse_depth:
            break
        affected_specs.update(parent.traverse(direction="children", visited=visited, key=dag_hash))
    return affected_specs


# Pruning functions should take a spack.spec.Spec object and
# return a RebuildDecision containg the pruners opinion on
# whether or not to keep (rebuild) the spec and a message
# containing the reason for the decision.


class RebuildDecision:
    def __init__(self, rebuild: bool = True, reason: str = ""):
        self.rebuild = rebuild
        self.reason = reason


def create_unaffected_pruner(
    affected_specs: Set[spack.spec.Spec],
) -> Callable[[spack.spec.Spec], RebuildDecision]:
    """Given a set of "affected" specs, return a filter that prunes specs
    not in the set."""

    def rebuild_filter(s: spack.spec.Spec) -> RebuildDecision:
        if s in affected_specs:
            return RebuildDecision(True, "affected by change")
        return RebuildDecision(False, "unaffected by change")

    return rebuild_filter


def create_already_built_pruner(
    check_index_only: bool = True,
) -> Callable[[spack.spec.Spec], RebuildDecision]:
    """Return a filter that prunes specs already present on any configured
    mirrors"""
    try:
        bindist.BINARY_INDEX.update()
    except bindist.FetchCacheError as e:
        tty.warn(e)

    def rebuild_filter(s: spack.spec.Spec) -> RebuildDecision:
        spec_locations = bindist.get_mirrors_for_spec(spec=s, index_only=check_index_only)

        if not spec_locations:
            return RebuildDecision(True, "not found anywhere")

        urls = ",".join([loc["mirror_url"] for loc in spec_locations])
        message = f"up-to-date [{urls}]"
        return RebuildDecision(False, message)

    return rebuild_filter


def create_external_pruner() -> Callable[[spack.spec.Spec], RebuildDecision]:
    """Return a filter that prunes external specs"""

    def rebuild_filter(s: spack.spec.Spec) -> RebuildDecision:
        if not s.external:
            return RebuildDecision(True, "not external")
        return RebuildDecision(False, "external spec")

    return rebuild_filter


def _format_pruning_message(spec: spack.spec.Spec, prune: bool, reasons: List[str]) -> str:
    reason_msg = ", ".join(reasons)
    spec_fmt = "{name}{@version}{%compiler}{/hash:7}"

    if not prune:
        status = colorize("@*g{[x]}  ")
        return f"  {status}{spec.cformat(spec_fmt)} ({reason_msg})"

    msg = f"{spec.format(spec_fmt)} ({reason_msg})"
    return colorize(f"  @K -   {cescape(msg)}@.")


def prune_pipeline(
    pipeline: PipelineDag,
    pruning_filters: List[Callable[[spack.spec.Spec], RebuildDecision]],
    print_summary: bool = False,
) -> None:
    """Given a PipelineDag and a list of pruning filters, return a modified
    PipelineDag containing only the nodes that survive pruning by all of the
    filters."""
    keys_to_prune = set()
    keys_to_rebuild = set()
    specs: Dict[str, spack.spec.Spec] = {}
    reasons: Dict[str, List[str]] = {}

    for _, node in pipeline.traverse_nodes(direction="children"):
        filter_results = [keepSpec(node.spec) for keepSpec in pruning_filters]

        reasons[node.key] = [r.reason for r in filter_results]
        specs[node.key] = node.spec

        if not all(r.rebuild for r in filter_results):
            keys_to_prune.add(node.key)
        else:
            keys_to_rebuild.add(node.key)

    for key in keys_to_prune:
        pipeline.prune(key)

    if print_summary:
        sort_key = lambda k: f"{specs[k].name}/{specs[k].dag_hash(7)}"
        tty.msg("Pipeline pruning summary:")
        if keys_to_rebuild:
            tty.msg("  Rebuild list:")
            for key in sorted(keys_to_rebuild, key=sort_key):
                tty.msg(_format_pruning_message(specs[key], False, reasons[key]))
        if keys_to_prune:
            tty.msg("  Prune list:")
            for key in sorted(keys_to_prune, key=sort_key):
                tty.msg(_format_pruning_message(specs[key], True, reasons[key]))


def check_for_broken_specs(pipeline_specs: List[spack.spec.Spec], broken_specs_url: str) -> bool:
    """Check the pipeline specs against the list of known broken specs and return
    True if there were any matches, False otherwise."""
    if broken_specs_url.startswith("http"):
        # To make checking each spec against the list faster, we require
        # a url protocol that allows us to iterate the url in advance.
        tty.msg("Cannot use an http(s) url for broken specs, ignoring")
        return False

    broken_spec_urls = web_util.list_url(broken_specs_url)

    if broken_spec_urls is None:
        return False

    known_broken_specs_encountered = []
    for release_spec in pipeline_specs:
        release_spec_dag_hash = release_spec.dag_hash()
        if release_spec_dag_hash in broken_spec_urls:
            known_broken_specs_encountered.append(release_spec_dag_hash)

    if known_broken_specs_encountered:
        tty.error("This pipeline generated hashes known to be broken on develop:")
        display_broken_spec_messages(broken_specs_url, known_broken_specs_encountered)
        return True

    return False


def collect_pipeline_options(env: ev.Environment, args) -> PipelineOptions:
    """Gather pipeline options from cli args, spack environment, and
    os environment variables"""
    pipeline_mirrors = spack.mirrors.mirror.MirrorCollection(binary=True)
    if "buildcache-destination" not in pipeline_mirrors:
        raise SpackCIError("spack ci generate requires a mirror named 'buildcache-destination'")

    buildcache_destination = pipeline_mirrors["buildcache-destination"]
    options = PipelineOptions(env, buildcache_destination)

    options.env = env
    options.artifacts_root = args.artifacts_root
    options.output_file = args.output_file
    options.prune_up_to_date = args.prune_dag
    options.prune_external = args.prune_externals
    options.check_index_only = args.index_only

    ci_config = cfg.get("ci")

    cdash_config = cfg.get("cdash")
    if "build-group" in cdash_config:
        options.cdash_handler = CDashHandler(cdash_config)

    dependent_depth = os.environ.get("SPACK_PRUNE_UNTOUCHED_DEPENDENT_DEPTH", None)
    if dependent_depth is not None:
        try:
            options.untouched_pruning_dependent_depth = int(dependent_depth)
        except (TypeError, ValueError):
            tty.warn(
                f"Unrecognized value ({dependent_depth}) "
                "provided for SPACK_PRUNE_UNTOUCHED_DEPENDENT_DEPTH, "
                "ignoring it."
            )

    spack_prune_untouched = os.environ.get("SPACK_PRUNE_UNTOUCHED", None)
    options.prune_untouched = (
        spack_prune_untouched is not None and spack_prune_untouched.lower() == "true"
    )

    # Allow overriding --prune-dag cli opt with environment variable
    prune_dag_override = os.environ.get("SPACK_PRUNE_UP_TO_DATE", None)
    if prune_dag_override is not None:
        options.prune_up_to_date = True if prune_dag_override.lower() == "true" else False

    options.stack_name = os.environ.get("SPACK_CI_STACK_NAME", None)
    require_signing = os.environ.get("SPACK_REQUIRE_SIGNING", None)
    options.require_signing = (
        True if require_signing and require_signing.lower() == "true" else False
    )

    # Get the type of pipeline, which is optional
    spack_pipeline_type = os.environ.get("SPACK_PIPELINE_TYPE", None)
    if spack_pipeline_type:
        try:
            options.pipeline_type = PipelineType[spack_pipeline_type]
        except KeyError:
            options.pipeline_type = None

    if "broken-specs-url" in ci_config:
        options.broken_specs_url = ci_config["broken-specs-url"]

    if "rebuild-index" in ci_config and ci_config["rebuild-index"] is False:
        options.rebuild_index = False

    return options


def generate_pipeline(env: ev.Environment, args) -> None:
    """Given an environment and the command-line args, generate a pipeline.

    Arguments:
        env (spack.environment.Environment): Activated environment object
            which must contain a ci section describing attributes for
            all jobs and a target which should specify an existing
            pipeline generator.
        args: (spack.main.SpackArgumentParser): Parsed arguments from the command
            line.
    """
    with spack.concretize.disable_compiler_existence_check():
        with env.write_transaction():
            env.concretize()
            env.write()

    options = collect_pipeline_options(env, args)

    # Get the joined "ci" config with all of the current scopes resolved
    ci_config = cfg.get("ci")
    if not ci_config:
        raise SpackCIError("Environment does not have a `ci` configuration")

    # Get the target platform we should generate a pipeline for
    ci_target = ci_config.get("target", "gitlab")
    try:
        generate_method = get_generator(ci_target)
    except UnknownGeneratorException:
        raise SpackCIError(f"Spack CI module cannot generate a pipeline for format {ci_target}")

    # If we are not doing any kind of pruning, we are rebuilding everything
    rebuild_everything = not options.prune_up_to_date and not options.prune_untouched

    # Build a pipeline from the specs in the concrete environment
    pipeline = PipelineDag(
        [
            concrete
            for abstract, concrete in env.concretized_specs()
            if abstract in env.spec_lists["specs"]
        ]
    )

    # Optionally add various pruning filters
    pruning_filters = []

    # Possibly prune specs that were unaffected by the change
    if options.prune_untouched:
        # If we don't have two revisions to compare, or if either the spack.yaml
        # associated with the active env or the .gitlab-ci.yml files changed
        # between the provided revisions, then don't do any "untouched spec"
        # pruning.  Otherwise, list the names of all packages touched between
        # rev1 and rev2, and prune from the pipeline any node whose spec has a
        # packagen name not in that list.
        rev1, rev2 = get_change_revisions()
        tty.debug(f"Got following revisions: rev1={rev1}, rev2={rev2}")
        if rev1 and rev2:
            # If the stack file itself did not change, proceed with pruning
            if not get_stack_changed(env.manifest_path, rev1, rev2):
                affected_pkgs = compute_affected_packages(rev1, rev2)
                tty.debug("affected pkgs:")
                for p in affected_pkgs:
                    tty.debug(f"  {p}")
                affected_specs = get_spec_filter_list(
                    env,
                    affected_pkgs,
                    dependent_traverse_depth=options.untouched_pruning_dependent_depth,
                )
                tty.debug(
                    "dependent_traverse_depth="
                    f"{options.untouched_pruning_dependent_depth}, affected specs:"
                )
                for s in affected_specs:
                    tty.debug(f"  {PipelineDag.key(s)}")

                pruning_filters.append(create_unaffected_pruner(affected_specs))

    # Possibly prune specs that are already built on some configured mirror
    if options.prune_up_to_date:
        pruning_filters.append(
            create_already_built_pruner(check_index_only=options.check_index_only)
        )

    # Possibly prune specs that are external
    if options.prune_external:
        pruning_filters.append(create_external_pruner())

    # Do all the pruning
    prune_pipeline(pipeline, pruning_filters, options.print_summary)

    # List all specs remaining after any pruning
    pipeline_specs = [n.spec for _, n in pipeline.traverse_nodes(direction="children")]

    # If this is configured, spack will fail "spack ci generate" if it
    # generates any hash which exists under the broken specs url.
    if options.broken_specs_url and not options.pipeline_type == PipelineType.COPY_ONLY:
        broken = check_for_broken_specs(pipeline_specs, options.broken_specs_url)
        if broken and not rebuild_everything:
            raise SpackCIError("spack ci generate failed broken specs check")

    spack_ci_config = SpackCIConfig(ci_config)
    spack_ci_config.init_pipeline_jobs(pipeline)

    # Format the pipeline using the formatter specified in the configs
    generate_method(pipeline, spack_ci_config, options)

    # Use all unpruned specs to populate the build group for this set
    cdash_config = cfg.get("cdash")
    if options.cdash_handler and options.cdash_handler.auth_token:
        try:
            options.cdash_handler.populate_buildgroup(
                [options.cdash_handler.build_name(s) for s in pipeline_specs]
            )
        except (SpackError, HTTPError, URLError, TimeoutError) as err:
            tty.warn(f"Problem populating buildgroup: {err}")
    elif cdash_config:
        # warn only if there was actually a CDash configuration.
        tty.warn("Unable to populate buildgroup without CDash credentials")


def import_signing_key(base64_signing_key):
    """Given Base64-encoded gpg key, decode and import it to use for
        signing packages.

    Arguments:
        base64_signing_key (str): A gpg key including the secret key,
            armor-exported and base64 encoded, so it can be stored in a
            gitlab CI variable.  For an example of how to generate such
            a key, see:

        https://github.com/spack/spack-infrastructure/blob/main/gitlab-docker/files/gen-key
    """
    if not base64_signing_key:
        tty.warn("No key found for signing/verifying packages")
        return

    tty.debug("ci.import_signing_key() will attempt to import a key")

    # This command has the side-effect of creating the directory referred
    # to as GNUPGHOME in setup_environment()
    list_output = spack_gpg("list", output=str)

    tty.debug("spack gpg list:")
    tty.debug(list_output)

    decoded_key = base64.b64decode(base64_signing_key)
    if isinstance(decoded_key, bytes):
        decoded_key = decoded_key.decode("utf8")

    with tempfile.TemporaryDirectory() as tmpdir:
        sign_key_path = os.path.join(tmpdir, "signing_key")
        with open(sign_key_path, "w", encoding="utf-8") as fd:
            fd.write(decoded_key)

        key_import_output = spack_gpg("trust", sign_key_path, output=str)
        tty.debug(f"spack gpg trust {sign_key_path}")
        tty.debug(key_import_output)

    # Now print the keys we have for verifying and signing
    trusted_keys_output = spack_gpg("list", "--trusted", output=str)
    signing_keys_output = spack_gpg("list", "--signing", output=str)

    tty.debug("spack gpg list --trusted")
    tty.debug(trusted_keys_output)
    tty.debug("spack gpg list --signing")
    tty.debug(signing_keys_output)


def can_sign_binaries():
    """Utility method to determine if this spack instance is capable of
    signing binary packages.  This is currently only possible if the
    spack gpg keystore contains exactly one secret key."""
    return len(gpg_util.signing_keys()) == 1


def can_verify_binaries():
    """Utility method to determin if this spack instance is capable (at
    least in theory) of verifying signed binaries."""
    return len(gpg_util.public_keys()) >= 1


def push_to_build_cache(spec: spack.spec.Spec, mirror_url: str, sign_binaries: bool) -> bool:
    """Push one or more binary packages to the mirror.

    Arguments:

        spec: Installed spec to push
        mirror_url: URL of target mirror
        sign_binaries: If True, spack will attempt to sign binary package before pushing.
    """
    tty.debug(f"Pushing to build cache ({'signed' if sign_binaries else 'unsigned'})")
    signing_key = bindist.select_signing_key() if sign_binaries else None
    mirror = spack.mirrors.mirror.Mirror.from_url(mirror_url)
    try:
        with bindist.make_uploader(mirror, signing_key=signing_key) as uploader:
            uploader.push_or_raise([spec])
        return True
    except bindist.PushToBuildCacheError as e:
        tty.error(f"Problem writing to {mirror_url}: {e}")
        return False


def copy_stage_logs_to_artifacts(job_spec: spack.spec.Spec, job_log_dir: str) -> None:
    """Copy selected build stage file(s) to the given artifacts directory

    Looks for build logs in the stage directory of the given
    job_spec, and attempts to copy the files into the directory given
    by job_log_dir.

    Args:
        job_spec: spec associated with spack install log
        job_log_dir: path into which build log should be copied
    """
    tty.debug(f"job spec: {job_spec}")

    try:
        pkg_cls = spack.repo.PATH.get_pkg_class(job_spec.name)
        job_pkg = pkg_cls(job_spec)
        tty.debug(f"job package: {job_pkg}")
    except AssertionError:
        msg = f"Cannot copy stage logs: job spec ({job_spec}) must be concrete"
        tty.error(msg)
        return

    stage_dir = job_pkg.stage.path
    tty.debug(f"stage dir: {stage_dir}")
    for file in [
        job_pkg.log_path,
        job_pkg.env_mods_path,
        *spack.builder.create(job_pkg).archive_files,
    ]:
        copy_files_to_artifacts(file, job_log_dir)


def copy_test_logs_to_artifacts(test_stage, job_test_dir):
    """
    Copy test log file(s) to the given artifacts directory

    Parameters:
        test_stage (str): test stage path
        job_test_dir (str): the destination artifacts test directory
    """
    tty.debug(f"test stage: {test_stage}")
    if not os.path.exists(test_stage):
        msg = f"Cannot copy test logs: job test stage ({test_stage}) does not exist"
        tty.error(msg)
        return

    copy_files_to_artifacts(os.path.join(test_stage, "*", "*.txt"), job_test_dir)


def download_and_extract_artifacts(url, work_dir):
    """Look for gitlab artifacts.zip at the given url, and attempt to download
        and extract the contents into the given work_dir

    Arguments:

        url (str): Complete url to artifacts.zip file
        work_dir (str): Path to destination where artifacts should be extracted
    """
    tty.msg(f"Fetching artifacts from: {url}")

    headers = {"Content-Type": "application/zip"}

    token = os.environ.get("GITLAB_PRIVATE_TOKEN", None)
    if token:
        headers["PRIVATE-TOKEN"] = token

    opener = build_opener(HTTPHandler)

    request = Request(url, headers=headers)
    request.get_method = lambda: "GET"

    response = opener.open(request, timeout=SPACK_CDASH_TIMEOUT)
    response_code = response.getcode()

    if response_code != 200:
        msg = f"Error response code ({response_code}) in reproduce_ci_job"
        raise SpackError(msg)

    artifacts_zip_path = os.path.join(work_dir, "artifacts.zip")

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)

    with open(artifacts_zip_path, "wb") as out_file:
        shutil.copyfileobj(response, out_file)

    zip_file = zipfile.ZipFile(artifacts_zip_path)
    zip_file.extractall(work_dir)
    zip_file.close()

    os.remove(artifacts_zip_path)


def get_spack_info():
    """If spack is running from a git repo, return the most recent git log
    entry, otherwise, return a string containing the spack version."""
    git_path = os.path.join(spack.paths.prefix, ".git")
    if os.path.exists(git_path):
        git = spack.util.git.git()
        if git:
            with fs.working_dir(spack.paths.prefix):
                git_log = git("log", "-1", output=str, error=os.devnull, fail_on_error=False)

            return git_log

    return f"no git repo, use spack {spack.spack_version}"


def setup_spack_repro_version(repro_dir, checkout_commit, merge_commit=None):
    """Look in the local spack clone to find the checkout_commit, and if
        provided, the merge_commit given as arguments.  If those commits can
        be found locally, then clone spack and attempt to recreate a merge
        commit with the same parent commits as tested in gitlab.  This looks
        something like 1) git clone repo && cd repo 2) git checkout
        <checkout_commit> 3) git merge <merge_commit>.  If there is no
        merge_commit provided, then skip step (3).

    Arguments:

        repro_dir (str): Location where spack should be cloned
        checkout_commit (str): SHA of PR branch commit
        merge_commit (str): SHA of target branch parent

    Returns: True if git repo state was successfully recreated, or False
        otherwise.
    """
    # figure out the path to the spack git version being used for the
    # reproduction
    tty.info(f"checkout_commit: {checkout_commit}")
    tty.info(f"merge_commit: {merge_commit}")

    dot_git_path = os.path.join(spack.paths.prefix, ".git")
    if not os.path.exists(dot_git_path):
        tty.error("Unable to find the path to your local spack clone")
        return False

    spack_git_path = spack.paths.prefix

    git = spack.util.git.git()
    if not git:
        tty.error("reproduction of pipeline job requires git")
        return False

    # Check if we can find the tested commits in your local spack repo
    with fs.working_dir(spack_git_path):
        git("log", "-1", checkout_commit, output=str, error=os.devnull, fail_on_error=False)

        if git.returncode != 0:
            tty.error(f"Missing commit: {checkout_commit}")
            return False

        if merge_commit:
            git("log", "-1", merge_commit, output=str, error=os.devnull, fail_on_error=False)

            if git.returncode != 0:
                tty.error(f"Missing commit: {merge_commit}")
                return False

    # Next attempt to clone your local spack repo into the repro dir
    with fs.working_dir(repro_dir):
        clone_out = git(
            "clone", spack_git_path, "spack", output=str, error=os.devnull, fail_on_error=False
        )

        if git.returncode != 0:
            tty.error("Unable to clone your local spack repo:")
            tty.msg(clone_out)
            return False

    # Finally, attempt to put the cloned repo into the same state used during
    # the pipeline build job
    repro_spack_path = os.path.join(repro_dir, "spack")
    with fs.working_dir(repro_spack_path):
        co_out = git(
            "checkout", checkout_commit, output=str, error=os.devnull, fail_on_error=False
        )

        if git.returncode != 0:
            tty.error(f"Unable to checkout {checkout_commit}")
            tty.msg(co_out)
            return False

        if merge_commit:
            merge_out = git(
                "-c",
                "user.name=cirepro",
                "-c",
                "user.email=user@email.org",
                "merge",
                "--no-edit",
                merge_commit,
                output=str,
                error=os.devnull,
                fail_on_error=False,
            )

            if git.returncode != 0:
                tty.error(f"Unable to merge {merge_commit}")
                tty.msg(merge_out)
                return False

    return True


def reproduce_ci_job(url, work_dir, autostart, gpg_url, runtime):
    """Given a url to gitlab artifacts.zip from a failed 'spack ci rebuild' job,
    attempt to setup an environment in which the failure can be reproduced
    locally.  This entails the following:

    First download and extract artifacts.  Then look through those artifacts
    to glean some information needed for the reproduer (e.g. one of the
    artifacts contains information about the version of spack tested by
    gitlab, another is the generated pipeline yaml containing details
    of the job like the docker image used to run it).  The output of this
    function is a set of printed instructions for running docker and then
    commands to run to reproduce the build once inside the container.
    """
    work_dir = os.path.realpath(work_dir)
    platform_script_ext = "ps1" if IS_WINDOWS else "sh"
    download_and_extract_artifacts(url, work_dir)

    gpg_path = None
    if gpg_url:
        gpg_path = web_util.fetch_url_text(gpg_url, dest_dir=os.path.join(work_dir, "_pgp"))
        rel_gpg_path = gpg_path.replace(work_dir, "").lstrip(os.path.sep)

    lock_file = fs.find(work_dir, "spack.lock")[0]
    repro_lock_dir = os.path.dirname(lock_file)

    tty.debug(f"Found lock file in: {repro_lock_dir}")

    yaml_files = fs.find(work_dir, ["*.yaml", "*.yml"])

    tty.debug("yaml files:")
    for yaml_file in yaml_files:
        tty.debug(f"  {yaml_file}")

    pipeline_yaml = None

    # Try to find the dynamically generated pipeline yaml file in the
    # reproducer.  If the user did not put it in the artifacts root,
    # but rather somewhere else and exported it as an artifact from
    # that location, we won't be able to find it.
    for yf in yaml_files:
        with open(yf, encoding="utf-8") as y_fd:
            yaml_obj = syaml.load(y_fd)
            if "variables" in yaml_obj and "stages" in yaml_obj:
                pipeline_yaml = yaml_obj

    if pipeline_yaml:
        tty.debug(f"\n{yf} is likely your pipeline file")

    relative_concrete_env_dir = pipeline_yaml["variables"]["SPACK_CONCRETE_ENV_DIR"]
    tty.debug(f"Relative environment path used by cloud job: {relative_concrete_env_dir}")

    # Using the relative concrete environment path found in the generated
    # pipeline variable above, copy the spack environment files so they'll
    # be found in the same location as when the job ran in the cloud.
    concrete_env_dir = os.path.join(work_dir, relative_concrete_env_dir)
    os.makedirs(concrete_env_dir, exist_ok=True)
    copy_lock_path = os.path.join(concrete_env_dir, "spack.lock")
    orig_yaml_path = os.path.join(repro_lock_dir, "spack.yaml")
    copy_yaml_path = os.path.join(concrete_env_dir, "spack.yaml")
    shutil.copyfile(lock_file, copy_lock_path)
    shutil.copyfile(orig_yaml_path, copy_yaml_path)

    # Find the install script in the unzipped artifacts and make it executable
    install_script = fs.find(work_dir, f"install.{platform_script_ext}")[0]
    if not IS_WINDOWS:
        # pointless on Windows
        st = os.stat(install_script)
        os.chmod(install_script, st.st_mode | stat.S_IEXEC)
    # Find the repro details file.  This just includes some values we wrote
    # during `spack ci rebuild` to make reproduction easier.  E.g. the job
    # name is written here so we can easily find the configuration of the
    # job from the generated pipeline file.
    repro_file = fs.find(work_dir, "repro.json")[0]
    repro_details = None
    with open(repro_file, encoding="utf-8") as fd:
        repro_details = json.load(fd)

    repro_dir = os.path.dirname(repro_file)
    rel_repro_dir = repro_dir.replace(work_dir, "").lstrip(os.path.sep)

    # Find the spack info text file that should contain the git log
    # of the HEAD commit used during the CI build
    spack_info_file = fs.find(work_dir, "spack_info.txt")[0]
    with open(spack_info_file, encoding="utf-8") as fd:
        spack_info = fd.read()

    # Access the specific job configuration
    job_name = repro_details["job_name"]
    job_yaml = None

    if job_name in pipeline_yaml:
        job_yaml = pipeline_yaml[job_name]

    if job_yaml:
        tty.debug("Found job:")
        tty.debug(job_yaml)

    job_image = None
    setup_result = False
    if "image" in job_yaml:
        job_image_elt = job_yaml["image"]
        if "name" in job_image_elt:
            job_image = job_image_elt["name"]
        else:
            job_image = job_image_elt
        tty.msg(f"Job ran with the following image: {job_image}")

        # Because we found this job was run with a docker image, so we will try
        # to print a "docker run" command that bind-mounts the directory where
        # we extracted the artifacts.

        # Destination of bind-mounted reproduction directory.  It makes for a
        # more faithful reproducer if everything appears to run in the same
        # absolute path used during the CI build.
        mount_as_dir = "/work"
        mounted_workdir = "/reproducer"
        if repro_details:
            mount_as_dir = repro_details["ci_project_dir"]
            mounted_repro_dir = os.path.join(mount_as_dir, rel_repro_dir)
            mounted_env_dir = os.path.join(mount_as_dir, relative_concrete_env_dir)
            if gpg_path:
                mounted_gpg_path = os.path.join(mounted_workdir, rel_gpg_path)

    # We will also try to clone spack from your local checkout and
    # reproduce the state present during the CI build, and put that into
    # the bind-mounted reproducer directory.

    # Regular expressions for parsing that HEAD commit.  If the pipeline
    # was on the gitlab spack mirror, it will have been a merge commit made by
    # gitub and pushed by the sync script.  If the pipeline was run on some
    # environment repo, then the tested spack commit will likely have been
    # a regular commit.
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
            setup_result = setup_spack_repro_version(work_dir, commit_2, merge_commit=commit_1)
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
        tty.error(
            "Failed to automatically setup the tested version of spack "
            "in your local reproduction directory."
        )
        tty.info(setup_msg)

    # In cases where CI build was run on a shell runner, it might be useful
    # to see what tags were applied to the job so the user knows what shell
    # runner was used.  But in that case in general, we cannot do nearly as
    # much to set up the reproducer.
    job_tags = None
    if "tags" in job_yaml:
        job_tags = job_yaml["tags"]
        tty.msg(f"Job ran with the following tags: {job_tags}")

    entrypoint_script = [
        ["git", "config", "--global", "--add", "safe.directory", mount_as_dir],
        [
            ".",
            os.path.join(
                mount_as_dir if job_image else work_dir,
                f"share/spack/setup-env.{platform_script_ext}",
            ),
        ],
        ["spack", "gpg", "trust", mounted_gpg_path if job_image else gpg_path] if gpg_path else [],
        ["spack", "env", "activate", mounted_env_dir if job_image else repro_dir],
        [
            (
                os.path.join(mounted_repro_dir, f"install.{platform_script_ext}")
                if job_image
                else install_script
            )
        ],
    ]
    entry_script = os.path.join(mounted_workdir, f"entrypoint.{platform_script_ext}")
    inst_list = []
    # Finally, print out some instructions to reproduce the build
    if job_image:
        # Allow interactive
        install_mechanism = (
            os.path.join(mounted_repro_dir, f"install.{platform_script_ext}")
            if job_image
            else install_script
        )
        entrypoint_script.append(["echo", f"Re-run install script using:\n\t{install_mechanism}"])
        # Allow interactive
        if IS_WINDOWS:
            entrypoint_script.append(["&", "($args -Join ' ')", "-NoExit"])
        else:
            entrypoint_script.append(["exec", "$@"])

        process_command(
            "entrypoint", entrypoint_script, work_dir, run=False, exit_on_failure=False
        )

        docker_command = [
            runtime,
            "run",
            "-i",
            "-t",
            "--rm",
            "--name",
            "spack_reproducer",
            "-v",
            ":".join([work_dir, mounted_workdir, "Z"]),
            "-v",
            ":".join(
                [
                    os.path.join(work_dir, "jobs_scratch_dir"),
                    os.path.join(mount_as_dir, "jobs_scratch_dir"),
                    "Z",
                ]
            ),
            "-v",
            ":".join([os.path.join(work_dir, "spack"), mount_as_dir, "Z"]),
            "--entrypoint",
        ]
        if IS_WINDOWS:
            docker_command.extend(["powershell.exe", job_image, entry_script, "powershell.exe"])
        else:
            docker_command.extend([entry_script, job_image, "bash"])
        docker_command = [docker_command]
        autostart = autostart and setup_result
        process_command("start", docker_command, work_dir, run=autostart)

        if not autostart:
            inst_list.append("\nTo run the docker reproducer:\n\n")
            inst_list.extend(
                [
                    "    - Start the docker container install",
                    f"       $ {work_dir}/start.{platform_script_ext}",
                ]
            )
    else:
        autostart = autostart and setup_result
        process_command("reproducer", entrypoint_script, work_dir, run=autostart)

        inst_list.append("\nOnce on the tagged runner:\n\n")
        inst_list.extent(
            [
                "    - Run the reproducer script",
                f"       $ {work_dir}/reproducer.{platform_script_ext}",
            ]
        )

    if not setup_result:
        inst_list.append("\n    - Clone spack and acquire tested commit")
        inst_list.append(f"\n        {spack_info}\n")
        inst_list.append("\n")
        inst_list.append(f"\n        Path to clone spack: {work_dir}/spack\n\n")

    tty.msg("".join(inst_list))


def process_command(name, commands, repro_dir, run=True, exit_on_failure=True):
    """
    Create a script for and run the command. Copy the script to the
    reproducibility directory.

    Arguments:
        name (str): name of the command being processed
        commands (list): list of arguments for single command or list of lists of
            arguments for multiple commands. No shell escape is performed.
        repro_dir (str): Job reproducibility directory
        run (bool): Run the script and return the exit code if True

    Returns: the exit code from processing the command
    """

    tty.debug(f"spack {name} arguments: {commands}")
    if len(commands) == 0 or isinstance(commands[0], str):
        commands = [commands]

    def compose_command_err_handling(args):
        if not IS_WINDOWS:
            args = [f'"{arg}"' for arg in args]
        arg_str = " ".join(args)
        result = arg_str + "\n"
        # ErrorActionPreference will handle PWSH commandlets (Spack calls),
        # but we need to handle EXEs (git, etc) ourselves
        catch_exe_failure = (
            """
if ($LASTEXITCODE -ne 0){{
    throw 'Command {} has failed'
}}
"""
            if IS_WINDOWS
            else ""
        )
        if exit_on_failure and catch_exe_failure:
            result += catch_exe_failure.format(arg_str)
        return result

    # Create a string [command 1] \n [command 2] \n ... \n [command n] with
    # commands composed into a platform dependent shell script, pwsh on Windows,
    full_command = "\n".join(map(compose_command_err_handling, commands))
    # Write the command to a python script
    if IS_WINDOWS:
        script = f"{name}.ps1"
        script_content = [f"\n# spack {name} command\n"]
        if exit_on_failure:
            script_content.append('$ErrorActionPreference = "Stop"\n')
        if os.environ.get("SPACK_VERBOSE_SCRIPT"):
            script_content.append("Set-PSDebug -Trace 2\n")
    else:
        script = f"{name}.sh"
        script_content = ["#!/bin/sh\n\n", f"\n# spack {name} command\n"]
        if exit_on_failure:
            script_content.append("set -e\n")
        if os.environ.get("SPACK_VERBOSE_SCRIPT"):
            script_content.append("set -x\n")
    script_content.append(full_command)
    script_content.append("\n")

    with open(script, "w", encoding="utf-8") as fd:
        for line in script_content:
            fd.write(line)

    copy_path = os.path.join(repro_dir, script)
    shutil.copyfile(script, copy_path)
    if not IS_WINDOWS:
        st = os.stat(copy_path)
        os.chmod(copy_path, st.st_mode | stat.S_IEXEC)

    # Run the generated shell script as if it were being run in
    # a login shell.
    exit_code = None
    if run:
        try:
            # We use sh as executor on Linux like platforms, pwsh on Windows
            interpreter = "powershell.exe" if IS_WINDOWS else "/bin/sh"
            cmd_process = subprocess.Popen([interpreter, f"./{script}"])
            cmd_process.wait()
            exit_code = cmd_process.returncode
        except (ValueError, subprocess.CalledProcessError, OSError) as err:
            tty.error(f"Encountered error running {name} script")
            tty.error(err)
            exit_code = 1

        tty.debug(f"spack {name} exited {exit_code}")
    else:
        # Delete the script, it is copied to the destination dir
        os.remove(script)

    return exit_code


def create_buildcache(
    input_spec: spack.spec.Spec, *, destination_mirror_urls: List[str], sign_binaries: bool = False
) -> List[PushResult]:
    """Create the buildcache at the provided mirror(s).

    Arguments:
        input_spec: Installed spec to package and push
        destination_mirror_urls: List of urls to push to
        sign_binaries: Whether or not to sign buildcache entry

    Returns: A list of PushResults, indicating success or failure.
    """
    results = []

    for mirror_url in destination_mirror_urls:
        results.append(
            PushResult(
                success=push_to_build_cache(input_spec, mirror_url, sign_binaries), url=mirror_url
            )
        )

    return results


def write_broken_spec(url, pkg_name, stack_name, job_url, pipeline_url, spec_dict):
    """Given a url to write to and the details of the failed job, write an entry
    in the broken specs list.
    """
    tmpdir = tempfile.mkdtemp()
    file_path = os.path.join(tmpdir, "broken.txt")

    broken_spec_details = {
        "broken-spec": {
            "job-name": pkg_name,
            "job-stack": stack_name,
            "job-url": job_url,
            "pipeline-url": pipeline_url,
            "concrete-spec-dict": spec_dict,
        }
    }

    try:
        with open(file_path, "w", encoding="utf-8") as fd:
            syaml.dump(broken_spec_details, fd)
        web_util.push_to_url(
            file_path, url, keep_original=False, extra_args={"ContentType": "text/plain"}
        )
    except Exception as err:
        # If there is an S3 error (e.g., access denied or connection
        # error), the first non boto-specific class in the exception
        # hierarchy is Exception.  Just print a warning and return
        msg = f"Error writing to broken specs list {url}: {err}"
        tty.warn(msg)
    finally:
        shutil.rmtree(tmpdir)


def read_broken_spec(broken_spec_url):
    """Read data from broken specs file located at the url, return as a yaml
    object.
    """
    try:
        _, _, fs = web_util.read_from_url(broken_spec_url)
    except web_util.SpackWebError:
        tty.warn(f"Unable to read broken spec from {broken_spec_url}")
        return None

    broken_spec_contents = codecs.getreader("utf-8")(fs).read()
    return syaml.load(broken_spec_contents)


def display_broken_spec_messages(base_url, hashes):
    """Fetch the broken spec file for each of the hashes under the base_url and
    print a message with some details about each one.
    """
    broken_specs = [(h, read_broken_spec(url_util.join(base_url, h))) for h in hashes]
    for spec_hash, broken_spec in [tup for tup in broken_specs if tup[1]]:
        details = broken_spec["broken-spec"]
        if "job-name" in details:
            item_name = f"{details['job-name']}/{spec_hash[:7]}"
        else:
            item_name = spec_hash

        if "job-stack" in details:
            item_name = f"{item_name} (in stack {details['job-stack']})"

        msg = f"  {item_name} was reported broken here: {details['job-url']}"
        tty.msg(msg)


def run_standalone_tests(**kwargs):
    """Run stand-alone tests on the current spec.

    Arguments:
       kwargs (dict): dictionary of arguments used to run the tests

    List of recognized keys:

    * "cdash" (CDashHandler): (optional) cdash handler instance
    * "fail_fast" (bool): (optional) terminate tests after the first failure
    * "log_file" (str): (optional) test log file name if NOT CDash reporting
    * "job_spec" (Spec): spec that was built
    * "repro_dir" (str): reproduction directory
    """
    cdash = kwargs.get("cdash")
    fail_fast = kwargs.get("fail_fast")
    log_file = kwargs.get("log_file")

    if cdash and log_file:
        tty.msg(f"The test log file {log_file} option is ignored with CDash reporting")
        log_file = None

    # Error out but do NOT terminate if there are missing required arguments.
    job_spec = kwargs.get("job_spec")
    if not job_spec:
        tty.error("Job spec is required to run stand-alone tests")
        return

    repro_dir = kwargs.get("repro_dir")
    if not repro_dir:
        tty.error("Reproduction directory is required for stand-alone tests")
        return

    test_args = ["spack", "--color=always", "--backtrace", "--verbose", "test", "run"]
    if fail_fast:
        test_args.append("--fail-fast")

    if cdash:
        test_args.extend(cdash.args())
    else:
        test_args.extend(["--log-format", "junit"])
        if log_file:
            test_args.extend(["--log-file", log_file])
    test_args.append(job_spec.name)

    tty.debug(f"Running {job_spec.name} stand-alone tests")
    exit_code = process_command("test", test_args, repro_dir)

    tty.debug(f"spack test exited {exit_code}")
