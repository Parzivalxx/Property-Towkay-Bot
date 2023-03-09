URI = 'https://www.propertyguru.com.sg/'
SCRAPER_INIT_RETRIES = 20
SCRAPER_ERROR_RETRIES = 3
MAX_PAGES = 5

preference_mapper = {
    'listing_type': {
        'Sale': 'sale',
        'Rent': 'rent'
    },
    'property_type': {
        'HDB': 'H',
        'Condo': 'N',
        'Landed': 'L'
    },
    'property_type_code': {
        'HDB': {
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
        },
        'Condo': {
            'Condo': 'CONDO',
            'Apartment': 'APT',
            'Walk-up': 'WALK',
            'Cluster House': 'CLUS',
            'Executive Condo': 'EXCON'
        },
        'Landed': {
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
    },
    'bedrooms': {
        'Studio': '0',
        '1': '1',
        '2': '2',
        '3': '3',
        '4': '4',
        '5': '5+'
    },
    'floor_level': {
        'Low': 'LOW',
        'Mid': 'MID',
        'High': 'HIGH',
        'Penthouse': 'PENT',
        'Ground': 'GND'
    },
    'tenure': {
        'Freehold': 'F',
        '99-year': 'L99',
        '103-year': 'L103',
        '110-year': 'L110',
        '999-year': 'L999',
        '9999-year': 'L9999',
        'Unknown': 'NA'
    }
}

query_mapper = {
    'property_type_code': 'property_type_code[]',
    'min_price': 'minprice',
    'max_price': 'maxprice',
    'min_floor_size': 'minsize',
    'max_floor_size': 'maxsize',
    'min_build_year': 'mintop',
    'max_build_year': 'maxtop',
    'bedrooms': 'beds[]',
    'floor_level': 'floor_level[]',
    'tenure': 'tenure[]',
    'district': 'district_code[]'
}

numeric_cols = (
    'min_price',
    'max_price',
    'min_floor_size',
    'max_floor_size',
    'min_build_year',
    'max_build_year',
    'job_frequency_hours'
)
