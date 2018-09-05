"""
    Data for database demonstrations
"""


def get_furniture_data():
    """
    demonstration data
    """
    # A list of dictionary data.
    furniture_data = [
        {
            'product':
                {'type': 'Couch',
                 'color': 'Red'},
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product':
                {'type': 'Couch',
                 'color': 'Blue'},
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product': 
                {'type': 'Coffee table',
                 'color': 'Brown'},
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product': 
                {'type': 'Couch',
                 'color': 'Red'},
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        },
        {
            'product': 
                {'type': 'Recliner',
                 'color': 'Blue'},
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product': 
                {'type': 'Chair',
                 'color': 'Black/White'},
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45
        },
        {
            'product':
                {'type': 'Lamp',
                 'color': 'Black'},
            'description': 'Metal',
            'monthly_rental_cost': 8.55,
            'in_stock_quantity': 11
        },
        {
            'product':
                {'type': 'Television',
                 'color': 'Black'},
            'description': 'Aluminum',
            'monthly_rental_cost': 33.99,
            'in_stock_quantity': 6
        }
    ]
    return furniture_data
