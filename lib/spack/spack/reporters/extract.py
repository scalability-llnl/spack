# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import re
import xml.sax.saxutils
from datetime import datetime

import llnl.util.tty as tty

from spack.install_test import TestStatus

# The keys here represent the only recognized (ctest/cdash) status values
completed = {
    "failed": "Completed",
    "passed": "Completed",
    "skipped": "Completed",
    "notrun": "No tests to run",
}

log_regexp = re.compile(r"^==> \[([0-9:.\-]*)(?:, [0-9]*)?\] (.*)")
returns_regexp = re.compile(r"\[([0-9 ,]*)\]")

skip_msgs = ["Testing package", "Results for", "Detected the following", "Warning:"]
skip_regexps = [re.compile(r"{0}".format(msg)) for msg in skip_msgs]

status_regexps = [re.compile(r"^({0})".format(str(stat))) for stat in TestStatus]


def add_part_output(part, line):
    if part:
        part["loglines"].append(xml.sax.saxutils.escape(line))


def elapsed(current, previous):
    if not (current and previous):
        return 0

    diff = current - previous
    tty.debug("elapsed = %s - %s = %s" % (current, previous, diff))
    return diff.total_seconds()


def new_part():
    return {
        "command": None,
        "completed": "Unknown",
        "desc": None,
        "elapsed": None,
        "name": None,
        "loglines": [],
        "output": None,
        "status": None,
    }


def process_part_end(part, curr_time, last_time):
    if part:
        if not part["elapsed"]:
            part["elapsed"] = elapsed(curr_time, last_time)

        stat = part["status"]
        if stat in completed:
            if part["completed"] == "Unknown":
                part["completed"] = completed[stat]
        elif stat is None or stat == "unknown":
            part["status"] = "passed"
        part["output"] = "\n".join(part["loglines"])


def timestamp(time_string):
    return datetime.strptime(time_string, "%Y-%m-%d-%H:%M:%S.%f")


def skip(line):
    for regex in skip_regexps:
        match = regex.search(line)
        if match:
            return match


def status(line):
    for regex in status_regexps:
        match = regex.search(line)
        if match:
            stat = match.group(0)
            stat = "notrun" if stat == "NO_TESTS" else stat
            return stat.lower()


def extract_test_parts(default_name, outputs):
    parts = []
    part = {}
    last_time = None
    curr_time = None

    for line in outputs:
        line = line.strip()
        if not line:
            add_part_output(part, line)
            continue

        if skip(line):
            continue

        # The spec was explicitly reported as skipped (e.g., installation
        # failed, package known to have failing tests, won't test external
        # package).
        if line.startswith("Skipped") and line.endswith("package"):
            stat = "skipped"
            part = new_part()
            part["command"] = "Not Applicable"
            part["completed"] = completed[stat]
            part["elapsed"] = 0.0
            part["loglines"].append(line)
            part["name"] = default_name
            part["status"] = "notrun"
            parts.append(part)
            continue

        # Process Spack log messages
        if line.find("==>") != -1:
            match = log_regexp.search(line)
            if match:
                curr_time = timestamp(match.group(1))
                msg = match.group(2)

                # Skip logged message for caching build-time data
                if msg.startswith("Installing"):
                    continue

                # Terminate without further parsing if no more test messages
                if "Completed testing" in msg:
                    # Process last lingering part IF it didn't generate status
                    process_part_end(part, curr_time, last_time)
                    return parts

                # New test parts start "test: <name>: <desc>".
                if msg.startswith("test: "):
                    # Update the last part processed
                    process_part_end(part, curr_time, last_time)

                    part = new_part()
                    desc = msg.split(":")
                    part["name"] = desc[1].strip()
                    part["desc"] = ":".join(desc[2:]).strip()
                    parts.append(part)

                # There is no guarantee of a 1-to-1 mapping of a test part and
                # a (single) command (or executable) since the introduction of
                # PR 34236.
                #
                # Note that tests where the package does not save the output
                # (e.g., output=str.split, error=str.split) will not have
                # a command printed to the test log.
                elif msg.startswith("'") and msg.endswith("'"):
                    if part:
                        if part["command"]:
                            part["command"] += "; " + msg.replace("'", "")
                        else:
                            part["command"] = msg.replace("'", "")
                    else:
                        part = new_part()
                        part["command"] = msg.replace("'", "")

                else:
                    # Update the last part processed since a new log message
                    # means a non-test action
                    process_part_end(part, curr_time, last_time)

            else:
                tty.debug("Did not recognize test output '{0}'".format(line))

            # Each log message potentially represents a new test part so
            # save off the last timestamp
            last_time = curr_time
            continue

        # Check for status values
        stat = status(line)
        if stat:
            if part:
                part["status"] = stat
                add_part_output(part, line)
            else:
                tty.warn("No part to add status from '{0}'".format(line))
            continue

        add_part_output(part, line)

    # Process the last lingering part IF it didn't generate status
    process_part_end(part, curr_time, last_time)

    # If no parts, create a skeleton to flag that the tests are not run
    if not parts:
        part = new_part()
        stat = "failed" if outputs[0].startswith("Cannot open log") else "notrun"

        part["command"] = "unknown"
        part["completed"] = completed[stat]
        part["elapsed"] = 0.0
        part["name"] = default_name
        part["status"] = stat
        part["output"] = "\n".join(outputs)
        parts.append(part)

    return parts
