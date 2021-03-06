'''
TODO:
    Selectable tables should actually be list boxes!
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


########################################################################################################################
'''
Main window
'''
# dpg.add_colormap_registry(label="Demo Colormap Registry", tag="__demo_colormap_registry")
#
# dpg.add_colormap([[255, 0, 0]], True, tag="red_tag", parent="__demo_colormap_registry")
# dpg.add_colormap([[0, 255, 0]], True, tag="green_tag",parent="__demo_colormap_registry")
#
# #not sure this is the way to go
# with dpg.theme() as enabled_theme:
#     with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 0), category=dpg.mvThemeCat_Core)
#
# with dpg.theme() as disabled_theme:
#     with dpg.theme_component(dpg.mvAll):
#         dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 255, 0), category=dpg.mvThemeCat_Core)

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

                        dpg.add_table_row(parent='dl_missing_days')
                        with dpg.table_row(parent='dl_missing_days'):
                            #dpg.add_table_cell()
                            # with dpg.table_cell():
                            dpg.add_text(f'{day}')

                    dpg.add_table_row(parent='io_dl_col')
                    with dpg.table_row(parent='io_dl_col'):
                        dpg.add_text(f'{daily_log.ret_date()}')

                    # pg.bind_colormap('dl_file_color', 'green_flag')

                def food_read(log_path):
                    #print('Empty function!')
                    kl = list(log_path['selections'].keys())

                    food_log.

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

########################################################################################################################

        with dpg.tab(label='Daily Log'):
            '''
            Daily Log Tab

            TODO:
                Import Daily log
            '''

            #dpg.add_text('Daily Log')
            with dpg.group(horizontal=True):
                dpg.add_button(label='Read Daily Log', callback=open_file, user_data='daily_log')
                # dpg.add_colormap_button(label="None", tag='dl_file_colors')
                # dpg.bind_colormap(dpg.last_item(), "red_tag")
                # dpg.bind_item_theme('dl_file_colors', disabled_theme)

            #dpg.add_date_picker(tag='dl_calendar')
            with dpg.collapsing_header(label='Activity Totals'):
                dpg.add_table(label='Activity Totals', tag='dl_totals')

            with dpg.collapsing_header(label='Missing Dates'):
                with dpg.table(borders_outerH=True, scrollY=True, reorderable=True, height=400,
                               borders_innerV=True, borders_outerV=True, width=200, tag='dl_missing_days'):
                    dpg.add_table_column() # make this a combo box? Or a date picker?

########################################################################################################################

        with dpg.tab(label='Food Log'):
            '''
            Food Log
            
            TODO:
                Show what items and dates don't have nutritional information
                How do deal with one log but not another ready...
            '''
            dpg.add_text('Food Log')
            dpg.add_button(label='Read Food Log', callback=open_file, user_data='food_log')
            dpg.add_button(label='Read Nutritional Info', callback=open_file, user_data='nutr_file')

            dpg.add_combo()

            with dpg.collapsing_header(label='Missing Dates'):
                with dpg.table(borders_outerH=True, scrollY=True, sortable=True, height=400,
                               borders_innerV=True, borders_outerV=True, width=200, tag='fl_missing_days'):
                    dpg.add_table_column()

            # with dpg.table(label='Missing Foods'):
            #     dpg.add_table_column(id='missing_food', label='Missing Days')

########################################################################################################################

        with dpg.tab(label='Weight Tracker'):
            '''
            Weight Tracker
            
            TODO:
             
            '''

            dpg.add_text('Weight Tracker')
            dpg.add_button(label='Read Weight Tracker', callback=open_file, user_data='weight_tracker')

            with dpg.collapsing_header(label='Missing Dates'):
                with dpg.table(borders_outerH=True, scrollY=True, sortable=True, height=400,
                               borders_innerV=True, borders_outerV=True, width=200, tag='wt_missing_days'):
                    dpg.add_table_column()

########################################################################################################################

        with dpg.tab(label='File System'):
            '''
            File merging I/O
            
            TODO:
                How to flag exiting files?
                Track and export files as pickle/.csv
            '''

            dpg.add_text('File System')

            with dpg.group(horizontal=True):
                with dpg.table(label='Daily Logs', tag='io_dl_col', width=150, height=300, scrollY=True, header_row=True):
                    dpg.add_table_column()

                with dpg.table(label='Weight Tracker', tag='io_wt_col', width=150, height=300, header_row=True, scrollY=True):
                    dpg.add_table_column()

                with dpg.table(label='Food Tracker', tag='io_ft_col', width=150, height=300, header_row=True, scrollY=True):
                    dpg.add_table_column()

########################################################################################################################

        with dpg.tab(label='Data Processing'):
            '''
            TODO:
                Graphs graphs graphs
            '''
            dpg.add_text('Data Processing')

########################################################################################################################

dpg.create_viewport(title='Life Data Program', width=1200, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window('primary', True)
dpg.start_dearpygui()
dpg.destroy_context()