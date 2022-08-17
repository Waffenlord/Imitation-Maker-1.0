import PySimpleGUI as sg  
from class_imitation import Imitation

sg.theme('dark')

NOTES = ['Rest','C', 'C#', 'Db', 'D', 'D#', 'Eb' ,'E', 'F', 'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']
MEASURES = [1, 2, 3, 4, 5, 6, 7, 8]
FONT = 'Montserrat Light'
TITLE_SIZE = 20
TEXT_SIZE = 12
BUTTON_TEXT_SIZE = 10

menu_layout = [
    ['Guide', ['Welcome']],
    ['Help', ['Imitation at the 8th', 'Imitation at the 5th']]
]

draw_container = [
    [sg.Push(), sg.Text('Draw a note', font= (FONT, TITLE_SIZE)), sg.Push()],
    [sg.Text('Staff', font= (FONT, TEXT_SIZE, 'italic')), sg.OptionMenu(['Upper', 'Lower'], pad=((20, 20)), key= '-STAFF-'), 
     sg.Text('Note', font= (FONT, TEXT_SIZE, 'italic')), sg.OptionMenu(NOTES, pad=((20, 20)), key= '-NOTE-'), 
     sg.Text('Value', font= (FONT, TEXT_SIZE, 'italic')), sg.OptionMenu(['Half', 'Whole'], pad=((20, 20)), key= '-VALUE-'), 
     sg.Text('Measure', font= (FONT, TEXT_SIZE, 'italic')), sg.OptionMenu(MEASURES, pad=((20, 20)), key= '-MEASURE-')],
    [sg.Push(),sg.Button('DRAW NOTE', key= '-DRAW-', font= (FONT, BUTTON_TEXT_SIZE)), sg.Push(), sg.Text('Octave', font= (FONT, TEXT_SIZE, 'italic')), 
     sg.Button('Upper', key= '-OUPPER-', font= (FONT, BUTTON_TEXT_SIZE)), sg.Button('Lower', key= '-OLOWER-', font= (FONT, BUTTON_TEXT_SIZE)),sg.Push()]
]

delete_container = [
    [sg.Push(), sg.Text('Delete the last note', font= (FONT, TITLE_SIZE)), sg.Push()],
    [sg.Text('Select the Staff', font= (FONT, TEXT_SIZE, 'italic')), sg.OptionMenu(['Upper', 'Lower'], pad=((20, 20)), key= '-DELETE_STAFF-'), 
     sg.Text('Select the measure', font= (FONT, TEXT_SIZE, 'italic')), sg.OptionMenu(MEASURES, pad=((20, 20)), key= '-DELETE_MEASURE-')],
    [sg.Push(),sg.Button('DELETE NOTE', key= '-DELETE_NOTE-', font= (FONT, BUTTON_TEXT_SIZE)), sg.Push()]
    
]

delete_all_container = [
    [sg.Push(), sg.Text('Delete all notes', font= (FONT, TITLE_SIZE)), sg.Push()],
    [sg.Text('Every note will be deleted!', font= (FONT, TEXT_SIZE), pad= 20)],
    [sg.Push(),sg.Button('DELETE ALL', key= '-DELETE_ALL-', font= (FONT, BUTTON_TEXT_SIZE)), sg.Push()]
    
]

field = sg.Graph(canvas_size = (1000, 300), graph_bottom_left= (0,0), graph_top_right= (1000, 300), background_color= 'white', enable_events = True, pad= 20, key= '-GRAPH-')



layout = [
    [sg.Menu(menu_layout, tearoff= True)],
    [sg.Column(draw_container), sg.VerticalSeparator(), sg.Column(delete_container), sg.VerticalSeparator(), sg.Column(delete_all_container)],
    [sg.HorizontalSeparator()],
    [sg.Push(), field, sg.Push()],
    [sg.HorizontalSeparator()],
    [sg.Push(), sg.Button('EXAMINE COMPOSITION', pad= 20, key= '-EXAMINE-', font= (FONT, BUTTON_TEXT_SIZE)), 
     sg.Button('Delete results', pad= 20, key= '-CLEAN_STATS-', font= (FONT, BUTTON_TEXT_SIZE)), sg.Push(), 
     sg.VerticalSeparator(), sg.Push(), sg.Multiline('Click examine composition to see here the results', size= ((60, 10)), key= '-STATS-',  font= (FONT, TEXT_SIZE), pad= 20), sg.Push()]

]



window = sg.Window('Imitation Maker 1.0', layout, icon= 'icon.ico', finalize= True)
field.draw_image('staff.png', location= (10, 260))



notes_to_draw_upper = {}
notes_to_draw_lower = {}
used_measures_upper = set()
used_measures_lower = set()
NOTE_RADIO = 5
NOTE_STEM_LONGITUDE = 30
NOTE_FILL_COLOR = 'white'
NOTE_LINE_COLOR = 'black'
NOTES_POSITION_UPPER = {'C': 151, 'D': 157, 'E': 162, 'F': 168, 'G': 174, 'A': 180, 'B': 184, 'R': (183, 181)}
NOTES_POSITION_LOWER = {'C': 55, 'D': 61, 'E': 67, 'F': 72, 'G': 77, 'A': 82, 'B': 87, 'R': (61, 58)}
MEASURE_POSITION = {'1': 140, '2': 250, '3': 360, '4': 470, '5': 580, '6': 680, '7': 790, '8': 890}
MEASURE_DISTANCE = 50
OCTAVE_DISTANCE = 38
MIDDLE_LINE_LONGITUDE = 10

imitate = Imitation()

def draw_notes(notes_to_draw_upper, notes_to_draw_lower, field):
    if len(notes_to_draw_upper) > 0:
        for note in notes_to_draw_upper.values():
            #note[0] = Measure position
            #note[1] = Note position
            #note[2] = Alterations
            #note[3] = Half or whole note
            #note[4] = Is a rest
            if note[4] == False:
                field.draw_circle((note[0], note[1]), radius= NOTE_RADIO, fill_color= NOTE_FILL_COLOR, line_color= NOTE_LINE_COLOR, line_width= 2)
                if note[2] != False:
                    field.draw_text(text = note[2], location= (note[0] - 12, note[1]), font= (FONT, 12) )
                
                if note[3] == True:
                    v_direction = NOTE_STEM_LONGITUDE
                    h_direction = 5
                    if note[1] > 180:
                        v_direction = -NOTE_STEM_LONGITUDE
                        h_direction = -h_direction
                    field.draw_line(point_from=(note[0] + h_direction, note[1]),point_to= (note[0] + h_direction, note[1] + v_direction), width= 2 )
                    
                if note[1] < NOTES_POSITION_UPPER['D']:
                    field.draw_line(point_from=(note[0] - MIDDLE_LINE_LONGITUDE, NOTES_POSITION_UPPER['C']),point_to= (note[0] + MIDDLE_LINE_LONGITUDE, NOTES_POSITION_UPPER['C']), width= 2 )
                    
            else:
                field.draw_rectangle((note[0], note[1][0]), (note[0] + 10, note[1][1]), fill_color= NOTE_LINE_COLOR)
                
                
    if len(notes_to_draw_lower) > 0:
        for note in notes_to_draw_lower.values():
            if note[4] == False:
                field.draw_circle((note[0], note[1]), radius= NOTE_RADIO, fill_color= NOTE_FILL_COLOR, line_color= NOTE_LINE_COLOR, line_width= 2)
                if note[2] != False:
                    field.draw_text(text = note[2], location= (note[0] - 12, note[1]), font= (FONT, 12) )
                if note[3] == True:
                    v_direction = NOTE_STEM_LONGITUDE
                    h_direction = 5
                    if note[1] > 55:
                        v_direction = -NOTE_STEM_LONGITUDE
                        h_direction = -h_direction
                    field.draw_line(point_from=(note[0] + h_direction, note[1]),point_to= (note[0] + h_direction, note[1] + v_direction), width= 2 )
                    
                if note[1] > NOTES_POSITION_LOWER['B']:
                    field.draw_line(point_from=(note[0] - MIDDLE_LINE_LONGITUDE, NOTES_POSITION_LOWER['C'] + OCTAVE_DISTANCE),point_to= (note[0] + MIDDLE_LINE_LONGITUDE, NOTES_POSITION_LOWER['C'] + OCTAVE_DISTANCE), width= 2 )
            else:
                field.draw_rectangle((note[0], note[1][0]), (note[0] + 10, note[1][1]), fill_color= NOTE_LINE_COLOR)



def guide_window_func():
    window_guide = sg.Window('Guide', [[sg.Image(source= r'music-app-guide.png')]], icon='icon.ico', finalize= True)
    
    while True:
        guide_event, guide_values = window_guide.read()
            
        if guide_event == sg.WIN_CLOSED:
            break
        
    window_guide.close()


def imitation_octave_window():
    slide1 = r'imitation-8-1.png'
    slide2 = r'imitation-8-2.png'
    
    slides = [slide1, slide2]
    
    idx = 0
    
    octave_layout = [
        [sg.Image(source= slides[idx], key= '-OCTAVE_SLIDES-')],
        [sg.Push(), sg.Button('Previous', pad= 20, key= '-BACK_8-', font= (FONT, BUTTON_TEXT_SIZE)), 
         sg.VerticalSeparator(), sg.Button('Next', pad= 20, key= '-NEXT_8-', font= (FONT, BUTTON_TEXT_SIZE)), sg.Push()]
        
    ]
    
    window_octave = sg.Window('Imitation at the 8th', octave_layout, icon='icon.ico', finalize= True)
    
    while True:
        octave_event, octave_values = window_octave.read()
            
        if octave_event == sg.WIN_CLOSED:
            break
        
        if octave_event == '-NEXT_8-':
            if idx < len(slides) - 1:
                idx += 1
                window_octave['-OCTAVE_SLIDES-'].update(source= slides[idx])
        
        if octave_event == '-BACK_8-':
            if idx > 0:
                idx -= 1
                window_octave['-OCTAVE_SLIDES-'].update(source= slides[idx])
        
        
        
    window_octave.close()
    
def imitation_fifth_window():
    slide1 = r'imitation-5-1.png'
    slide2 = r'imitation-5-2.png'
    
    slides = [slide1, slide2]
    
    idx = 0
    
    fifth_layout = [
        [sg.Image(source= slides[idx], key= '-FIFTH_SLIDES-')],
        [sg.Push(), sg.Button('Previous', pad= 20, key= '-BACK_5-', font= (FONT, BUTTON_TEXT_SIZE)), 
         sg.VerticalSeparator(), sg.Button('Next', pad= 20, key= '-NEXT_5-', font= (FONT, BUTTON_TEXT_SIZE)), sg.Push()]
        
    ]
    
    window_fifth = sg.Window('Imitation at the 5th', fifth_layout, icon='icon.ico', finalize= True)
    
    while True:
        fifth_event, fifth_values = window_fifth.read()
            
        if fifth_event == sg.WIN_CLOSED:
            break
        
        if fifth_event == '-NEXT_5-':
            if idx < len(slides) - 1:
                idx += 1
                window_fifth['-FIFTH_SLIDES-'].update(source= slides[idx])
        
        if fifth_event == '-BACK_5-':
            if idx > 0:
                idx -= 1
                window_fifth['-FIFTH_SLIDES-'].update(source= slides[idx])
        
        
        
    window_fifth.close()
    
    
    
while True:

    event, values = window.read()
   
    if event == sg.WIN_CLOSED:
        break
   
                                                                #DRAW BUTTON 
    if event == '-DRAW-':
        draw_complete_form = True
        options = ['-STAFF-', '-NOTE-', '-VALUE-', '-MEASURE-']
        for option in options:
            if len(values[option]) == 0:
                sg.popup_no_buttons('Please select an option in every field!', title= 'Error', auto_close= True, auto_close_duration= 2)
                draw_complete_form = False
                break
        
        if draw_complete_form == True:                    #Get the values of each field, convert the values to numbers for the backend if needed
            selected_staff = values['-STAFF-']
            selected_note = values['-NOTE-']
            if selected_note == 'Rest':
                note_to_pass = None
            else:
                note_to_pass = selected_note
                
            selected_value = values['-VALUE-']
            if len(selected_note) == 2:
                alteration_to_draw = selected_note[1]
            else:
                alteration_to_draw = False
                
            if selected_value == 'Half':
                value_to_pass = 2
                selected_half = True
            else:
                value_to_pass = 4
                selected_half = False
            
            selected_measure = values['-MEASURE-']
            

            if selected_staff == 'Upper':                 #Add the note to the upper melody
                successful = imitate.upper.add_note(note_to_pass, int(selected_measure), value_to_pass)
                if successful == True:
                    if selected_measure in used_measures_upper:
                        if selected_note != 'Rest':
                            notes_to_draw_upper[f'{selected_measure}a'] = ([MEASURE_POSITION[selected_measure] + MEASURE_DISTANCE, NOTES_POSITION_UPPER[selected_note[0]], alteration_to_draw, selected_half, False])
                            used_measures_upper.add(f'{selected_measure}a')
                        else:
                            notes_to_draw_upper[f'{selected_measure}a'] = ([MEASURE_POSITION[selected_measure]  + MEASURE_DISTANCE, NOTES_POSITION_UPPER['R'], alteration_to_draw, selected_half, True])
                            used_measures_upper.add(f'{selected_measure}a')
                    else:
                        if selected_note != 'Rest':
                            notes_to_draw_upper[selected_measure] = ([MEASURE_POSITION[selected_measure], NOTES_POSITION_UPPER[selected_note[0]], alteration_to_draw, selected_half, False])
                            used_measures_upper.add(selected_measure)
                        else:
                            notes_to_draw_upper[selected_measure] = ([MEASURE_POSITION[selected_measure] , NOTES_POSITION_UPPER['R'], alteration_to_draw, selected_half, True])
                            used_measures_upper.add(selected_measure)
                
                else:
                    sg.popup_no_buttons('There is no space in this measure!', title= 'Error', auto_close= True, auto_close_duration= 2)
                        
            elif selected_staff == 'Lower':               #Add the note to the lower melody
                successful = imitate.lower.add_note(note_to_pass, int(selected_measure), value_to_pass)
                if successful == True:
                    if selected_measure in used_measures_lower:
                        if selected_note != 'Rest':
                            notes_to_draw_lower[f'{selected_measure}a'] = ([MEASURE_POSITION[selected_measure] + MEASURE_DISTANCE, NOTES_POSITION_LOWER[selected_note[0]], alteration_to_draw, selected_half, False])
                            used_measures_lower.add(f'{selected_measure}a')
                        else:
                            notes_to_draw_lower[f'{selected_measure}a'] = ([MEASURE_POSITION[selected_measure]  + MEASURE_DISTANCE, NOTES_POSITION_LOWER['R'], alteration_to_draw, selected_half, True])
                            used_measures_lower.add(f'{selected_measure}a')
                    else:
                        if selected_note != 'Rest':
                            notes_to_draw_lower[selected_measure] = ([MEASURE_POSITION[selected_measure], NOTES_POSITION_LOWER[selected_note[0]], alteration_to_draw, selected_half, False])
                            used_measures_lower.add(selected_measure)
                        else:
                            notes_to_draw_lower[selected_measure] = ([MEASURE_POSITION[selected_measure] , NOTES_POSITION_LOWER['R'], alteration_to_draw, selected_half, True])
                            used_measures_lower.add(selected_measure)
                
                else:
                    sg.popup_no_buttons('There is no space in this measure!', title= 'Error', auto_close= True, auto_close_duration= 2)
    
        draw_notes(notes_to_draw_upper, notes_to_draw_lower, field)   
                                                    
                                                    #OCTAVE ABOVE
    
    if event == '-OUPPER-':                              
        current_staff = values['-STAFF-']
        current_measure = values['-MEASURE-']
        
        if current_staff == 'Upper':
            if f'{current_measure}a' in used_measures_upper:
                current_note = notes_to_draw_upper[f'{current_measure}a']
                if current_note[4] == False and current_note[1] < NOTES_POSITION_UPPER['A']:
                    current_note[1] += OCTAVE_DISTANCE
            
            elif current_measure in used_measures_upper and not f'{current_measure}a' in used_measures_upper:
                current_note = notes_to_draw_upper[current_measure]
                if current_note[4] == False and current_note[1]  < NOTES_POSITION_UPPER['A']:
                    current_note[1] += OCTAVE_DISTANCE
                
        elif current_staff == 'Lower':
            if f'{current_measure}a' in used_measures_lower:
                current_note = notes_to_draw_lower[f'{current_measure}a']
                if current_note[4] == False and current_note[1] < NOTES_POSITION_LOWER['E']:
                    current_note[1] += OCTAVE_DISTANCE
            
            elif current_measure in used_measures_lower and not f'{current_measure}a' in used_measures_lower:
                current_note = notes_to_draw_lower[current_measure]
                if current_note[4] == False and current_note[1] < NOTES_POSITION_LOWER['E']:
                    current_note[1] += OCTAVE_DISTANCE

        field.draw_image('staff.png', location= (10, 260))
        draw_notes(notes_to_draw_upper, notes_to_draw_lower, field)   
    
    
                                                            #OCTAVE BELOW
    if event == '-OLOWER-':
        current_staff = values['-STAFF-']
        current_measure = values['-MEASURE-']
        
        if current_staff == 'Upper':
            if f'{current_measure}a' in used_measures_upper:
                current_note = notes_to_draw_upper[f'{current_measure}a']
                if current_note[4] == False and current_note[1] > NOTES_POSITION_UPPER['A']:
                    current_note[1] -= OCTAVE_DISTANCE
                    
            
            elif current_measure in used_measures_upper and not f'{current_measure}a' in used_measures_upper:
                current_note = notes_to_draw_upper[current_measure]
                if current_note[4] == False and current_note[1] > NOTES_POSITION_UPPER['A']:
                    current_note[1] -= OCTAVE_DISTANCE
                    
                
        elif current_staff == 'Lower':
            if f'{current_measure}a' in used_measures_lower:
                current_note = notes_to_draw_lower[f'{current_measure}a']
                if current_note[4] == False and current_note[1] > NOTES_POSITION_LOWER['E']:
                    current_note[1] -= OCTAVE_DISTANCE
            
            elif current_measure in used_measures_lower and not f'{current_measure}a' in used_measures_lower:
                current_note = notes_to_draw_lower[current_measure]
                if current_note[4] == False and current_note[1] > NOTES_POSITION_LOWER['E']:
                    current_note[1] -= OCTAVE_DISTANCE
        
        field.draw_image('staff.png', location= (10, 260))
        draw_notes(notes_to_draw_upper, notes_to_draw_lower, field)   
    
    
                                                            #DELETE SINGLE N BUTTON
    if event == '-DELETE_NOTE-':
        delete_complete_form = True
        options = ['-DELETE_STAFF-', '-DELETE_MEASURE-']
        for option in options:
            if len(values[option]) == 0:
                sg.popup_no_buttons('Please select an option in every field!', title= 'Error', auto_close= True, auto_close_duration= 2)
                delete_complete_form = False
                break
        
    
        if delete_complete_form == True:
            delete_staff = values['-DELETE_STAFF-']
            delete_measure = values['-DELETE_MEASURE-']
            
            if delete_staff == 'Upper':                   #Delete a note from the upper melody
                successful = imitate.upper.remove_last_note(int(delete_measure))
                if successful == True:
                    if f'{delete_measure}a' in used_measures_upper:
                        used_measures_upper.remove(f'{delete_measure}a')
                        notes_to_draw_upper.pop(f'{delete_measure}a')

                    elif delete_measure in used_measures_upper and not f'{delete_measure}a' in used_measures_upper:
                        used_measures_upper.remove(delete_measure)
                        notes_to_draw_upper.pop(delete_measure)
                        
                    field.draw_image('staff.png', location= (10, 260))
                    draw_notes(notes_to_draw_upper, notes_to_draw_lower, field)   
                else:
                    sg.popup_no_buttons('There are no notes to delete in this measure!', title= 'Error', auto_close= True, auto_close_duration= 2)
            
            elif delete_staff == 'Lower':                 #Delete a note from the lower melody
                successful = imitate.lower.remove_last_note(int(delete_measure))
                if successful == True:
                    if f'{delete_measure}a' in used_measures_lower:
                        used_measures_lower.remove(f'{delete_measure}a')
                        notes_to_draw_lower.pop(f'{delete_measure}a')

                    elif delete_measure in used_measures_lower and not f'{delete_measure}a' in used_measures_lower:
                        used_measures_lower.remove(delete_measure)
                        notes_to_draw_lower.pop(delete_measure)
                    
                    field.draw_image('staff.png', location= (10, 260))
                    draw_notes(notes_to_draw_upper, notes_to_draw_lower, field)   
                
                else:
                    sg.popup_no_buttons('There are no notes to delete in this measure!', title= 'Error', auto_close= True, auto_close_duration= 2)
           
                                                        #DELETE ALL NOTES
                                                        
    if event == '-DELETE_ALL-':
        notes_to_draw_upper.clear()
        notes_to_draw_lower.clear()
        used_measures_upper.clear()
        used_measures_lower.clear()
        imitate = Imitation()
        field.draw_image('staff.png', location= (10, 260))
        draw_notes(notes_to_draw_upper, notes_to_draw_lower, field)   
                    
        
                
                                                        #GET THE MISTAKES IN THE COMPOSITION        
    if event == '-EXAMINE-':
        message = imitate.get_mistakes()
        if len(message) > 0:
            window['-STATS-'].update(message)
    
    if event == '-CLEAN_STATS-':
        message = 'Click examine composition to see here the results'
        window['-STATS-'].update(message)
        
    
    if event == 'Welcome':
        guide_window_func()
        
    if event == 'Imitation at the 8th':
        imitation_octave_window()

    if event == 'Imitation at the 5th':
        imitation_fifth_window()

    
window.close()

#print(sg.Text.fonts_installed_list())