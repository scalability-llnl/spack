# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Interact with a Spack Monitor Service. Derived from
https://github.com/spack/spack-monitor/blob/main/script/spackmoncli.py
"""

import base64
import json
import os
import platform
import re

try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError
except ImportError:
    from urllib2 import urlopen, Request, URLError  # noqa

import spack
import spack.hash_types as ht
import spack.main
import spack.store
import llnl.util.tty as tty
from copy import deepcopy


def get_client(host, prefix="ms1", disable_auth=False, allow_fail=False):
    """a common function to get a client for a particular host and prefix.
    If the client is not running, we exit early, unless allow_fail is set
    to true, indicating that we should continue the build even if the
    server is not present.
    """
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


class SpackMonitorClient:
    """The SpackMonitorClient is a handle to interact with a spack monitor
    server. We require the host url, along with the prefix to discover the
    service_info endpoint. If allow_fail is set to True, we will not exit
    on error with tty.fail given that a request is not successful. The spack
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

    def capture_build_environment(self):
        """Use spack.environment._get_host_environment to capture the
        environment for the build. This is important because it's a unique
        identifier, along with the spec, for a Build. It should look something
        like this:

        {'target': 'skylake',
         'os': 'ubuntu20.04',
         'platform': 'linux',
         'arch': arch=linux-ubuntu20.04-skylake,
         'architecture': arch=linux-ubuntu20.04-skylake,
         'arch_str': 'linux-ubuntu20.04-skylake',
         'hostname': 'superman-computer',
         'kernel_version': '#73-Ubuntu SMP Mon Jan 18 17:25:17 UTC 2021'}
        """
        from spack.environment import _get_host_environment
        self.build_environment = _get_host_environment()
        self.build_environment['kernel_version'] = platform.version()

    def _get_build_environment(self):
        return {"host_os": self.build_environment['os'],
                "platform": self.build_environment['platform'],
                "host_target": self.build_environment['target'],
                "hostname": self.build_environment['hostname'],
                "kernel_version": self.build_environment['kernel_version'],
                "spack_version": self.spack_version}

    def require_auth(self):
        """Require authentication, meaning that the token and username must
        not be unset
        """
        if not self.token or not self.username:
            tty.die("You are required to export SPACKMON_TOKEN and SPACKMON_USER")

    def set_header(self, name, value):
        self.headers.update({name: value})

    def set_basic_auth(self, username, password):
        """A wrapper to adding basic authentication to the Request"""
        auth_str = "%s:%s" % (username, password)
        auth_header = base64.b64encode(auth_str.encode("utf-8"))
        self.set_header("Authorization", "Basic %s" % auth_header.decode("utf-8"))

    def reset(self):
        """Reset and prepare for a new request.
        """
        if "Authorization" in self.headers:
            self.headers = {"Authorization": self.headers['Authorization']}
        else:
            self.headers = {}

    def prepare_request(self, endpoint, data, headers):
        """Given an endpoint url and data, prepare the request. If data
        is provided, urllib makes the request a POST
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
                data = json.dumps(data)
            data = data.encode('ascii')

        return Request(endpoint, data=data, headers=headers)

    def issue_request(self, request, retry=True):
        """Given a prepared request, issue it. If we get an error, die. If
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
                        json.loads(request.data),
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
        """Do a request. If data is provided, it is POST, otherwise GET.
        If an entire URL is provided, don't use the endpoint
        """
        request = self.prepare_request(endpoint, data, headers)

        # If we have an authorization error, we retry with
        response = self.issue_request(request)

        # A 200/201 response incidates success
        if response.code in [200, 201]:
            return json.loads(response.read().decode('utf-8'))

        return response

    def authenticate_request(self, originalResponse):
        """Given a response (an HTTPError 401), look for a Www-Authenticate
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
        """get the service information endpoint"""
        # Base endpoint provides service info
        return self.do_request("")

    def new_configuration(self, specs):
        """Given a list of specs, generate a new configuration for each. We
        return a lookup of specs with their package names. This assumes
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
            response = self.do_request("specs/new/", data=json.dumps(as_dict))
            configs[spec.package.name] = response.get('data', {})
        return configs

    def new_build(self, spec):
        """Create a new build, meaning sending the hash of the spec to be built,
        along with the build environment. These two sets of data uniquely can
        identify the build, and we will add objects (the binaries produced) to
        it. We return the build id to the calling client.
        """
        full_hash = spec.full_hash()
        return self.get_build_id(full_hash, return_response=True)

    def get_build_id(self, full_hash, return_response=False):
        """Retrieve a build id, either in the local cache, or query the server
        """
        if full_hash in self.build_ids:
            return self.build_ids[full_hash]

        # Prepare build environment data (including spack version)
        data = self._get_build_environment()
        data['full_hash'] = full_hash
        response = self.do_request("builds/new/", data=json.dumps(data))

        # Add the build id to the lookup
        bid = self.build_ids[full_hash] = response['data']['build']['build_id']
        self.build_ids[full_hash] = bid

        # If the function is called directly, the user might want output
        if return_response:
            return response
        return bid

    def update_build(self, spec, status="SUCCESS"):
        """update task will just update the relevant package to indicate a
        successful install. Unlike cancel_task that sends a cancalled request
        to the main package, here we don't need to cancel or otherwise update any
        other statuses. This endpoint can take a general status to update just
        one
        """
        full_hash = spec.full_hash()
        data = {"build_id": self.get_build_id(full_hash), "status": status}
        return self.do_request("builds/update/", data=json.dumps(data))

    def fail_task(self, spec):
        """Given a spec, mark it as failed. This means that Spack Monitor
        marks all dependencies as cancelled, unless they are already successful
        """
        return self.update_build(spec, status="FAILED")

    def send_final(self, pkg):
        """Given a metadata folder, usually .spack within the spack root
        opt/<system>/<compiler>/<package>/.spack with the following:

             'spack-configure-args.txt',
             'spack-build-env.txt',
             'spec.yaml',
             'archived-files',
             'spack-build-out.txt',
             'install_manifest.json',
             'repos'

        read in all metadata files except for phase and output (which are sent
        as they are generated with the phase) and send to the monitor server.
        """

        # Prepare build environment data (including spack version)
        data = {"build_id": self.get_build_id(pkg.spec.full_hash())}

        meta_dir = os.path.dirname(pkg.install_log_path)
        env_file = os.path.join(meta_dir, "spack-build-env.txt")
        config_file = os.path.join(meta_dir, "spack-configure-args.txt")
        manifest_file = os.path.join(meta_dir, "install_manifest.json")

        metadata = {"environ": self._read_environment_file(env_file),
                    "config": read_file(config_file),
                    "manifest": read_json(manifest_file)}

        data['metadata'] = metadata
        return self.do_request("builds/metadata/", data=json.dumps(data))

    def send_phase(self, pkg, phase_name, phase_output_file, status):
        """Given a package, phase name, and status, update the monitor endpoint
        to alert of the status of the stage. This includes parsing the package
        metadata folder for phase output and error files
        """
        data = {"build_id": self.get_build_id(pkg.spec.full_hash())}

        # Send output specific to the phase (does this include error?)
        data.update({"status": status,
                     "output": read_file(phase_output_file),
                     "phase_name": phase_name})

        return self.do_request("builds/phases/update/", data=json.dumps(data))

    def _read_environment_file(self, filename):
        """Given an environment file, we want to read it, split by semicolons
        and new lines, and then parse down to the subset of SPACK_* variables.
        We assume that all spack prefix variables are not secrets, and unlike
        the install_manifest.json, we don't (at least to start) parse the values
        to remove path prefixes specific to user systems.
        """
        if not os.path.exists(filename):
            return
        content = read_file(filename)

        # Filter down to lines, not export statements. I'm only using multiple
        # lines because of the length limit.
        lines = re.split("(;|\n)", content)
        lines = [x for x in lines if x not in ['', '\n', ';'] and "SPACK_" in x]
        lines = [x.strip() for x in lines if "export " not in x]
        lines = [x.strip() for x in lines if "export " not in x]
        return {x.split("=", 1)[0]: x.split("=", 1)[1] for x in lines}

    def upload_specfile(self, filename):
        """Given a spec file (must be json) upload to the UploadSpec endpoint.
        This function is not used in the spack to server workflow, but could
        be useful is Spack Monitor is intended to send an already generated
        file in some kind of separate analysis. For the environment file, we
        parse out SPACK_* variables to include.
        """
        # We load as json just to validate it
        spec = read_json(filename)
        data = {"spec": spec, "spack_verison": self.spack_version}
        return self.do_request("specs/new/", data=json.dumps(data))


# Helper functions

def parse_auth_header(authHeaderRaw):
    """parse authentication header into pieces"""
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
    """Read a file, if it exists. Otherwise return None
    """
    if not os.path.exists(filename):
        return
    with open(filename, 'r') as fd:
        content = fd.read()
    return content


def read_json(filename):
    """Read a file and load into json, if it exists. Otherwise return None"""
    if not os.path.exists(filename):
        return
    return json.loads(read_file(filename))
