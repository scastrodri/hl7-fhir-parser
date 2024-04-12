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
    def segments(item:dict, **kwargs)->bool:
        """
        Validate if the segment it's an appropriated SCH

        Parameters:
            segment: a str

        Returns:
            Boolean: True or False
        """
        expected_segments = ['PID', 'SCH']
        missing_segments = [key for key in expected_segments if key not in item.keys()]
        if missing_segments:
            LOG.error(f'Missing required keys: {", ".join(missing_segments)}')
            return False
        return True
    
    
    @staticmethod
    def PID(pid_data:dict, **kwargs)->bool:
        """
        Validate if the segment it's an appropriated PID

        Parameters:
            segment: a str

        Returns:
            Boolean: True or False
        """
        expected_keys = ['MRN', 'Patient ID', 'Name']
        missing_keys = [key for key in expected_keys if key not in pid_data]
        if missing_keys:
            LOG.error(f'The PID segment is missing the required keys: {", ".join(missing_keys)}')
            return False

        # Some patterns to validate through regex
        mrn_pattern = r"^\d{10}$"
        name_pattern = r"^[a-zA-Z]+$"
        
        mrn = pid_data['MRN']
        first_name = pid_data['Name']['First Name']
        last_name = pid_data['Name']['First Name']
        
        if not re.match(mrn_pattern, mrn):
            LOG.error("The MRN field doesn't have all the 10 digits expected")
            return False
        if not re.match(name_pattern, first_name) or not re.match(name_pattern, last_name):
            LOG.error("The first name or last name is not completely letters")
            return False
        return True
    
    
    @staticmethod
    def SCH(sch_data:dict, **kwargs)->bool:
        """
        Validate if the segment it's an appropriated SCH

        Parameters:
            segment: a str

        Returns:
            Boolean: True or False
        """

        expected_keys = ['Scheduled ID', 'Start Date', 'End Date']
        missing_keys = [key for key in expected_keys if key not in sch_data]
        if missing_keys:
            LOG.error(f'The SCH segment is missing the required keys: {", ".join(missing_keys)}')
            return False
        
        # Some patterns to validate through regex
        appointment_pattern = r"^\d{8}$"
        date_pattern = r"^\d{14}$"
        
        placer_appointment_id = sch_data['Placer Appointment ID']
        filler_appointment_id = sch_data['Filler Appointment ID']
        start_date = sch_data['Start Date']
        end_date = sch_data['End Date']

        if not re.match(appointment_pattern, placer_appointment_id) or not re.match(appointment_pattern, filler_appointment_id):
            LOG.error("One of the appointment fields doesn't have the appropriated pattern")
            return False
        if not re.match(date_pattern, start_date) or not re.match(date_pattern, end_date):
            LOG.error("One of the date fields doesn't have the appropriated pattern")
            return False
        return True