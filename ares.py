from dataclasses import dataclass
from lib import get_subject

@dataclass
class ARES():
    '''
        Get info on registered czech economical subjects from https://wwwinfo.mfcr.cz/ares/ares_es.html.cz
        Initialized e.g. a = ARES('1234567')
    '''
    _id: str
    subject_name: str = None
    subject_id: str = None
    subject_town: str = None
    subject_street: str = None
    subject_house_no: str = None
    subject_zipcode: str = None
    subject_type:str = None
    
    def __post_init__(self):
        subject: dict = get_subject.get(self._id)
        self.subject_name = subject['name']
        self.subject_id = subject['id']
        self.subject_town = subject['town']
        self.subject_street = subject['street']
        self.subject_house_no = subject['house_no']
        self.subject_zipcode = subject['zipcode']
        self.subject_type = subject['type']

if __name__ == "__main__":
    # cmd line interface example
    _id = input('Zadejte IC: ')
    validator = ARES(_id)
    print(validator)
