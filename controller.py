from model import ModelFromFile, ModelsManager
from views import Window


class Controller:
    def __init__(self):
        self.geo_models = {}
        self.aggregate_geo_model = []
        self.financial_models = {}
        self.financial_keys = []
        self.views = {}
        self.app = object

    def create_app(self, title, view_model_dict):
        geo_model = self.aggregate_geo_model
        app = Window(title, view_model_dict, geo_model)
        self.views = app.views
        self.app = app

    def import_muni_data(self, base_muni_models):
        base_geo_models = base_muni_models['geo_files']
        base_financial_models = base_muni_models['financial_files']
        # todo: abstract this out into the ModelsManger class
        # import_model_data()?
        for dict_name, dict_val in base_geo_models.items():
            # import data
            rough_model = ModelFromFile(dict_name, dict_val)
            # filter data
            self.geo_models[dict_name] = rough_model.filtered_data

        # this assumes strictly two geo models
        # prep like data structures for combine
        geo_model_a = self.geo_models['parcels']
        geo_model_b = self.geo_models['lease_condo']
        # combine models into a new aggregate model
        self.aggregate_geo_model = ModelsManager.append_geo_models(geo_model_a, geo_model_b)

        # prep for financial import
        for dict_name, dict_val in base_financial_models.items():
            # import data
            rough_model = ModelFromFile(dict_name, dict_val)
            # filter data
            self.financial_models[dict_name] = rough_model.filtered_data
            # add column names that can be analyzed - should turn into method
            # these will be important for making stats between columns
            self.financial_keys = self.financial_models[dict_name].keys()

        # need combine finance and geo for heat maps
        spatial_model = {
            'data': self.aggregate_geo_model,
            'merge_key': base_muni_models['geo_files']['lease_condo']['merge_key']
        }

        attribute_model = {
            'data': self.financial_models['vision'],
            'merge_key': base_muni_models['financial_files']['vision']['merge_key']
        }
        fin_geo_aggregate = ModelsManager.join_spatial_and_attributes(spatial_model, attribute_model)
        # this overwrites previous self.aggregate_geo_model
        self.aggregate_geo_model = fin_geo_aggregate

    def create_view_controller_ui(self, view_model_dict):
        controller = self
        self.app.create_ui_controllers(view_model_dict, controller)

    def show_view(self, view_name):
        # print('view name: ', view_name)
        view = self.views[view_name]
        # print(type(view))
        view.tkraise()

