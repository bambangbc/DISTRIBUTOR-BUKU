{
    'name': 'Book Distribution',
    'version': '1.0',
    'author': 'Teckzilla',
    'category': 'Product Management',
    'summary': 'Sales Team',
    'description': """
Using this application you can create a new payment term and add
it to the existing terms list
=======================================================================
 """,
    'website': 'https://www.odoo.com/page/crm',
    'depends': ['base','mail','sale'],
    'data': [
    'views/product_product_view_new.xml',
    'views/product_template_view_new.xml',

    
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
