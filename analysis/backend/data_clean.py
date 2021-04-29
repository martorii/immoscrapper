import pandas as pd
import numpy as np
import Levenshtein as lev

def drop_unnecessary_columns(df):
    unnecessary_columns = ['property_id', 'title', 'extraction_date', 'lift', 'security_system', 'last_seen']
    df.drop(columns=unnecessary_columns, inplace=True)
    return df


def map_from_value_to_key(row_value, mapper):
    # Everything must be lowcase!
    if row_value is not None:
        row_value_lowercase = row_value.lower()
        for key, value_list in mapper.items():
            if row_value_lowercase in value_list:
                return key
    return np.NAN


def get_dummies_from_categorical(categorical_features, df):
    for categorical_feature in categorical_features:
        # Get one hot encoding of columns 'vehicleType'
        one_hot = pd.get_dummies(df[categorical_feature], prefix=categorical_feature)
        # Drop column as it is now encoded
        df = df.drop(categorical_feature,axis = 1)
        # Join the encoded df
        df = pd.concat([df, one_hot], axis=1)
    return df


def match_districts(list_1, list_2):
    match_dict = {}
    list_1_copy = sorted(list_1, key=len, reverse=True)
    list_2_copy = list_2.copy()
    for el_1 in list_1_copy:
        min_dist = 1000
        best_match = ''
        for el_2 in list_2_copy:
            dist = lev.distance(el_1, el_2)
            if dist < min_dist:
                min_dist = dist
                best_match = el_2
        match_dict[best_match] = el_1.strip()
        list_2_copy.remove(best_match)
    return match_dict


def preprocess_pisos(df, sale_or_rent):
    # Filter to get only pisos data
    df = df[df.portal == 'pisos']
    # Delete portal
    df.drop(columns=['portal'], inplace=True)
    # Get only sale or rent
    df = df[df.sale_or_rent==sale_or_rent]
    df.drop(columns=['sale_or_rent'], inplace=True)
    # Get only interesting columns
    df = drop_unnecessary_columns(df)
    # Delete properties without price
    df = df[df.price > 0]
    # Remove too expensive properties
    if sale_or_rent=='buy':
        df = df[df.price < 1500000]
    elif sale_or_rent=='rent':
        df = df[df.price <= 3500]
    # Assume NaNs are E by energy_certificate
    df.energy_certificate.fillna('E', inplace=True)
    # Calculate floor_area
    df['floor_area'] = df[['usable_floor_area', 'floor_area']].min(axis=1)
    df['built_up_area'] = df[['built_up_area', 'floor_area']].max(axis=1)
    df.floor_area.fillna(df.built_up_area, inplace=True)
    df = df[df.floor_area.notna()]
    df.drop(columns=['usable_floor_area', 'built_up_area'], inplace=True)
    # Delete weird floors
    df = df[df.floor <= 10]
    # Study only locations in Barcelona
    df = df[df.location.str.contains('Barcelona')]
    # Drop where no n_rooms
    df = df[df.n_rooms.notna()]
    # No bathrooms --> 1
    df.loc[(df.n_bathrooms.isna()), 'n_bathrooms'] = 1
    # Replace garage nans with 0
    df.garage.fillna(0, inplace=True)
    # Improve flooring
    df.drop(columns=['flooring'], inplace=True)
    # Condition
    df = df[df.condition.notna()]
    condition_dict = {
        'good': ['in good condition', 'good'],
        'remodelled': ['remodelled'],
        'new': ['brand new'],
        'very good': ['almost new', 'very good'],
        'to reform': ['to renovate']
    }
    df['condition'] = df['condition'].apply(map_from_value_to_key, mapper=condition_dict)
    # Heating
    heating_dict = {
        'natural gas': ['natural gas', 'gas natural', 'yes', 'central', 'gasoil'],
        'electric': ['electricity', 'electricidad']
    }
    df['heating'] = df['heating'].apply(map_from_value_to_key, mapper=heating_dict)
    df.heating.fillna('No', inplace=True)
    # Air conditioning
    air_conditioning_dict = {
        'cold and heat': ['cold and heat', 'frío-calor'],
        'cold': ['cold', 'yes']
    }
    df['air_conditioning'] = df['air_conditioning'].apply(map_from_value_to_key, mapper=air_conditioning_dict)
    df.air_conditioning.fillna('No', inplace=True)
    # Antiquity
    antiquity_dict = {
        '50+': ['more than 50 years', '50 to 70 years', '70 to 100 years'],
        '30-50': ['between 30 and 50 years', '30 to 50 years'],
        '20-30': ['between 20 and 30 years', '20 to 30 years'],
        '10-20': ['between 10 and 20 years', '10 to 20 years'],
        '5-10': ['between 5 and 10 years'],
        '0-5': ['less than 5 years', '1 to 5 years']
    }
    df['antiquity'] = df['antiquity'].apply(map_from_value_to_key, mapper=antiquity_dict)
    df.antiquity.fillna('10-20', inplace=True)
    # Facing
    df.loc[(df.facing.isna()), 'facing'] = 'West'
    df = df[df.facing.isin(['South', 'East', 'Southeast', 'Southwest', 'West', 'North', 'Northeast', 'Northwest'])]
    # Swimming pool
    swimming_pool_dict = {
        'communal': ['communal'],
        'own': ['own', 'con piscina']
    }
    df['swimming_pool'] = df['swimming_pool'].apply(map_from_value_to_key, mapper=swimming_pool_dict)
    df.swimming_pool.fillna('No', inplace=True)
    # Garden
    garden_dict = {
        'communal': ['communal'],
        'own': ['own', 'private', 'yes']
    }
    df['garden'] = df['garden'].apply(map_from_value_to_key, mapper=garden_dict)
    df.garden.fillna('No', inplace=True)
    # Calculate price per m2
    df['price'] = df['price']/df['floor_area']
    df.drop(columns=['floor_area'], inplace=True)
    # Separate url from df
    urls = df['url']
    df.drop(columns='url', inplace=True)
    # Drop constant columns
    df = df.loc[:, (df != df.iloc[0]).any()]
    return df, urls


