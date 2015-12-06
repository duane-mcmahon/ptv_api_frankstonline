import pip
from subprocess import call

for dist in pip.get_installed_distributions():
    call("pip install --upgrade --force-reinstall " + dist.project_name, shell=True)
