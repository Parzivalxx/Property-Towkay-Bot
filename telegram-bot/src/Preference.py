class Preference:
    def __init__(self,
                 user_id: str,
                 district: str,
                 property_type: str,
                 min_price: int,
                 max_price: int,
                 bedrooms: int,
                 min_floor_size: int,
                 max_floor_size: int,
                 tenure: str,
                 min_build_year: int,
                 max_build_year: int,
                 floor_level: str):
        self.__user_id = user_id
        self.__district = district
        self.__property_type = property_type
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

    def get_district(self) -> str:
        return self.__district

    def get_property_type(self) -> str:
        return self.__property_type

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

    def set_district(self, district: str) -> None:
        self.__district = district
        return

    def set_property_type(self, property_type: str) -> None:
        self.__property_type = property_type
        return

    def set_min_price(self, min_price: int) -> None:
        self.__min_price = min_price
        return

    def set_max_price(self, max_price: int) -> None:
        self.__max_price = max_price
        return

    def set_bedrooms(self, bedrooms: int) -> None:
        self.__bedrooms = bedrooms
        return

    def set_min_floor_size(self, min_floor_size: int) -> None:
        self.__min_floor_size = min_floor_size
        return

    def set_max_floor_size(self, max_floor_size: int) -> None:
        self.__max_floor_size = max_floor_size
        return

    def set_tenure(self, tenure: str) -> None:
        self.__tenure = tenure
        return

    def set_min_build_year(self, min_build_year: int) -> None:
        self.__min_build_year = min_build_year
        return

    def set_max_build_year(self, max_build_year: int) -> None:
        self.__max_build_year = max_build_year
        return

    def set_floor_level(self, floor_level: str) -> int:
        self.__floor_level = floor_level
        return
