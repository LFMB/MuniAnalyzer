# static models
from model import buttons_model, muni_files

# classes
from controller import Controller

# init app
c = Controller()

# import data
c.import_muni_data(muni_files)

# create views
c.create_app("Muni Analyzer", buttons_model)

# create UI controllers that link views
c.create_view_controller_ui(buttons_model)

# this is a hack: need to fix view controllers
c.show_view('sq_foot_total')

c.app.mainloop()
