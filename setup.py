from setuptools import setup, find_packages

setup(name='pddlgym_planners',
      version='0.0.1',
      install_requires=['numpy'],
      packages=find_packages(),
      include_package_data=True,
)
