class Preference:
    def __init__(self,
                 user_id: str = '',
                 listing_type: str = '',
                 district: str = '',
                 property_type: str = '',
                 property_code: str = '',
                 min_price: int = 0,
                 max_price: int = 0,
                 bedrooms: int = 0,
                 min_floor_size: int = 0,
                 max_floor_size: int = 0,
                 tenure: str = '',
                 min_build_year: int = 0,
                 max_build_year: int = 0,
                 floor_level: str = ''):
        self.__user_id = user_id
        self.__listing_type = listing_type
        self.__district = district
        self.__property_type = property_type
        self.__property_code = property_code
        self.__min_price = min_price
        self.__max_price = max_price
        self.__bedrooms = bedrooms
        self.__min_floor_size = min_floor_size
        self.__max_floor_size = max_floor_size
        self.__tenure = tenure
        self.__min_build_year = min_build_year
        self.__max_build_year = max_build_year
        self.__floor_level = floor_level

    def get_user_id(self) -> str:
        return self.__user_id

    def get_listing_type(self) -> str:
        return self.__listing_type

    def get_district(self) -> str:
        return self.__district

    def get_property_type(self) -> str:
        return self.__property_type

    def get_property_code(self) -> str:
        return self.__property_code

    def get_min_price(self) -> int:
        return self.__min_price

    def get_max_price(self) -> int:
        return self.__max_price

    def get_bedrooms(self) -> int:
        return self.__bedrooms

    def get_min_floor_size(self) -> int:
        return self.__min_floor_size

    def get_max_floor_size(self) -> int:
        return self.__max_floor_size

    def get_tenure(self) -> str:
        return self.__tenure

    def get_min_build_year(self) -> int:
        return self.__min_build_year

    def get_max_build_year(self) -> int:
        return self.__max_build_year

    def get_floor_level(self) -> str:
        return self.__floor_level
