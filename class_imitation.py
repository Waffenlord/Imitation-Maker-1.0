from intervals import Scale
from melodies import Melody



class Imitation:
    def __init__(self):
        self.upper = Melody(8, 4)
        self.lower = Melody(8, 4)

  
    def count_intervals(self, lower_mel, upper_mel):
        scale = Scale()
        intervals_description = {}
        
        i, j = 0, 0
        
        while i < lower_mel.measures and j < upper_mel.measures:   #Check each measure
            intervals_lst = []
            if len(lower_mel.staff[i]) < 1 or len(upper_mel.staff[j]) < 1:
                i += 1
                j += 1
                continue
            
            n1, n2 = 0, 0
            while n1 < len(lower_mel.staff[i]) and n2 < len(upper_mel.staff[j]):  #Check each note
                if lower_mel.staff[i][n1][0] == None or upper_mel.staff[j][n2][0] == None:
                    n1 += 1
                    n2 += 1
                    continue
                
                distance = scale.get_interval(lower_mel.staff[i][n1][0], upper_mel.staff[j][n2][0])  #Get the interval for each pair of notes
                intervals_lst.append((distance, n1))
                n1 += 1
                n2 += 1
            
            intervals_description[i] = intervals_lst  #add the intervals for each measure to the dictionary
                
            i += 1
            j += 1
                
        return intervals_description
            
    
    def get_bad_intervals(self, total_intervals):
        bad_intervals = {0.5: 'Minor second', 1.0: 'Mayor second', 2.5: 'Perfect fourth', 3.0: 'Tritone', 5.0: 'Minor seventh', 5.5: 'Mayor seventh'}
        bad_notes = {}
        for key in total_intervals:   #Check each measure
            notes_lst = []
            for note in total_intervals[key]:  #Check each note
                if note[0] in bad_intervals:
                    notes_lst.append((bad_intervals[note[0]], note[1]))   #Add the string translation of the bad interval
            
            if len(notes_lst) > 0:                 #Append only the bad intervals
                bad_notes[key] = notes_lst
        
        return bad_notes

    def get_mistakes(self):
        all_intervals = self.count_intervals(self.lower, self.upper)
        bad_intervals = self.get_bad_intervals(all_intervals)
        
        error_message = ''
                                                                 
        if len(bad_intervals) > 0:                                #Disonances
            for key in bad_intervals:
                for note in bad_intervals[key]:
                    if key == 6:
                        error_message += f'- Caution: Measure {key + 1}. There is a {note[0]} at position {note[1] + 1}. \n           If it is part of the cadence ignore this message. \n'
                    else:
                        if note[1] + 1 == 1:
                            error_message += f'- Caution: Measure {key + 1}. There is a {note[0]} at position {note[1] + 1}. \n           If you are in four species check if the dissonance is justified by the previous note. \n'
                        else:
                            error_message += f'- Error: Measure {key + 1}. There is a {note[0]} at position {note[1] + 1}. \n'           
        
        previous = None
        for key in all_intervals:                                 #Parallel fifths and parallel octaves
            for note in all_intervals[key]:
                # print('previous',previous)
                # print('current', note)
                if previous == None:
                    previous = note
                    continue
                else:
                    if previous[0] == 3.5 and note[0] == 3.5:
                        error_message += f'Caution: Measure {key + 1}. There are two consecutive perfect fifths.\n         Check they are not in parallel motion. \n'
                    elif previous[0] == 0.0 and note[0] == 0.0:
                        error_message += f'Caution: Measure {key + 1}. There are two consecutive perfect octaves.\n         Check they are not in parallel motion. \n'
                previous = note
        
        return error_message
        
        
        
        

# exercise = Imitation()
# exercise.upper.add_note(None, 0, 2)
# exercise.upper.add_note('G', 0, 2)
# exercise.upper.add_note('F', 1, 2)
# exercise.upper.add_note('A', 1, 2)
# exercise.upper.add_note('G', 2, 2)
# exercise.upper.add_note('D', 2, 2)
# exercise.upper.add_note('D', 3, 2)
# exercise.upper.add_note('C', 3, 2)
# exercise.upper.add_note('B', 4, 2)
# exercise.upper.add_note('F#', 4, 2)
# exercise.upper.add_note('E', 5, 2)
# exercise.upper.add_note('C', 5, 2)
# exercise.upper.add_note('D', 6, 4)
# exercise.upper.add_note('C', 7, 4)


# exercise.lower.add_note('C', 0, 2)
# exercise.lower.add_note('B', 0, 2)
# exercise.lower.add_note('D', 1, 2)
# exercise.lower.add_note('C', 1, 2)
# exercise.lower.add_note('G', 2, 4)
# exercise.lower.add_note('F', 3, 2)
# exercise.lower.add_note('E', 3, 2)
# exercise.lower.add_note('B', 4, 2)
# exercise.lower.add_note('A', 4, 2)
# exercise.lower.add_note('A', 5, 2)
# exercise.lower.add_note('C', 5, 2)
# exercise.lower.add_note('C', 6, 2)
# exercise.lower.add_note('B', 6, 2)
# exercise.lower.add_note('C', 7, 4)


# print(exercise.upper)
# print(exercise.lower)
# print(exercise.count_intervals(exercise.lower, exercise.upper))
# print(exercise.get_mistakes())