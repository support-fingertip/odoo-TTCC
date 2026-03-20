{
    'name': 'TT Quotation Preview',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom Quotation Preview with Category-wise Breakdown, Payment Schedule & Material Specifications',
    'description': """
        Extends Sale Order / Quotation with:
        - Category-wise quotation line items (Category, Subcategory, Service Item, Item Name, Qty, Unit, Amount)
        - GST (18%) computation per category
        - Platform Fee (7%) on overall total
        - Floor Protection charges
        - Fixed Payment Schedule (10%, 25%, 25%, 40%)
        - Product & Material Specifications
        - QWeb PDF Report matching Tint Tone & Shade quotation preview format
    """,
    'author': 'Tint Tone & Shade',
    'website': 'https://tinttoneandshade.com',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'reports/quotation_preview_report.xml',
        'reports/quotation_preview_template.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
