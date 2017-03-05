class Helper:

    def __init__(self):
        pass

    @staticmethod
    def date(date):
        # Create event object with fields
        months = ""+date[0]+date[1]
        days = ""+date[3]+date[4]
        year = ""+date[6]+date[7]+date[8]+date[9]
        return year+"-"+months+"-"+days