'''
TODO:
    How to pass sender data to file dialog
    Format tabs
    Figure out I/O layout
    Graphs!
'''


import dearpygui.dearpygui as dpg
from daily_log_processing import dailyLog as dl
from weight_parser import weightLog as wl
from food_concatenator import foodTracker as ft

dpg.create_context()

data_path = f'E:\Documents\Datasets'

# initialize our log objects
daily_log = dl()
weight_log = wl()
food_log = ft()


with dpg.window(label='Life Data Tracker and Analysis', tag='primary'):
    with dpg.tab_bar():
        def open_file(sender, app_data, user_data):
            fd_uid = dpg.generate_uuid()

            def add_file(user_data, data):
                # what = list(data['selections'].values())
                # print(what[0])
                # dpg.set_value(user_data, what[0])

                def dl_read(log_path):

                    kl = list(log_path['selections'].keys())
                    # print(log_path['selections'][kl[0]])
                    daily_log.import_new_log(path=log_path['selections'][kl[0]])

                    for day in daily_log.ret_missing_dates():

                        with dpg.table_row(parent='dl_missing_days'):
                            dpg.add_text(f'{day}')

                def food_read(log_path):
                    print('Empty function!')
                    return

                def nutr_file(log_path):
                    print('Empty function!')
                    return

                def wt_read(log_path):
                    print('Empty function!')
                    return

                return {'daily_log':        dl_read,
                        'food_log':         food_read,
                        'nutr_file':        nutr_file,
                        'weight_tracker':   wt_read}.get(user_data)(data)

            with dpg.file_dialog(label="File Dialog", width=600, height=400, show=False, default_path=data_path,
                                 callback=lambda s, a, u: add_file(user_data, a), tag=fd_uid):
                dpg.add_file_extension(".*")
                dpg.add_file_extension("", color=(150, 255, 150, 255))
                dpg.add_file_extension(".csv", color=(255, 255, 0, 255))
                dpg.add_file_extension(".xml", color=(255, 0, 255, 255))
                dpg.add_file_extension(".xmlx", color=(0, 255, 0, 255))

            dpg.show_item(fd_uid)

        with dpg.tab(label='Daily Log'):
            dpg.add_text('Daily Log')
            dpg.add_button(label='Read Daily Log', callback=open_file, user_data='daily_log')

            with dpg.table(header_row=True, policy=dpg.mvTable_SizingStretchProp, borders_outerH=True,
                           borders_innerV=True, borders_outerV=True, width=300, tag='dl_missing_days'):
                dpg.add_table_column()

            #dpg.add_date_picker(tag='dl_calendar')
            dpg.add_table(label='Activity Totals', tag='dl_totals')

        with dpg.tab(label='Food Log'):
            dpg.add_text('Food Log')
            dpg.add_button(label='Read Food Log', callback=open_file, user_data='food_log')
            dpg.add_button(label='Read Nutritional Info', callback=open_file, user_data='nutr_file')

            with dpg.table(header_row=True, policy=dpg.mvTable_SizingStretchProp, borders_outerH=True,
                           borders_innerV=True, borders_outerV=True, width=300, label='Missing Dates'):
                dpg.add_table_column()

            # with dpg.table(label='Missing Foods'):
            #     dpg.add_table_column(id='missing_food', label='Missing Days')


        with dpg.tab(label='Weight Tracker'):
            dpg.add_text('Weight Tracker')
            dpg.add_button(label='Read Weight Tracker', callback=open_file, user_data='weight_tracker')

        with dpg.tab(label='File System'):
            dpg.add_text('File System')

        with dpg.tab(label='Data Processing'):
            dpg.add_text('Data Processing')

dpg.create_viewport(title='Life Data Program', width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('primary', True)
dpg.start_dearpygui()
dpg.destroy_context()