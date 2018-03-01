import argparse
import os
import urllib

from datasets import LundyProject
import requests

def parse_config_file(config_path):
    config_parameters = ('login', 'password', 'project_name', '')
    with open(config_path) as f:
        for line in f:
            command = line[:-1]
            command = command.split('=')
            if command[0] == 'project_source':
                project_src = command[1]
    user = urllib.quote("lunni")
    password = urllib.quote("afhJKH#$H@saC*&(")
    dir_path = os.getcwd()
    project_src = os.path.join(dir_path, project_src)
    return project_src


def send_project_version():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    project_dir = os.path.join(dir_path, 'sample_project_dir')
    project = LundyProject("Lundy")
    project.scan(project_dir)
    url = 'http://127.0.0.1:8000/api/lundy_objects/'
    data = {'type': 'project', 'data': project.to_json(), 'hash': project.hash, 'id': 4}
    requests.post(url, json=data)

def collect():
    dir_path = os.getcwd()
    lundy_config_path = os.path.join(dir_path, '.lunni')
    if os.path.exists(lundy_config_path):
        project_src = parse_config_file(lundy_config_path)
    else:
        raise("Please provide .lunni config file")
    project = LundyProject("Lundy")
    project.scan(project_src)
    print("DATA COLLECTED")
    return project.to_json()

def main():
    """Main function for using Lundy agent"""
    parser = argparse.ArgumentParser(
        usage="test")
    parser.add_argument(
        "-c",
        "--collect",
        action="store_true",
        help=
        "")
    parser.add_argument(
        "-p",
        "--push",
        action="store_true",
        default=False,
        help=
        "")
    args = parser.parse_args()
    if args.collect:
        collect()
    if args.push:
        print "push"

if __name__ == "__main__":
  main()