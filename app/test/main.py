import os

from app.datasets import LundyProject

dir_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.join(dir_path, 'sample_project_dir')
project = LundyProject("Lundy", project_dir)
project.scan()
print("")
print(project.__dict__)