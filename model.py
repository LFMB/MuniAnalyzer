# third-party packages
import geopandas as gpd
from abc import ABC

buttons_model = {
    'land_value': {
        'text': 'Land val/Total Assessed Val',
        'name': 'land_to_total'
    },
    'total_assessed_sq_foot': {
        'text': 'Total value per sq foot',
        'name': 'sq_foot_total'
    },
    'default': {
        'text': 'Home',
        'name': 'default_view'
    }
}


# could maybe generate by controller by going through each folder in Data and find file ending in .shp
muni_files = {
    'geo_files': {
        'lease_condo': {
            'name': 'lease_condo',
            'type': 'shp',
            'about': 'lease_condos hold the geometries for leases, condos and trailer homes',
            'merge_key': 'LinkID',
            'src': 'Data/Lease_Areas_Condos/Lease_Areas_Condos_Only_20200923.shp',
            'column_drop_list': [
                    'OBJECTID', 'Ward', 'SenateDist', 'HouseDist', 'MeSPC_Loc', 'Updated',
                    'Updated_By', 'Ward_2013'
                ]
        },
        'parcels': {
            'name': 'parcels',
            'type': 'shp',
            'about': 'parcels hold the geometries for residential and commercial properties',
            'merge_key': 'LinkID',
            'src': 'Data/Parcels/Parcels_Only_20200923.shp',
            'column_drop_list': [
                'OBJECTID', 'senate_201', 'ward_2003', 'house_2003', 'senate_200', 'house_2013',
                'Ward', 'SenateDist', 'HouseDist', 'MeSPC_Loc', 'Updated', 'Export_Vis',
                'Updated_By', 'Ward_2013', 'FD', 'PD'
            ]
        }
    },
    'financial_files': {
        'vision': {
            'name': 'vision',
            'type': 'dbf',
            'about': 'vision holds property info like owner history, tax assessment metrics, and political zoning',
            'merge_key': 'GISID',
            'src': 'Data/Vision_Data/Vision_Data_20200923.dbf',
            'column_drop_list': [
                'Owners_Nam', 'Mailing__1', 'Mailing__2', 'Mailing__3', 'Mailing__4', 'Mailing__7', 'Mailing__8',
                'Ward', 'Senate_Dis', 'Current__7', 'Current__8', 'Current__9', 'Current_10', 'Previous_O',
                'Previous_1', 'Previous_2', 'Previous_3', 'Previous_4', 'Previous_5', 'Previous_6', 'Previous_7',
                'Previous_8', 'Previous_9', 'Previou_10', 'Previou_11', 'Previou_12', 'Previou_13', 'Previou_14',
                'Previou_15', 'Previou_16', 'Previou_17', 'Previou_18', 'Previou_19', 'Previou_20', 'Previou_21',
                'Previou_22', 'Previou_23', 'Previou_24', 'Previou_25', 'Previou_26', 'Previou_27', 'Previou_28',
                'Previou_29', 'Previou_30', 'Previou_31', 'Previou_32', 'Previou_33', 'Previou_34', 'Previou_35',
                'Previou_36', 'Previou_37', 'Previou_38', 'Previou_39', 'Previou_40', 'Previou_41', 'Previou_42',
                'Previou_43', 'Previou_44', 'Previou_45', 'Previou_46', 'Previou_47', 'Previou_48', 'Previou_49'
            ]
        }
    }
}


# takes structured dict config file
class ModelFromFile:
    def __init__(self, name, model_init_dict={}):
        self.name = name
        self.storage = model_init_dict['src']
        self.column_drop_list = model_init_dict['column_drop_list']
        self.raw_data = []
        self.filtered_data = []
        # read_file method currently just uses geopandas
        self.__read_file()
        self.__filter_columns()

    def __read_file(self):
        # todo: make different dataframes relative to type
        self.raw_data = gpd.read_file(self.storage)
        # todo: raise exception for storage url not matching
        # todo: raise general exception for read_file

    def __filter_columns(self):
        # todo: raise exceptions for incorrect column filter list
        self.filtered_data = self.raw_data.drop(columns=self.column_drop_list)


class ModelsManager(ABC):
    @staticmethod
    def append_geo_models(model_a, model_b):
        # current case has same crs info. In future will need to
        # write logic to test for identical crs settings
        aggregate_geo = model_a.append(model_b)
        return aggregate_geo

    @staticmethod
    def join_spatial_and_attributes(spatial_model, attribute_model):

        if spatial_model['merge_key'] != attribute_model['merge_key']:
            old_column_name = attribute_model['merge_key']
            new_column_name = spatial_model['merge_key']
            # already checked that both data parameters are still geopandas DFs
            # future code shouldn't assume so
            # print(type(spatial_model['data']), type(attribute_model['data']))
            attribute_model['data'] = attribute_model['data'].rename(columns={old_column_name: new_column_name})

        # print("attribute_model['data'].keys()", attribute_model['data'].keys())
        attribute_model = attribute_model['data'].drop(columns='geometry')
        merged_models = spatial_model['data'].merge(attribute_model, on=spatial_model['merge_key'])
        merged_models.drop_duplicates(subset=spatial_model['merge_key'])
        # this is to help with debugging
        drop_column_list = [
            'Condo_Gros', 'Condo_effe', 'Condo_Livi', 'Commercial', 'Commerci_1',
            'Commerci_2', 'Commerci_3', 'Commerci_4', 'Commerci_5', 'SurveyBoun',
            'LUZone', 'Contract_Z', 'OL_APO', 'OL_GD', 'Condo_Resi', 'Condo_Comm',
            'Condo_Styl', 'Condo_St_1', 'Condo_Stor', 'Condo_Room', 'Condo_Bedr',
            'Condo_Full', 'Condo_Half'
        ]
        # once debugging is done with stats modeling probably can remove the local drop_column_list
        merged_models = merged_models.drop(columns=drop_column_list)
        # print(merged_models.keys())
        return merged_models
