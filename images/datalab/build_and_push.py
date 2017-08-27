#!/usr/bin/python
import argparse
import hashlib
import logging
import os
import re
import shutil
import subprocess


def GetGitHash():
    # The image tag is based on the githash.
    git_hash = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"])
    git_hash=git_hash.strip()
    modified_files = subprocess.check_output(["git", "ls-files", "--modified"])
    untracked_files = subprocess.check_output(["git", "ls-files", "--others", "--exclude-standard"])
    if modified_files or untracked_files:
        diff= subprocess.check_output(["git", "diff"])
        sha = hashlib.sha256()
        sha.update(diff)
        diffhash = sha.hexdigest()[0:7]
        git_hash = "{0}-dirty-{1}".format(git_hash, diffhash)
    return git_hash

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser(
        description='Build Dockerfile for cmle-example Datalab.')
    parser.add_argument(
        '--project',
        default="dataflow-jlewi",
        type = str,
        help='The project to use for the GCR registry.')

    args = parser.parse_args()

    this_file = __file__
    filename = "Dockerfile"
    images_dir = os.path.dirname(this_file)

    context_dir = images_dir
    logging.info("context_dir: %s", context_dir)
    if not os.path.exists(context_dir):
        os.makedirs(context_dir)
    dockerfile = os.path.join(context_dir, 'Dockerfile')

    image = "gcr.io/{0}/cmle-example-datalab".format(args.project)

    image += ":" + GetGitHash()
    subprocess.check_call(["docker", "build", "-t", image,  context_dir])
    logging.info("Built image: %s", image)
    subprocess.check_call(["gcloud", "docker", "--", "push", image])
    logging.info("Pushed image: %s", image)