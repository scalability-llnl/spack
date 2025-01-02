# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import codecs
import copy
import json
import os
import re
import ssl
import sys
import time
from collections import deque
from enum import Enum
from typing import Dict, Generator, List, Optional, Set, Tuple
from urllib.parse import quote, urlencode, urlparse
from urllib.request import HTTPHandler, HTTPSHandler, Request, build_opener

import llnl.util.filesystem as fs
import llnl.util.tty as tty
from llnl.util.lang import Singleton, memoized

import spack.binary_distribution as bindist
import spack.config as cfg
import spack.deptypes as dt
import spack.environment as ev
import spack.error
import spack.mirrors.mirror
import spack.schema
import spack.spec
import spack.util.spack_yaml as syaml
import spack.util.url as url_util
import spack.util.web as web_util
from spack import traverse
from spack.reporters import CDash, CDashConfiguration
from spack.reporters.cdash import SPACK_CDASH_TIMEOUT
from spack.reporters.cdash import build_stamp as cdash_build_stamp


def _urlopen():
    error_handler = web_util.SpackHTTPDefaultErrorHandler()

    # One opener with HTTPS ssl enabled
    with_ssl = build_opener(
        HTTPHandler(), HTTPSHandler(context=web_util.ssl_create_default_context()), error_handler
    )

    # One opener with HTTPS ssl disabled
    without_ssl = build_opener(
        HTTPHandler(), HTTPSHandler(context=ssl._create_unverified_context()), error_handler
    )

    # And dynamically dispatch based on the config:verify_ssl.
    def dispatch_open(fullurl, data=None, timeout=None, verify_ssl=True):
        opener = with_ssl if verify_ssl else without_ssl
        timeout = timeout or cfg.get("config:connect_timeout", 1)
        return opener.open(fullurl, data, timeout)

    return dispatch_open


IS_WINDOWS = sys.platform == "win32"
SPACK_RESERVED_TAGS = ["public", "protected", "notary"]
_dyn_mapping_urlopener = Singleton(_urlopen)


def copy_files_to_artifacts(src, artifacts_dir):
    """
    Copy file(s) to the given artifacts directory

    Parameters:
        src (str): the glob-friendly path expression for the file(s) to copy
        artifacts_dir (str): the destination directory
    """
    try:
        fs.copy(src, artifacts_dir)
    except Exception as err:
        msg = (
            f"Unable to copy files ({src}) to artifacts {artifacts_dir} due to "
            f"exception: {str(err)}"
        )
        tty.warn(msg)


def win_quote(quote_str: str) -> str:
    if IS_WINDOWS:
        quote_str = f'"{quote_str}"'
    return quote_str


def _spec_matches(spec, match_string):
    return spec.intersects(match_string)


def _noop(x):
    return x


def unpack_script(script_section, op=_noop):
    script = []
    for cmd in script_section:
        if isinstance(cmd, list):
            for subcmd in cmd:
                script.append(op(subcmd))
        else:
            script.append(op(cmd))

    return script


def ensure_expected_target_path(path: str) -> str:
    """Returns passed paths with all Windows path separators exchanged
    for posix separators

    TODO (johnwparent): Refactor config + cli read/write to deal only in posix style paths
    """
    if path:
        return path.replace("\\", "/")
    return path


def update_env_scopes(
    env: ev.Environment,
    cli_scopes: List[str],
    output_file: str,
    transform_windows_paths: bool = False,
) -> None:
    """Add any config scopes from cli_scopes which aren't already included in the
    environment, by reading the yaml, adding the missing includes, and writing the
    updated yaml back to the same location.
    """
    with open(env.manifest_path, "r", encoding="utf-8") as env_fd:
        env_yaml_root = syaml.load(env_fd)

    # Add config scopes to environment
    env_includes = env_yaml_root["spack"].get("include", [])
    include_scopes: List[str] = []
    for scope in cli_scopes:
        if scope not in include_scopes and scope not in env_includes:
            include_scopes.insert(0, scope)
    env_includes.extend(include_scopes)
    env_yaml_root["spack"]["include"] = [
        ensure_expected_target_path(i) if transform_windows_paths else i for i in env_includes
    ]

    with open(output_file, "w", encoding="utf-8") as fd:
        syaml.dump_config(env_yaml_root, fd, default_flow_style=False)


def write_pipeline_manifest(specs, src_prefix, dest_prefix, output_file):
    """Write out the file describing specs that should be copied"""
    buildcache_copies = {}

    for release_spec in specs:
        release_spec_dag_hash = release_spec.dag_hash()
        # TODO: This assumes signed version of the spec
        buildcache_copies[release_spec_dag_hash] = [
            {
                "src": url_util.join(
                    src_prefix,
                    bindist.build_cache_relative_path(),
                    bindist.tarball_name(release_spec, ".spec.json.sig"),
                ),
                "dest": url_util.join(
                    dest_prefix,
                    bindist.build_cache_relative_path(),
                    bindist.tarball_name(release_spec, ".spec.json.sig"),
                ),
            },
            {
                "src": url_util.join(
                    src_prefix,
                    bindist.build_cache_relative_path(),
                    bindist.tarball_path_name(release_spec, ".spack"),
                ),
                "dest": url_util.join(
                    dest_prefix,
                    bindist.build_cache_relative_path(),
                    bindist.tarball_path_name(release_spec, ".spack"),
                ),
            },
        ]

    target_dir = os.path.dirname(output_file)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    with open(output_file, "w", encoding="utf-8") as fd:
        fd.write(json.dumps(buildcache_copies))


class CDashHandler:
    """
    Class for managing CDash data and processing.
    """

    def __init__(self, ci_cdash):
        # start with the gitlab ci configuration
        self.url = ci_cdash.get("url")
        self.build_group = ci_cdash.get("build-group")
        self.project = ci_cdash.get("project")
        self.site = ci_cdash.get("site")

        # grab the authorization token when available
        self.auth_token = os.environ.get("SPACK_CDASH_AUTH_TOKEN")
        if self.auth_token:
            tty.verbose("Using CDash auth token from environment")

        # append runner description to the site if available
        runner = os.environ.get("CI_RUNNER_DESCRIPTION")
        if runner:
            self.site += f" ({runner})"

    def args(self):
        return [
            "--cdash-upload-url",
            win_quote(self.upload_url),
            "--cdash-build",
            win_quote(self.build_name()),
            "--cdash-site",
            win_quote(self.site),
            "--cdash-buildstamp",
            win_quote(self.build_stamp),
        ]

    def build_name(self, spec: Optional[spack.spec.Spec] = None) -> Optional[str]:
        """Returns the CDash build name.

        A name will be generated if the `spec` is provided,
        otherwise, the value will be retrieved from the environment
        through the `SPACK_CDASH_BUILD_NAME` variable.

        Returns: (str) given spec's CDash build name."""
        if spec:
            build_name = f"{spec.name}@{spec.version}%{spec.compiler} \
hash={spec.dag_hash()} arch={spec.architecture} ({self.build_group})"
            tty.debug(f"Generated CDash build name ({build_name}) from the {spec.name}")
            return build_name

        env_build_name = os.environ.get("SPACK_CDASH_BUILD_NAME")
        tty.debug(f"Using CDash build name ({env_build_name}) from the environment")
        return env_build_name

    @property  # type: ignore
    def build_stamp(self):
        """Returns the CDash build stamp.

        The one defined by SPACK_CDASH_BUILD_STAMP environment variable
        is preferred due to the representation of timestamps; otherwise,
        one will be built.

        Returns: (str) current CDash build stamp"""
        build_stamp = os.environ.get("SPACK_CDASH_BUILD_STAMP")
        if build_stamp:
            tty.debug(f"Using build stamp ({build_stamp}) from the environment")
            return build_stamp

        build_stamp = cdash_build_stamp(self.build_group, time.time())
        tty.debug(f"Generated new build stamp ({build_stamp})")
        return build_stamp

    @property  # type: ignore
    @memoized
    def project_enc(self):
        tty.debug(f"Encoding project ({type(self.project)}): {self.project})")
        encode = urlencode({"project": self.project})
        index = encode.find("=") + 1
        return encode[index:]

    @property
    def upload_url(self):
        url_format = f"{self.url}/submit.php?project={self.project_enc}"
        return url_format

    def copy_test_results(self, source, dest):
        """Copy test results to artifacts directory."""
        reports = fs.join_path(source, "*_Test*.xml")
        copy_files_to_artifacts(reports, dest)

    def create_buildgroup(self, opener, headers, url, group_name, group_type):
        data = {"newbuildgroup": group_name, "project": self.project, "type": group_type}

        enc_data = json.dumps(data).encode("utf-8")

        request = Request(url, data=enc_data, headers=headers)

        response = opener.open(request, timeout=SPACK_CDASH_TIMEOUT)
        response_code = response.getcode()

        if response_code not in [200, 201]:
            msg = f"Creating buildgroup failed (response code = {response_code})"
            tty.warn(msg)
            return None

        response_text = response.read()
        response_json = json.loads(response_text)
        build_group_id = response_json["id"]

        return build_group_id

    def populate_buildgroup(self, job_names):
        url = f"{self.url}/api/v1/buildgroup.php"

        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }

        opener = build_opener(HTTPHandler)

        parent_group_id = self.create_buildgroup(opener, headers, url, self.build_group, "Daily")
        group_id = self.create_buildgroup(
            opener, headers, url, f"Latest {self.build_group}", "Latest"
        )

        if not parent_group_id or not group_id:
            msg = f"Failed to create or retrieve buildgroups for {self.build_group}"
            tty.warn(msg)
            return

        data = {
            "dynamiclist": [
                {"match": name, "parentgroupid": parent_group_id, "site": self.site}
                for name in job_names
            ]
        }

        enc_data = json.dumps(data).encode("utf-8")

        request = Request(url, data=enc_data, headers=headers)
        request.get_method = lambda: "PUT"

        response = opener.open(request, timeout=SPACK_CDASH_TIMEOUT)
        response_code = response.getcode()

        if response_code != 200:
            msg = f"Error response code ({response_code}) in populate_buildgroup"
            tty.warn(msg)

    def report_skipped(self, spec: spack.spec.Spec, report_dir: str, reason: Optional[str]):
        """Explicitly report skipping testing of a spec (e.g., it's CI
        configuration identifies it as known to have broken tests or
        the CI installation failed).

        Args:
            spec: spec being tested
            report_dir: directory where the report will be written
            reason: reason the test is being skipped
        """
        configuration = CDashConfiguration(
            upload_url=self.upload_url,
            packages=[spec.name],
            build=self.build_name(),
            site=self.site,
            buildstamp=self.build_stamp,
            track=None,
        )
        reporter = CDash(configuration=configuration)
        reporter.test_skipped_report(report_dir, spec, reason)


class PipelineType(Enum):
    COPY_ONLY = 1
    spack_copy_only = 1
    PROTECTED_BRANCH = 2
    spack_protected_branch = 2
    PULL_REQUEST = 3
    spack_pull_request = 3


class PipelineOptions:
    """A container for all pipeline options that can be specified (whether
    via cli, config/yaml, or environment variables)"""

    def __init__(
        self,
        env: ev.Environment,
        buildcache_destination: spack.mirrors.mirror.Mirror,
        artifacts_root: str = "jobs_scratch_dir",
        print_summary: bool = True,
        output_file: Optional[str] = None,
        check_index_only: bool = False,
        broken_specs_url: Optional[str] = None,
        rebuild_index: bool = True,
        untouched_pruning_dependent_depth: Optional[int] = None,
        prune_untouched: bool = False,
        prune_up_to_date: bool = True,
        prune_external: bool = True,
        stack_name: Optional[str] = None,
        pipeline_type: Optional[PipelineType] = None,
        require_signing: bool = False,
        cdash_handler: Optional["CDashHandler"] = None,
    ):
        """
        Args:
            env: Active spack environment
            buildcache_destination: The mirror where built binaries should be pushed
            artifacts_root: Path to location where artifacts should be stored
            print_summary: Print a summary of the scheduled pipeline
            output_file: Path where output file should be written
            check_index_only: Only fetch the index or fetch all spec files
            broken_specs_url: URL where broken specs (on develop) should be reported
            rebuild_index: Generate a job to rebuild mirror index after rebuilds
            untouched_pruning_dependent_depth: How many parents to traverse from changed pkg specs
            prune_untouched: Prune jobs for specs that were unchanged in git history
            prune_up_to_date: Prune specs from pipeline if binary exists on the mirror
            prune_external: Prune specs from pipeline if they are external
            stack_name: Name of spack stack
            pipeline_type: Type of pipeline running (optional)
            require_signing: Require buildcache to be signed (fail w/out signing key)
            cdash_handler: Object for communicating build information with CDash
        """
        self.env = env
        self.buildcache_destination = buildcache_destination
        self.artifacts_root = artifacts_root
        self.print_summary = print_summary
        self.output_file = output_file
        self.check_index_only = check_index_only
        self.broken_specs_url = broken_specs_url
        self.rebuild_index = rebuild_index
        self.untouched_pruning_dependent_depth = untouched_pruning_dependent_depth
        self.prune_untouched = prune_untouched
        self.prune_up_to_date = prune_up_to_date
        self.prune_external = prune_external
        self.stack_name = stack_name
        self.pipeline_type = pipeline_type
        self.require_signing = require_signing
        self.cdash_handler = cdash_handler


class PipelineNode:
    spec: spack.spec.Spec
    parents: Set[str]
    children: Set[str]

    def __init__(self, spec: spack.spec.Spec):
        self.spec = spec
        self.parents = set()
        self.children = set()

    @property
    def key(self):
        """Return key of the stored spec"""
        return PipelineDag.key(self.spec)


class PipelineDag:
    """Turn a list of specs into a simple directed graph, that doesn't keep track
    of edge types."""

    @classmethod
    def key(cls, spec: spack.spec.Spec) -> str:
        return spec.dag_hash()

    def __init__(self, specs: List[spack.spec.Spec]) -> None:
        # Build dictionary of nodes
        self.nodes: Dict[str, PipelineNode] = {
            PipelineDag.key(s): PipelineNode(s)
            for s in traverse.traverse_nodes(specs, deptype=dt.ALL_TYPES, root=True)
        }

        # Create edges
        for edge in traverse.traverse_edges(
            specs, deptype=dt.ALL_TYPES, root=False, cover="edges"
        ):
            parent_key = PipelineDag.key(edge.parent)
            child_key = PipelineDag.key(edge.spec)

            self.nodes[parent_key].children.add(child_key)
            self.nodes[child_key].parents.add(parent_key)

    def prune(self, node_key: str):
        """Remove a node from the graph, and reconnect its parents and children"""
        node = self.nodes[node_key]
        for parent in node.parents:
            self.nodes[parent].children.remove(node_key)
            self.nodes[parent].children |= node.children
        for child in node.children:
            self.nodes[child].parents.remove(node_key)
            self.nodes[child].parents |= node.parents
        del self.nodes[node_key]

    def traverse_nodes(
        self, direction: str = "children"
    ) -> Generator[Tuple[int, PipelineNode], None, None]:
        """Yields (depth, node) from the pipeline graph.  Traversal is topologically
        ordered from the roots if ``direction`` is ``children``, or from the leaves
        if ``direction`` is ``parents``. The yielded depth is the length of the
        longest path from the starting point to the yielded node."""
        if direction == "children":
            get_in_edges = lambda node: node.parents
            get_out_edges = lambda node: node.children
        else:
            get_in_edges = lambda node: node.children
            get_out_edges = lambda node: node.parents

        sort_key = lambda k: self.nodes[k].spec.name

        out_edges = {k: sorted(get_out_edges(n), key=sort_key) for k, n in self.nodes.items()}
        num_in_edges = {k: len(get_in_edges(n)) for k, n in self.nodes.items()}

        # Populate a queue with all the nodes that have no incoming edges
        nodes = deque(
            sorted(
                [(0, key) for key in self.nodes.keys() if num_in_edges[key] == 0],
                key=lambda item: item[1],
            )
        )

        while nodes:
            # Remove the next node, n, from the queue and yield it
            depth, n_key = nodes.pop()
            yield (depth, self.nodes[n_key])

            # Remove an in-edge from every node, m, pointed to by an
            # out-edge from n.  If any of those nodes are left with
            # 0 remaining in-edges, add them to the queue.
            for m in out_edges[n_key]:
                num_in_edges[m] -= 1
                if num_in_edges[m] == 0:
                    nodes.appendleft((depth + 1, m))

    def get_dependencies(self, node: PipelineNode) -> List[PipelineNode]:
        """Returns a list of nodes corresponding to the direct dependencies
        of the given node."""
        return [self.nodes[k] for k in node.children]


class SpackCIConfig:
    """Spack CI object used to generate intermediate representation
    used by the CI generator(s).
    """

    def __init__(self, ci_config):
        """Given the information from the ci section of the config
        and the staged jobs, set up meta data needed for generating Spack
        CI IR.
        """

        self.ci_config = ci_config
        self.named_jobs = ["any", "build", "copy", "cleanup", "noop", "reindex", "signing"]

        self.ir = {
            "jobs": {},
            "rebuild-index": self.ci_config.get("rebuild-index", True),
            "broken-specs-url": self.ci_config.get("broken-specs-url", None),
            "broken-tests-packages": self.ci_config.get("broken-tests-packages", []),
            "target": self.ci_config.get("target", "gitlab"),
        }
        jobs = self.ir["jobs"]

        for name in self.named_jobs:
            # Skip the special named jobs
            if name not in ["any", "build"]:
                jobs[name] = self.__init_job("")

    def __init_job(self, release_spec):
        """Initialize job object"""
        job_object = {"spec": release_spec, "attributes": {}}
        if release_spec:
            job_vars = job_object["attributes"].setdefault("variables", {})
            job_vars["SPACK_JOB_SPEC_DAG_HASH"] = release_spec.dag_hash()
            job_vars["SPACK_JOB_SPEC_PKG_NAME"] = release_spec.name
            job_vars["SPACK_JOB_SPEC_PKG_VERSION"] = release_spec.format("{version}")
            job_vars["SPACK_JOB_SPEC_COMPILER_NAME"] = release_spec.format("{compiler.name}")
            job_vars["SPACK_JOB_SPEC_COMPILER_VERSION"] = release_spec.format("{compiler.version}")
            job_vars["SPACK_JOB_SPEC_ARCH"] = release_spec.format("{architecture}")
            job_vars["SPACK_JOB_SPEC_VARIANTS"] = release_spec.format("{variants}")

        return job_object

    def __is_named(self, section):
        """Check if a pipeline-gen configuration section is for a named job,
        and if so return the name otherwise return none.
        """
        for _name in self.named_jobs:
            keys = [f"{_name}-job", f"{_name}-job-remove"]
            if any([key for key in keys if key in section]):
                return _name

        return None

    @staticmethod
    def __job_name(name, suffix=""):
        """Compute the name of a named job with appropriate suffix.
        Valid suffixes are either '-remove' or empty string or None
        """
        assert isinstance(name, str)

        jname = name
        if suffix:
            jname = f"{name}-job{suffix}"
        else:
            jname = f"{name}-job"

        return jname

    def __apply_submapping(self, dest, spec, section):
        """Apply submapping setion to the IR dict"""
        matched = False
        only_first = section.get("match_behavior", "first") == "first"

        for match_attrs in reversed(section["submapping"]):
            attrs = cfg.InternalConfigScope._process_dict_keyname_overrides(match_attrs)
            for match_string in match_attrs["match"]:
                if _spec_matches(spec, match_string):
                    matched = True
                    if "build-job-remove" in match_attrs:
                        spack.config.remove_yaml(dest, attrs["build-job-remove"])
                    if "build-job" in match_attrs:
                        spack.schema.merge_yaml(dest, attrs["build-job"])
                    break
            if matched and only_first:
                break

        return dest

    # Create jobs for all the pipeline specs
    def init_pipeline_jobs(self, pipeline: PipelineDag):
        for _, node in pipeline.traverse_nodes():
            dag_hash = node.spec.dag_hash()
            self.ir["jobs"][dag_hash] = self.__init_job(node.spec)

    # Generate IR from the configs
    def generate_ir(self):
        """Generate the IR from the Spack CI configurations."""

        jobs = self.ir["jobs"]

        # Implicit job defaults
        defaults = [
            {
                "build-job": {
                    "script": [
                        "cd {env_dir}",
                        "spack env activate --without-view .",
                        "spack ci rebuild",
                    ]
                }
            },
            {"noop-job": {"script": ['echo "All specs already up to date, nothing to rebuild."']}},
        ]

        # Job overrides
        overrides = [
            # Reindex script
            {
                "reindex-job": {
                    "script:": ["spack buildcache update-index --keys {index_target_mirror}"]
                }
            },
            # Cleanup script
            {
                "cleanup-job": {
                    "script:": ["spack -d mirror destroy {mirror_prefix}/$CI_PIPELINE_ID"]
                }
            },
            # Add signing job tags
            {"signing-job": {"tags": ["aws", "protected", "notary"]}},
            # Remove reserved tags
            {"any-job-remove": {"tags": SPACK_RESERVED_TAGS}},
        ]

        pipeline_gen = overrides + self.ci_config.get("pipeline-gen", []) + defaults

        for section in reversed(pipeline_gen):
            name = self.__is_named(section)
            has_submapping = "submapping" in section
            has_dynmapping = "dynamic-mapping" in section
            section = cfg.InternalConfigScope._process_dict_keyname_overrides(section)

            if name:
                remove_job_name = self.__job_name(name, suffix="-remove")
                merge_job_name = self.__job_name(name)
                do_remove = remove_job_name in section
                do_merge = merge_job_name in section

                def _apply_section(dest, src):
                    if do_remove:
                        dest = spack.config.remove_yaml(dest, src[remove_job_name])
                    if do_merge:
                        dest = copy.copy(spack.schema.merge_yaml(dest, src[merge_job_name]))

                if name == "build":
                    # Apply attributes to all build jobs
                    for _, job in jobs.items():
                        if job["spec"]:
                            _apply_section(job["attributes"], section)
                elif name == "any":
                    # Apply section attributes too all jobs
                    for _, job in jobs.items():
                        _apply_section(job["attributes"], section)
                else:
                    # Create a signing job if there is script and the job hasn't
                    # been initialized yet
                    if name == "signing" and name not in jobs:
                        if "signing-job" in section:
                            if "script" not in section["signing-job"]:
                                continue
                            else:
                                jobs[name] = self.__init_job("")
                    # Apply attributes to named job
                    _apply_section(jobs[name]["attributes"], section)

            elif has_submapping:
                # Apply section jobs with specs to match
                for _, job in jobs.items():
                    if job["spec"]:
                        job["attributes"] = self.__apply_submapping(
                            job["attributes"], job["spec"], section
                        )
            elif has_dynmapping:
                mapping = section["dynamic-mapping"]

                dynmap_name = mapping.get("name")

                # Check if this section should be skipped
                dynmap_skip = os.environ.get("SPACK_CI_SKIP_DYNAMIC_MAPPING")
                if dynmap_name and dynmap_skip:
                    if re.match(dynmap_skip, dynmap_name):
                        continue

                # Get the endpoint
                endpoint = mapping["endpoint"]
                endpoint_url = urlparse(endpoint)

                # Configure the request header
                header = {"User-Agent": web_util.SPACK_USER_AGENT}
                header.update(mapping.get("header", {}))

                # Expand header environment variables
                # ie. if tokens are passed
                for value in header.values():
                    value = os.path.expandvars(value)

                verify_ssl = mapping.get("verify_ssl", spack.config.get("config:verify_ssl", True))
                timeout = mapping.get("timeout", spack.config.get("config:connect_timeout", 1))

                required = mapping.get("require", [])
                allowed = mapping.get("allow", [])
                ignored = mapping.get("ignore", [])

                # required keys are implicitly allowed
                allowed = sorted(set(allowed + required))
                ignored = sorted(set(ignored))
                required = sorted(set(required))

                # Make sure required things are not also ignored
                assert not any([ikey in required for ikey in ignored])

                def job_query(job):
                    job_vars = job["attributes"]["variables"]
                    query = (
                        "{SPACK_JOB_SPEC_PKG_NAME}@{SPACK_JOB_SPEC_PKG_VERSION}"
                        # The preceding spaces are required (ref. https://github.com/spack/spack-gantry/blob/develop/docs/api.md#allocation)
                        " {SPACK_JOB_SPEC_VARIANTS}"
                        " arch={SPACK_JOB_SPEC_ARCH}"
                        "%{SPACK_JOB_SPEC_COMPILER_NAME}@{SPACK_JOB_SPEC_COMPILER_VERSION}"
                    ).format_map(job_vars)
                    return f"spec={quote(query)}"

                for job in jobs.values():
                    if not job["spec"]:
                        continue

                    # Create request for this job
                    query = job_query(job)
                    request = Request(
                        endpoint_url._replace(query=query).geturl(), headers=header, method="GET"
                    )
                    try:
                        response = _dyn_mapping_urlopener(
                            request, verify_ssl=verify_ssl, timeout=timeout
                        )
                    except Exception as e:
                        # For now just ignore any errors from dynamic mapping and continue
                        # This is still experimental, and failures should not stop CI
                        # from running normally
                        tty.warn(f"Failed to fetch dynamic mapping for query:\n\t{query}")
                        tty.warn(f"{e}")
                        continue

                    config = json.load(codecs.getreader("utf-8")(response))

                    # Strip ignore keys
                    if ignored:
                        for key in ignored:
                            if key in config:
                                config.pop(key)

                    # Only keep allowed keys
                    clean_config = {}
                    if allowed:
                        for key in allowed:
                            if key in config:
                                clean_config[key] = config[key]
                    else:
                        clean_config = config

                    # Verify all of the required keys are present
                    if required:
                        missing_keys = []
                        for key in required:
                            if key not in clean_config.keys():
                                missing_keys.append(key)

                        if missing_keys:
                            tty.warn(f"Response missing required keys: {missing_keys}")

                    if clean_config:
                        job["attributes"] = spack.schema.merge_yaml(
                            job.get("attributes", {}), clean_config
                        )

        for _, job in jobs.items():
            if job["spec"]:
                job["spec"] = job["spec"].name

        return self.ir


class SpackCIError(spack.error.SpackError):
    def __init__(self, msg):
        super().__init__(msg)
