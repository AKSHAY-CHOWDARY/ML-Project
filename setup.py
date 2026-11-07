## Helps to build the whole project into a package
from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .' # The HYPHEN_E_DOT will automaticaly run the setup.py file. Its basically an indication that we have a setup.py file.
## you can just run requirements.txt and it will automatically execute setup.py
def get_requirements(file_path:str) -> List[str]:
    ''' This function will return list of requirements '''
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.strip() for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
    return requirements

            

        
setup(
    name='mlproject',
    version="0.0.1",
    author='Akshay',
    author_email="k.v.akshay111@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)