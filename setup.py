try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='SimplSale',
    version="0.1",
    #description='',
    #author='',
    #author_email='',
    #url='',
    install_requires=[
    "Pylons >= 0.9.6.1",
    'lxml >= 2.0alpha5',
    'PyFlowPro >= 0.1dev',
    'ZipLookup >= 0.1dev',
    ],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'simplsale': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors = {'simplsale': [
    #        ('**.py', 'python', None),
    #        ('templates/**.mako', 'mako', None),
    #        ('public/**', 'ignore', None)]},
    entry_points="""
    [paste.app_factory]
    main = simplsale.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller

    [simplsale.commerce]
    mock = simplsale.plugins.commerce:MockCommerce

    [simplsale.email]
    inline = simplsale.plugins.email:InlineEmail
    mock = simplsale.plugins.email:MockEmail
    smtp = simplsale.plugins.email:SmtpEmail
    """,
)
