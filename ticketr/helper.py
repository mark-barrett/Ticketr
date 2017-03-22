import string, random


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

    @staticmethod
    def token_generator(size=6, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def remove_key(value, arg):
        return value.split(arg)[0]
