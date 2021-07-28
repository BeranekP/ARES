import requests
import xml.etree.ElementTree as ET

from lib import get_subject_type as gst

def get(id) -> dict:
        '''
        Connects to ARES, receives XML response, parse useful data
        returns - dict {'name': subject_name, 'ic': subject_ic, 'town': subject_town,
                'street':ubject_street, 'house_no': .subject_house_no, 'zipcode': subject_zipcode, 'pf': subject_pf}
                or Not found
        '''
        response = requests.get(f"https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi?ico={id}")
        xml = ET.fromstring(response.content.decode('utf-8'))
        tree = ET.ElementTree(xml)
        root = tree.getroot()

        subject_type: str = None
        subject_name: str = None
        subject_id: str = None
        subject_town: str = None
        subject_town_part: str = None
        subject_street: str = None
        subject_house_no: str = None
        subject_zipcode: str = None
        
        try:
            for tp in root.iter('{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4}Kod_PF'):
                subject_type = gst.get_subject_type(tp.text)
            for name in root.iter('{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1}Obchodni_firma'):
                subject_name = name.text
            for ico in root.iter('{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_answer/v_1.0.1}ICO'):
                subject_id = ico.text
            for town in root.iter('{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4}Nazev_obce'):
                subject_town = town.text
            for town_part in root.iter('{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4}Nazev_casti_obce'):
                subject_town_part = town_part.text
            for street in root.iter('{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4}Nazev_ulice'):
                subject_street = street.text
            for house_no in root.iter('{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4}Cislo_domovni'):
                subject_house_no = house_no.text
            for zipcode in root.iter('{http://wwwinfo.mfcr.cz/ares/xml_doc/schemas/ares/ares_datatypes/v_1.0.4}PSC'):
                subject_zipcode = zipcode.text

            if not subject_street:
                subject_street = subject_town_part

            return {'name': subject_name,
                    'id': subject_id, 
                    'town': subject_town,
                    'street': subject_street,
                    'house_no': subject_house_no,
                    'zipcode': subject_zipcode,
                    'type': subject_type}
        except Exception as e:
            return {"Not found": e}
