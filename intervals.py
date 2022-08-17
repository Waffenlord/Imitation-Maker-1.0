

class Note:
    def __init__(self, key):
        self.key = key
        self.next_half = None
        self.next_note = None
        
    def __repr__(self):
        return f'{self.key} -> next {self.next_half}, {self.next_note}'
    
    def __str__(self):
        return self.__repr__()
    
    
    
class Scale:
    notes = [('C', ('C#', 'Db')), ('D', ('D#', 'Eb')), ('E', None), ('F', ('F#', 'Gb')), ('G', ('G#', 'Ab')), ('A', ('A#', 'Bb')), ('B', None)] 
    def __init__(self):
        self.head = None
        for note, half in Scale.notes:
            self._append(note, half)
        self._connect_last_note()
        
        
    def _append(self, key, next_half=None):
        if self.head == None:
            self.head = Note(key)
            self.head.next_half = next_half
            
        else:
            current = self.head
            while current.next_note:
                current = current.next_note
            
            current.next_note = Note(key)
            current.next_note.next_half = next_half
            
    def show_elements(self):
        current = self.head
        n = 7
        while n > 0:
            if current:
                print((current.key, current.next_half), '->')
                current = current.next_note
            n -= 1
            
    def _connect_last_note(self):
        current = self.head
        while current.next_note:
            current = current.next_note
        
        current.next_note = self.head
        current.next_note.next_half = self.head.next_half
        
    
    def get_interval(self, first, last):
        result = 0
        current = self.head
        while True:
            if current.key == first:
                break
            
            elif current.next_half and first in current.next_half:
                result -= 0.5
                break
    
            current = current.next_note
        
        while True:
            if current.key == last:
                break
            
            elif current.next_half and last in current.next_half:
                result += 0.5
                break
            
            elif current.next_note.key not in ['F', 'C']:
                result += 1
            
            elif current.next_note.key in ['F', 'C']:
                result += 0.5
            
            current = current.next_note
        
        
        return float(result)
                   
          
# scale = Scale()
    

# scale.show_elements()


# print(scale.get_interval('B', 'F#'))