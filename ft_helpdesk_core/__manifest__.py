{
    'name': 'Fingertip Helpdesk Core',
    'version': '18.0.1.0.0',
    'summary': 'Custom Helpdesk Ticket Management with Project Linking',
    'category': 'Services/Helpdesk',
    'author': 'Fingertip',
    'depends': ['base', 'mail', 'project'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/ticket_views.xml',
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
