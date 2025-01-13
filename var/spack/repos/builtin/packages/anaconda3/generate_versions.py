#!/usr/bin/env python3

import json
import os
import re
import sys

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "anaconda-archive.dat")
output_file = os.path.join(script_dir, "versions.json")

# Regular expression patterns
anaconda_pattern = r"(Anaconda3-([0-9.-]+)-(Windows|Linux|MacOSX)-([^.]+)\.(sh|exe|pkg))"
sha256_pattern = r"([a-fA-F0-9]{64})"
platform_map = {"Linux": "linux", "MacOSX": "darwin", "Windows": "windows"}

ERROR_PKG_NOT_SUPPORTED = ValueError("pkg files are not supported")
ERROR_NO_MATCH_FOUND = ValueError("No match found")


def re_match_line(line):
    filename_match = re.search(anaconda_pattern, line)
    sha256_match = re.search(sha256_pattern, line)
    if filename_match and sha256_match:
        ext = filename_match.group(5)
        if ext == "pkg":
            raise ERROR_PKG_NOT_SUPPORTED
        installer_name = filename_match.group(1)
        version = filename_match.group(2)
        try:
            platform = platform_map[filename_match.group(3)]
        except KeyError as exc:
            raise ERROR_NO_MATCH_FOUND from exc
        arch = filename_match.group(4)
        sha256 = sha256_match.group(1)
        return platform, arch, version, installer_name, sha256
    raise ERROR_NO_MATCH_FOUND


def generate_versions_json():
    versions = {}
    with open(input_file, "r", encoding="utf-8") as file:
        for n, line in enumerate(file):
            if line.strip().startswith("#") or not line.strip():
                continue
            try:
                platform, arch, version, installer_name, sha256 = re_match_line(line)
                if platform not in versions:
                    versions[platform] = {}
                if arch not in versions[platform]:
                    versions[platform][arch] = {}
                versions[platform][arch][version] = {
                    "version": version,
                    "sha256": sha256,
                    "installer_name": installer_name,
                }
            except ValueError as e:
                if e == ERROR_PKG_NOT_SUPPORTED:
                    continue
                print(f"Ignored line {n}: {line.strip()}", file=sys.stderr)
                continue
    return versions


def main():
    try:
        versions = generate_versions_json()
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(versions, f)
    except FileNotFoundError:
        print(f"Error: File not found at {input_file}")


if __name__ == "__main__":
    main()
