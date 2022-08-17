


class Melody:
    def __init__(self, measures, timesignature):
        self.measures = measures
        self.staff = [[] for _ in range(measures)]
        self.time_signature = timesignature
        self.measure_spaces = [[timesignature] for _ in range(measures)]  #keep track of the values available in each measure

        
    def add_note(self, note, measure, value):
        measure = measure - 1  #optional
        if measure > len(self.staff) - 1 or self.measure_spaces[measure][0] - value < 0:
            # print('Invalid input')
            return False

        self.staff[measure].append((note, value))
        
        self.measure_spaces[measure][0] -= value
        
        return True
        
    def remove_last_note(self, measure):
        measure = measure - 1   #optional
        if measure > len(self.staff) - 1 or len(self.staff[measure]) < 1:
            # print('No notes available to delete')
            return False
        
        note_removed = self.staff[measure].pop()
        
        self.measure_spaces[measure][0] += note_removed[1]
        
        return True
        
    def __repr__(self):
        string = ''
        for measure in self.staff:
            string += f'{measure} ->'
        return string
    
    def __str__(self):
        return self.__repr__()
            
        
        

# melody_1 = Melody(4, 4)
# # print(melody_1)
# melody_1.add_note('C', 0, 2)
# # print(melody_1)
# # print(melody_1.measure_spaces)
# melody_1.remove_last_note(0)
# # print(melody_1)
# # print(melody_1.measure_spaces)
# melody_1.add_note('C#', 0, 2)
# melody_1.add_note('E', 0, 2)
# # print(melody_1)
# melody_1.add_note('F', 1, 2)
# print(melody_1)
# print(melody_1.measure_spaces)