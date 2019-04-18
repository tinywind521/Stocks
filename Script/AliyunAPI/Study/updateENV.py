##################################
# 更新Anaconda
# conda update conda
# 更新所有包
# conda update --all
##################################
import pip
from subprocess import call
for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)