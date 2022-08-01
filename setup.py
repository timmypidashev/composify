from setuptools import setup
import re

requirements = []
with open('requirements.txt') as file:
    requirements = file.read().splitlines()

version = ''
with open('gpm/__init__.py') as file:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

readme = ''
with open('README.md') as file:
    readme = file.read()
  
extras_require = {
    'test': [
      'pytest'
    ]
}

setup(
    name='git-project-manager',
    url='https://github.com/timmypidashev/gpm',
    project_urls={
        'Issues': 'https://github.com/timmypidashev/gpm/issues',
        'Releases': 'https://github.com/timmypidashev/gpm/releases'
    },
    version=version,
    license='MIT',
    description='Git Project Manager(GPM)',
    long_description=readme,
    long_description_content_type='text/md',
    python_requires='>=3.8.0',
    classifiers=[
        'Development Status :: Development/Prerelease',
        'License :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
      ]

)