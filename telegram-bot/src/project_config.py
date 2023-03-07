handlers = {
    '/help': 'view list of commands to run',
    '/new': 'input new preference',
    '/update': 'update existing preference',
    '/delete': 'delete existing preference',
    '/pause': 'pause current job',
    '/continue': 'continue current job'
}

preference_data = {
    'user_id': '',
    'listing_type': '',
    'property_type': '',
    'property_code': '',
    'min_price': 0,
    'max_price': 0,
    'min_floor_size': 0,
    'max_floor_size': 0,
    'min_build_year': 0,
    'max_build_year': 0,
    'bedrooms': 0,
    'floor_level': '',
    'tenure': '',
    'district': ''
}

preference_options = {
    'listing_type': (
        'Sale',
        'Rent'
    ),
    'property_type': (
        'HDB',
        'Condo',
        'Landed'
    ),
    'property_code': {
        'HDB': (
            '1 room',
            '2 room',
            '3 room',
            '4 room',
            '5 room',
            'Jumbo',
            'EA',
            'EM',
            'MG',
            'Terrace'
        ),
        'Condo': (
            'Condo',
            'Apartment',
            'Walk-up',
            'Cluster House',
            'Executive Condo'
        ),
        'Landed': (
            'Terraced House',
            'Detached House',
            'Semi-Detached House',
            'Corner Terrace',
            'Bungalow',
            'Good Class Bungalow',
            'Shophouse',
            'Land Only',
            'Town House',
            'Conservation House',
            'Cluster House'
        )
    },
    'min_price': None,
    'max_price': None,
    'min_floor_size': None,
    'max_floor_size': None,
    'min_build_year': None,
    'max_build_year': None,
    'bedrooms': (
        'Studio',
        '1',
        '2',
        '3',
        '4',
        '5'
    ),
    'floor_level': (
        'Low',
        'Mid',
        'High',
        'Penthouse',
        'Ground'
    ),
    'tenure': (
        'Freehold',
        '99-year',
        '103-year',
        '110-year',
        '999-year',
        '9999-year',
        'Unknown'
    ),
    'district': (
        'D01 Boat Quay / Raffles Place / Marina',
        'D02 Chinatown / Tanjong Pagar',
        'D03 Alexandra / Commonwealth',
        'D04 Harbourfront / Telok Blangah',
        'D05 Buona Vista / West Coast / Clementi New Town',
        'D06 City Hall / Clarke Quay',
        'D07 Beach Road / Bugis / Rochor',
        'D08 Farrer Park / Serangoon Rd',
        'D09 Orchard / River Valley',
        'D10 Tanglin / Holland / Bukit Timah',
        'D11 Newton / Novena',
        'D12 Balestier / Toa Payoh',
        'D13 Macpherson / Potong Pasir',
        'D14 Eunos / Geylang / Paya Lebar',
        'D15 East Coast / Marine Parade',
        'D16 Bedok / Upper East Coast',
        'D17 Changi Airport / Changi Village',
        'D18 Pasir Ris / Tampines',
        'D19 Hougang / Punggol / Sengkang',
        'D20 Ang Mo Kio / Bishan / Thomson',
        'D21 Clementi Park / Upper Bukit Timah',
        'D22 Boon Lay / Jurong / Tuas',
        'D23 Dairy Farm / Bukit Panjang / Choa Chu Kang',
        'D24 Lim Chu Kang / Tengah',
        'D25 Admiralty / Woodlands',
        'D26 Mandai / Upper Thomson',
        'D27 Sembawang / Yishun',
        'D28 Seletar / Yio Chu Kang'
    )
}
