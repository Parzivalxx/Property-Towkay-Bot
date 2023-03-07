URI = 'https://www.propertyguru.com.sg/'
SCRAPER_INIT_RETRIES = 10
SCRAPER_ERROR_RETRIES = 3

PREFERENCES = {
    'Listing Type': {
        'Sale': 'sale',
        'Rent': 'rent'
    },
    'Property Type': {
        'HDB': {
            'Type': 'H',
            'Codes': {
                '1 room': '1R',
                '2 room': ['2A', '2I', '2S'],
                '3 room': ['3A', '3NG', '3Am', '3NGm', '3I', '3Im', '3S', '3STD'],
                '4 room': ['4A', '4NG', '4S', '4I', '4STD'],
                '5 room': ['5A', '5I', '5S'],
                'Jumbo': '6J',
                'EA': 'EA',
                'EM': 'EM',
                'MG': 'MG',
                'Terrace': 'TE'
            }
        },
        'Condo': {
            'Type': 'N',
            'Codes': {
                'Condo': 'CONDO',
                'Apartment': 'APT',
                'Walk-up': 'WALK',
                'Cluster House': 'CLUS',
                'Executive Condo': 'EXCON'
            }
        },
        'Landed': {
            'Type': 'L',
            'Codes': {
                'Terraced House': 'TERRA',
                'Detached House': 'DETAC',
                'Semi-Detached House': 'SEMI',
                'Corner Terrace': 'CORN',
                'Bungalow': 'LBUNG',
                'Good Class Bungalow': 'BUNG',
                'Shophouse': 'SHOPH',
                'Land Only': 'RLAND',
                'Town House': 'TOWN',
                'Conservation House': 'CON',
                'Cluster House': 'LCUS'
            }
        }
    },
    'Number of bedrooms': {
        'Studio': '0',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5+'
    },
    'Floor level': {
        'Low': 'LOW',
        'Mid': 'MID',
        'High': 'HIGH',
        'Penthouse': 'PENT',
        'Ground': 'GND'
    },
    'Tenure': {
        'Freehold': 'F',
        '99-year': 'L99',
        '103-year': 'L103',
        '110-year': 'L110',
        '999-year': 'L999',
        '9999-year': 'L9999',
        'Unknown': 'NA'
    }
}
