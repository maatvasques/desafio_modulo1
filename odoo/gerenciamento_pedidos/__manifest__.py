# -*- coding: utf-8 -*-
{
    'name': "Gerenciamento de Pedidos",
    'summary': """
        Um módulo de gerenciamento de pedidos personalizado.
    """,
    'description': """
        Este módulo ajuda a gerenciar pedidos de forma eficiente e integrar com o WhatsApp.
    """,
    'author': "Seu Nome",
    'website': "http://www.seusite.com",
    'category': 'Sales',
    'version': '0.1',
    'depends': ['base', 'mail', 'product'], # <-- Add 'product' to this list
    'data': [
        'security/ir.model.access.csv',
        'views/pedido_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}