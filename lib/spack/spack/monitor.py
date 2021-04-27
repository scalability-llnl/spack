# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Interact with a Spack Monitor Service. Derived from
https://github.com/spack/spack-monitor/blob/main/script/spackmoncli.py
"""

import base64
import os
import re

try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib2 import urlopen, Request, URLError  # type: ignore  # novm

import spack
import spack.hash_types as ht
import spack.main
import spack.store
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import llnl.util.tty as tty
from copy import deepcopy


# A global client to instantiate once
cli = None


def get_client(host, prefix="ms1", disable_auth=False, allow_fail=False):
    """
    Get a monitor client for a particular host and prefix.

    If the client is not running, we exit early, unless allow_fail is set
    to true, indicating that we should continue the build even if the
    server is not present. Note that this client is defined globally as "cli"
    so we can istantiate it once (checking for credentials, etc.) and then
    always have access to it via spack.monitor.cli. Also note that
    typically, we call the monitor by way of hooks in spack.hooks.monitor.
    So if you want the monitor to have a new interaction with some part of
    the codebase, it's recommended to write a hook first, and then have
    the monitor use it.
    """
    global cli
    cli = SpackMonitorClient(host=host, prefix=prefix, allow_fail=allow_fail)

    # If we don't disable auth, environment credentials are required
    if not disable_auth:
        cli.require_auth()

    # We will exit early if the monitoring service is not running
    info = cli.service_info()

    # If we allow failure, the response will be done
    if info:
        tty.debug("%s v.%s has status %s" % (
            info['id'],
            info['version'],
            info['status'])
        )
        return cli

    else:
        tty.debug("spack-monitor server not found, continuing as allow_fail is True.")


def get_monitor_group(subparser):
    """
    Retrieve the monitor group for the argument parser.

    Since the monitor group is shared between commands, we provide a common
    function to generate the group for it. The user can pass the subparser, and
    the group is added, and returned.
    """
    # Monitoring via https://github.com/spack/spack-monitor
    monitor_group = subparser.add_argument_group()
    monitor_group.add_argument(
        '--monitor', action='store_true', dest='use_monitor', default=False,
        help="interact with a montor server during builds.")
    monitor_group.add_argument(
        '--monitor-no-auth', action='store_true', dest='monitor_disable_auth',
        default=False, help="the monitoring server does not require auth.")
    monitor_group.add_argument(
        '--monitor-keep-going', action='store_true', dest='monitor_keep_going',
        default=False, help="continue the build if a request to monitor fails.")
    monitor_group.add_argument(
        '--monitor-host', dest='monitor_host', default="http://127.0.0.1",
        help="If using a monitor, customize the host.")
    monitor_group.add_argument(
        '--monitor-prefix', dest='monitor_prefix', default="ms1",
        help="The API prefix for the monitor service.")
    return monitor_group


class SpackMonitorClient:
    """Client to interact with a spack monitor server.

    We require the host url, along with the prefix to discover the
    service_info endpoint. If allow_fail is set to True, we will not exit
    on error with tty.die given that a request is not successful. The spack
    version is one of the fields to uniquely identify a spec, so we add it
    to the client on init.
    """

    def __init__(self, host=None, prefix="ms1", allow_fail=False):
        self.host = host or "http://127.0.0.1"
        self.baseurl = "%s/%s" % (self.host, prefix.strip("/"))
        self.token = os.environ.get("SPACKMON_TOKEN")
        self.username = os.environ.get("SPACKMON_USER")
        self.headers = {}
        self.allow_fail = allow_fail
        self.spack_version = spack.main.get_version()
        self.capture_build_environment()

        # We keey lookup of build_id by full_hash
        self.build_ids = {}

    def load_build_environment(self, spec):
        """
        Load a build environment from install_environment.json.

        If we are running an analyze command, we will need to load previously
        used build environment metadata from install_environment.json to capture
        what was done during the build.
        """
        if not hasattr(spec, "package") or not spec.package:
            tty.die("A spec must have a package to load the environment.")

        pkg_dir = os.path.dirname(spec.package.install_log_path)
        env_file = os.path.join(pkg_dir, "install_environment.json")
        build_environment = read_json(env_file)
        if not build_environment:
            tty.warning(
                "install_environment.json not found in package folder. "
                " This means that the current environment metadata will be used."
            )
        else:
            self.build_environment = build_environment

    def capture_build_environment(self):
        """
        Capture the environment for the build.

        This uses spack.util.environment.get_host_environment_metadata to do so.
        This is important because it's a unique identifier, along with the spec,
        for a Build. It should look something like this:

        {'host_os': 'ubuntu20.04',
         'platform': 'linux',
         'host_target': 'skylake',
         'hostname': 'vanessa-ThinkPad-T490s',
         'spack_version': '0.16.1-1455-52d5b55b65',
         'kernel_version': '#73-Ubuntu SMP Mon Jan 18 17:25:17 UTC 2021'}

        This is saved to a package install's metadata folder as
        install_environment.json, and can be loaded by the monitor for uploading
        data relevant to a later analysis.
        """
        from spack.util.environment import get_host_environment_metadata
        self.build_environment = get_host_environment_metadata()

    def require_auth(self):
        """
        Require authentication.

        The token and username must not be unset
        """
        if not self.token or not self.username:
            tty.die("You are required to export SPACKMON_TOKEN and SPACKMON_USER")

    def set_header(self, name, value):
        self.headers.update({name: value})

    def set_basic_auth(self, username, password):
        """
        A wrapper to adding basic authentication to the Request
        """
        auth_str = "%s:%s" % (username, password)
        auth_header = base64.b64encode(auth_str.encode("utf-8"))
        self.set_header("Authorization", "Basic %s" % auth_header.decode("utf-8"))

    def reset(self):
        """
        Reset and prepare for a new request.
        """
        if "Authorization" in self.headers:
            self.headers = {"Authorization": self.headers['Authorization']}
        else:
            self.headers = {}

    def prepare_request(self, endpoint, data, headers):
        """
        Prepare a request given an endpoint, data, and headers.

        If data is provided, urllib makes the request a POST
        """
        # Always reset headers for new request.
        self.reset()

        headers = headers or {}

        # The calling function can provide a full or partial url
        if not endpoint.startswith("http"):
            endpoint = "%s/%s" % (self.baseurl, endpoint)

        # If we have data, the request will be POST
        if data:
            if not isinstance(data, str):
                data = sjson.dump(data)
            data = data.encode('ascii')

        return Request(endpoint, data=data, headers=headers)

    def issue_request(self, request, retry=True):
        """
        Given a prepared request, issue it.

        If we get an error, die. If
        there are times when we don't want to exit on error (but instead
        disable using the monitoring service) we could add that here.
        """
        try:
            response = urlopen(request)
        except URLError as e:

            # If we have an authorization request, retry once with auth
            if e.code == 401 and retry:
                if self.authenticate_request(e):
                    request = self.prepare_request(
                        e.url,
                        sjson.load(request.data.decode('utf-8')),
                        self.headers
                    )
                    return self.issue_request(request, False)

            # Otherwise, relay the message and exit on error
            msg = ""
            if hasattr(e, 'reason'):
                msg = e.reason
            elif hasattr(e, 'code'):
                msg = e.code

            if self.allow_fail:
                tty.warning("Request to %s was not successful, but continuing." % e.url)
                return

            tty.die(msg)

        return response

    def do_request(self, endpoint, data=None, headers=None, url=None):
        """
        Do the actual request.

        If data is provided, it is POST, otherwise GET.
        If an entire URL is provided, don't use the endpoint
        """
        request = self.prepare_request(endpoint, data, headers)

        # If we have an authorization error, we retry with
        response = self.issue_request(request)

        # A 200/201 response incidates success
        if response.code in [200, 201]:
            return sjson.load(response.read().decode('utf-8'))

        return response

    def authenticate_request(self, originalResponse):
        """
        Authenticate the request.

        Given a response (an HTTPError 401), look for a Www-Authenticate
        header to parse. We return True/False to indicate if the request
        should be retried.
        """
        authHeaderRaw = originalResponse.headers.get("Www-Authenticate")
        if not authHeaderRaw:
            return False

        # If we have a username and password, set basic auth automatically
        if self.token and self.username:
            self.set_basic_auth(self.username, self.token)

        headers = deepcopy(self.headers)
        if "Authorization" not in headers:
            tty.error(
                "This endpoint requires a token. Please set "
                "client.set_basic_auth(username, password) first "
                "or export them to the environment."
            )
            return False

        # Prepare request to retry
        h = parse_auth_header(authHeaderRaw)
        headers.update({
            "service": h.Service,
            "Accept": "application/json",
            "User-Agent": "spackmoncli"}
        )

        # Currently we don't set a scope (it defaults to build)
        authResponse = self.do_request(h.Realm, headers=headers)

        # Request the token
        token = authResponse.get("token")
        if not token:
            return False

        # Set the token to the original request and retry
        self.headers.update({"Authorization": "Bearer %s" % token})
        return True

    # Functions correspond to endpoints
    def service_info(self):
        """
        Get the service information endpoint
        """
        # Base endpoint provides service info
        return self.do_request("")

    def new_configuration(self, specs):
        """
        Given a list of specs, generate a new configuration for each.

        We return a lookup of specs with their package names. This assumes
        that we are only installing one version of each package. We aren't
        starting or creating any builds, so we don't need a build environment.
        """
        configs = {}

        # There should only be one spec generally (what cases would have >1?)
        for spec in specs:
            # Not sure if this is needed here, but I see it elsewhere
            if spec.name in spack.repo.path or spec.virtual:
                spec.concretize()
            as_dict = {"spec": spec.to_dict(hash=ht.full_hash),
                       "spack_version": self.spack_version}
            response = self.do_request("specs/new/", data=sjson.dump(as_dict))
            configs[spec.package.name] = response.get('data', {})
        return configs

    def new_build(self, spec):
        """
        Create a new build.

        This means sending the hash of the spec to be built,
        along with the build environment. These two sets of data uniquely can
        identify the build, and we will add objects (the binaries produced) to
        it. We return the build id to the calling client.
        """
        return self.get_build_id(spec, return_response=True)

    def get_build_id(self, spec, return_response=False, spec_exists=True):
        """
        Retrieve a build id, either in the local cache, or query the server.
        """
        full_hash = spec.full_hash()
        if full_hash in self.build_ids:
            return self.build_ids[full_hash]

        # Prepare build environment data (including spack version)
        data = self.build_environment.copy()
        data['full_hash'] = full_hash

        # If we allow the spec to not exist (meaning we create it) we need to
        # include the full spec.yaml here
        if not spec_exists:
            meta_dir = os.path.dirname(spec.package.install_log_path)
            spec_file = os.path.join(meta_dir, "spec.yaml")
            data['spec'] = syaml.load(read_file(spec_file))

        response = self.do_request("builds/new/", data=sjson.dump(data))

        # Add the build id to the lookup
        bid = self.build_ids[full_hash] = response['data']['build']['build_id']
        self.build_ids[full_hash] = bid

        # If the function is called directly, the user might want output
        if return_response:
            return response
        return bid

    def update_build(self, spec, status="SUCCESS"):
        """
        Update a build with a new status.

        This typically updates the relevant package to indicate a
        successful install. This endpoint can take a general status to update.
        """
        data = {"build_id": self.get_build_id(spec), "status": status}
        return self.do_request("builds/update/", data=sjson.dump(data))

    def fail_task(self, spec):
        """Given a spec, mark it as failed. This means that Spack Monitor
        marks all dependencies as cancelled, unless they are already successful
        """
        return self.update_build(spec, status="FAILED")

    def send_analyze_metadata(self, pkg, metadata):
        """
        Send spack analyzer metadata to the spack monitor server.

        Given a dictionary of analyzers (with key as analyzer type, and
        value as the data) upload the analyzer output to Spack Monitor.
        Spack Monitor should either have a known understanding of the analyzer,
        or if not (the key is not recognized), it's assumed to be a dictionary
        of objects/files, each with attributes to be updated. E.g.,

        {"analyzer-name": {"object-file-path": {"feature1": "value1"}}}
        """
        # Prepare build environment data (including spack version)
        # Since the build might not have been generated, we include the spec
        data = {"build_id": self.get_build_id(pkg.spec, spec_exists=False),
                "metadata": metadata}
        return self.do_request("analyze/builds/", data=sjson.dump(data))

    def send_phase(self, pkg, phase_name, phase_output_file, status):
        """
        Send the result of a phase during install.

        Given a package, phase name, and status, update the monitor endpoint
        to alert of the status of the stage. This includes parsing the package
        metadata folder for phase output and error files
        """
        data = {"build_id": self.get_build_id(pkg.spec)}

        # Send output specific to the phase (does this include error?)
        data.update({"status": status,
                     "output": read_file(phase_output_file),
                     "phase_name": phase_name})

        return self.do_request("builds/phases/update/", data=sjson.dump(data))

    def upload_specfile(self, filename):
        """
        Upload a spec file to the spack monitor server.

        Given a spec file (must be json) upload to the UploadSpec endpoint.
        This function is not used in the spack to server workflow, but could
        be useful is Spack Monitor is intended to send an already generated
        file in some kind of separate analysis. For the environment file, we
        parse out SPACK_* variables to include.
        """
        # We load as json just to validate it
        spec = read_json(filename)
        data = {"spec": spec, "spack_verison": self.spack_version}
        return self.do_request("specs/new/", data=sjson.dump(data))


# Helper functions

def parse_auth_header(authHeaderRaw):
    """
    Parse an authentication header into relevant pieces
    """
    regex = re.compile('([a-zA-z]+)="(.+?)"')
    matches = regex.findall(authHeaderRaw)
    lookup = dict()
    for match in matches:
        lookup[match[0]] = match[1]
    return authHeader(lookup)


class authHeader:
    def __init__(self, lookup):
        """Given a dictionary of values, match them to class attributes"""
        for key in lookup:
            if key in ["realm", "service", "scope"]:
                setattr(self, key.capitalize(), lookup[key])


def read_file(filename):
    """
    Read a file, if it exists. Otherwise return None
    """
    if not os.path.exists(filename):
        return
    with open(filename, 'r') as fd:
        content = fd.read()
    return content


def write_file(content, filename):
    """
    Write content to file
    """
    with open(filename, 'w') as fd:
        fd.writelines(content)
    return content


def write_json(obj, filename):
    """
    Write a json file, if the output directory exists.
    """
    if not os.path.exists(os.path.dirname(filename)):
        return
    return write_file(sjson.dump(obj), filename)


def read_json(filename):
    """
    Read a file and load into json, if it exists. Otherwise return None.
    """
    if not os.path.exists(filename):
        return
    return sjson.load(read_file(filename))
