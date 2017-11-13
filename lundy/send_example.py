import os

from lundy.datasets import LundyProject

dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(dir_path, 'test', 'sample_project_dir')
project = LundyProject("Lundy")
project.scan(project_dir)
print("")
print(project.__dict__)