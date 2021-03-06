#!/usr/bin/python
import argparse
import hashlib
import logging
import os
import re
import shutil
import subprocess

from images import git_util

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

    image += ":" + git_util.GetGitHash()
    subprocess.check_call(["docker", "build", "-t", image,  context_dir])
    logging.info("Built image: %s", image)
    subprocess.check_call(["gcloud", "docker", "--", "push", image])
    logging.info("Pushed image: %s", image)