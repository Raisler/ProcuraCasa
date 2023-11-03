import re
class Cleaning:
    def __init__():
        pass 
    
    def price(text):
        return re.sub(r'[^0-9]', '', text).strip()
    
    def n_room(text):
        n = re.sub(r'[^0-9]', '', text).strip()
        if len(n) > 0:
            return n 
        else:
            return -1
        
    def area(text):
        return re.sub(r'm²', '', text).strip()