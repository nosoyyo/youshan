import time
from datetime import datetime, timedelta


def formatToday(timetuple=None, timestamp=None, day: str=None) -> str:
    '''
    Arg(s) must be explicitly named.
    '''
    if timetuple:
        ahora = timetuple
    elif timestamp:
        ahora = time.localtime(timestamp)
    elif day == 'yesterday':
        yesterday = datetime.today() + timedelta(days=-1)
        ahora = time.localtime(yesterday.timestamp())
    else:
        ahora = time.localtime()

    def zero(inp: int) -> str:
        if len(str(inp)) != 2:
            return '0' + str(inp)
        else:
            return str(inp)
    return str(ahora.tm_year) + zero(ahora.tm_mon) + zero(ahora.tm_mday)
