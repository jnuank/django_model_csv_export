from setuptools import setup

setup(
    name='django_model_export',
    version='0.0.4',
    packages=['model_export', 'model_export.management', 'model_export.management.commands', 'model_export.migrations'],
    url='',
    license='',
    author='jnuank',
    author_email='ikuta1919@gmail.com',
    description='',
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    model_export_help = model_export.test:main
    """,
)
