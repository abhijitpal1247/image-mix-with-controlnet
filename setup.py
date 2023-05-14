from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='image_mix_with_controlnet',
      version='0.1',
      description='Testing installation of Package',
      url='#',
      author='auth',
      author_email='author@email.com',
      install_requires=required,
      license='MIT',
      packages=['src'],
      zip_safe=False)
