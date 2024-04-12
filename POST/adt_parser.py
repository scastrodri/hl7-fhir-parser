import logging

from validation import Validate

# Create logger, define formatter and the handler for the logger
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)

formatter = logging.Formatter("%(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
LOG.addHandler(handler)

class ADT_Messages:
    @staticmethod
    def run(message, **kwargs):
        """
        Process ADT messages

        Parameters:
            message: a str message

        Returns:
            Data: info retrieved from the message or None if there's an error
        """


        try:
            # Reading the message and getting the segments 
            segments_data = message.strip().splitlines()

            # Validate segments
            for segment in segments_data:
                if not segment or '|' not in segment:
                    return LOG.info(f"Invalid segment format: {segment}")

            segments_labels = [segment.split('|')[0] for segment in segments_data]

            # Considering single message, not a batch, check if it's a valid HL7 message
            if segments_labels[0] != 'MSH':
                return LOG.info('Not an appropriate HL7 message')
            
            # Process segments
            data = {}
            pid_data = {}
            sch_data = {}
            
            if ('PID' and 'SCH') in segments_labels: # As much segments required, could be a method to validate
                for segment in segments_data:
                    fields = segment.split('|')
                    segment_type = fields[0]

                    
                    # Considering just some mandatory PID fields
                    if segment_type == "PID":
                        try:
                            if Validate.PID(segment):
                                try:
                                    pid_data['Patient ID'] = fields[3]
                                    pid_data['MRN'] = fields[2]
                                    pid_data['Name'] = {
                                        'Last Name': fields[5].split('^')[1],
                                        'First Name': fields[5].split('^')[0]
                                        }
                                    pid_data['Address'] = {
                                        'Country':fields[11].split('^')[5],
                                        'Zip Code':fields[11].split('^')[4],
                                        'Estate':fields[11].split('^')[3],
                                        'City':fields[11].split('^')[2],
                                        'Number':fields[11].split('^')[0],}
                                    LOG.info('All the PID data retrieved')
                                except Exception as e:
                                    return LOG.info(f'An error has ocurred during the message processing for PID segment: {str(e)}')
                            else:
                                return LOG.info("Not validate PID segment")
                        except Exception as e:
                            return e
                    # Considering the mandatory PID fields
                    elif segment_type == "SCH":
                        try:
                            if Validate.SCH(segment):
                                try:
                                    sch_data["Scheduled ID"] = fields[1]
                                    sch_data["Placer Appointment ID"] = fields[2]
                                    sch_data["Filler Appointment ID"] = fields[3]
                                    sch_data["Planned Appointment ID"] = fields[4]
                                    sch_data["Start Date"] = fields[5]
                                    sch_data["End Date"] = fields[6]
                                    sch_data["Scheduled Activity Code"] = fields[7]
                                    LOG.info('All the SCH data retrieved')
                                except Exception as e:
                                    return LOG.info('An error has ocurred during the message processing for SCH segment: %s', str(e))
                            else:
                                return LOG.info("Not validate PID segment")
                        except Exception as e:
                            return e
                data['PID'] = pid_data
                data['SCH'] = sch_data            
                return data
            
        except (IOError, UnicodeDecodeError) as e:
            return LOG.info(f"Error processing file: {str(e)}")
        except ValueError as e:
            return LOG.info(str(e))