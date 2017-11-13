import os

from lundy.datasets import LundyProject

dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(dir_path, 'sample_project_dir')
project = LundyProject("Lundy")
project.scan(project_dir)

import requests
url = 'http://127.0.0.1:8000/api/lundy_objects/'
data = {'data': project.to_json(), 'hash': project.hash, 'id':2}
requests.post(url, json=data)


