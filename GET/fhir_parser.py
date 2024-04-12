import logging

from validation import Validate

# Create logger, define formatter and the handler for the logger
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

formatter = logging.Formatter("%(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
LOG.addHandler(handler)

class FHIR_message:
    @staticmethod
    def run(item, **kwargs):
        """
        Parse an item retrieved from a DynamoDB table to FHIR format
        
        Parameters:
            item: item from a DynamoDB table
            
        Returns:
            an FHIR formated element
        """
        
        try:
            
            # Check for the desired segments
            segment_keys = item.keys()
            if not Validate.segments:
                LOG.error("The message doesn't have the expected segments")
                return None
            # Validate segments
            pid_data = item['PID']
            if not Validate.PID(pid_data):
                LOG.error('Invalid PID segment')
                return None
            sch_data = item['SCH']
            if not Validate.SCH(sch_data):
                LOG.error('Invalid SCH segment')
                return None
            # Create the fhir object
            fhir_object = {
                'resourceType': 'Patient',
                'id': pid_data['Patient ID'],
                'name': {
                    'First Name': pid_data['Name']['First Name'],
                    'Last Name': pid_data['Name']['Last Name']
                },
                'schedule': {
                'id': sch_data['Scheduled ID'],
                'start': sch_data['Start Date'],
                'end': sch_data['End Date']
                }
            }
            return fhir_object
        except Exception as e:
            LOG.error(f'Error parsing item: {e}')
            return None