{
    'name': "Mail Domain Management",

    'summary': """
        Module that add extra modification to restrict mail by domain
        """,

    'description': """
        *   add extra modification to restrict mail by domain

    """,

    'author': "Impulso Diagonal",
    'website': "https://impulso.xyz",

    # for the full list
    'category': 'Extra Tools',
    'version': '13.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/mail_domain_management_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml'
    ],
}
