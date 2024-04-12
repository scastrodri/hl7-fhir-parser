import logging
import re

# Create logger, define formatter and the handler for the logger
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

formatter = logging.Formatter("%(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
LOG.addHandler(handler)


class Validate:
    @staticmethod
    def SCH(segment:str, **kwargs)->bool:
        """
        Validate if the segment it's an appropriated SCH

        Parameters:
            segment: a str

        Returns:
            Boolean: True or False
        """

        fields = segment.split('|')

        if len(fields) != 8:
            LOG.info("The SCH segment doesn't have the amount of fields expected")
            return False

        # Some patterns to validate through regex
        appointment_pattern = r"^\d{8}$"
        date_pattern = r"^\d{14}$"
        
        placer_appointment_id = fields[2]
        filler_appointment_id = fields[3]

        if not re.match(appointment_pattern, placer_appointment_id) or not re.match(appointment_pattern, filler_appointment_id):
            LOG.info("One of the appointment fields doesn't have the appropriated pattern")
            return False
        if not re.match(date_pattern, fields[5]) or not re.match(date_pattern, fields[6]):
            LOG.info("One of the date fields doesn't have the appropriated pattern")
            return False
        return True
    
    @staticmethod
    def PID(segment:str, **kwargs)->bool:
        """
        Validate if the segment it's an appropriated PID

        Parameters:
            segment: a str

        Returns:
            Boolean: True or False
        """
        fields = segment.split('|')

        if len(fields) != 19:
            LOG.info("The PID segment doesn't have the amount of fields expected")
            return False

        # Some patterns to validate through regex
        mrn_pattern = r"^\d{10}$"
        name_pattern = r"^[a-zA-Z]+$"

        first_name = fields[5].split('^')[0]
        last_name = fields[5].split('^')[1]
        
        if not re.match(mrn_pattern, fields[2]):
            LOG.info("The MRN field doesn't have all the 10 digits expected")
            return False
        if not re.match(name_pattern, first_name) or not re.match(name_pattern, last_name):
            LOG.info("The first name or last name is not completely letters")
            return False
        return True