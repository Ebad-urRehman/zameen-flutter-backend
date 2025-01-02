import json

def get_converted_values(area, area_type, str_bath, str_bedroom, str_location, str_city, str_property_type, str_purpose, str_province_name):
    with open('files/categorical_to_numerical_data.json') as json_file:
        cat_to_num = json.load(json_file)
    
    # area conversion
    if area_type == 'marlas':
        area = float(area) * (1/1976.84)
    elif area_type == 'kanals':
        area = float(area) * (1/39536.8)

    # numerical columns
    baths = int(str_bath)
    bedrooms = int(str_bedroom)

    # categoical column
    location = cat_to_num['location'][str_location]
    city = cat_to_num['city'][str_city]
    property_type = cat_to_num['property_type'][str_property_type]
    purpose = cat_to_num['purpose'][f'{str_purpose} {str_property_type}']
    province = cat_to_num['province_name'][str_province_name]

    return [property_type, location, city, province, baths, area, purpose, bedrooms]



def abbreviate_number(num):
    num = int(num)
    if num < 1_000:
        return str(num)
    elif num < 1_00_000:
        return f"{num // 1_000} K"
    elif num < 1_00_00_000:
        return f"{num // 1_00_000} L"
    elif num < 1_00_00_00_000:
        return f"{num // 1_00_00_000} Cr"
    else:
        return f"{num // 1_00_00_00_000} B" 