import os

from lundy.datasets import LundyProject
from sample_project_dir.sample_class import SampleClass

dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(dir_path, 'sample_project_dir')
project = LundyProject("Lundy")
project.scan(project_dir)



import requests

def send_project_version():
    url = 'http://127.0.0.1:8000/api/lundy_objects/'
    data = {'type': 'project', 'data': project.to_json(), 'hash': project.hash, 'id': 4}
    requests.post(url, json=data)

def send_test_run_of_method():
    sample_run = SampleClass('a', 'b')
    sample_run.sample_method_with_args('a', 'b')

# send_project_version()
send_test_run_of_method()

