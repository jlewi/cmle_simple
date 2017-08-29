#!/usr/bin/python
import argparse
import hashlib
import logging
import os
import re
import shutil
import subprocess
import tempfile

from images import git_util

def IgnorePyc(_, names):
  ignore = [n for n in names if n.endswith('.pyc')]
  return ignore


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
    root_dir = os.path.abspath(os.path.join(images_dir, os.pardir, os.pardir))
    context_dir =  tempfile.mkdtemp(prefix='tmp_cmle_example_context')
    logging.info("context_dir: %s", context_dir)
    if not os.path.exists(context_dir):
        os.makedirs(context_dir)

    cmle_source = os.path.join(root_dir, 'cmle_example')
    shutil.copytree(cmle_source, os.path.join(context_dir, 'cmle_example'), ignore=IgnorePyc)
    shutil.copyfile(os.path.join(root_dir, 'setup.py'), os.path.join(context_dir, 'setup.py'))


    subprocess.check_call(['python', 'setup.py', 'sdist'], cwd=context_dir)
    pip_file = 'cmle_example-0.1.1.tar.gz'
    shutil.copyfile(os.path.join(context_dir, 'dist', pip_file),
                    os.path.join(context_dir, pip_file))

    # Copy files from source directory
    for f in ['Dockerfile']:
      shutil.copyfile(os.path.join(images_dir, f), os.path.join(context_dir, f))

    image = "gcr.io/{0}/cmle-example".format(args.project)

    image += ":" + git_util.GetGitHash()
    subprocess.check_call(["docker", "build", "-t", image,  context_dir])
    logging.info("Built image: %s", image)
    subprocess.check_call(["gcloud", "docker", "--", "push", image])
    logging.info("Pushed image: %s", image)