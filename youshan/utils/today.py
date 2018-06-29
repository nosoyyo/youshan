import time


def formatToday() -> str:
    ahora = time.localtime()

    def zero(inp: int) -> str:
        if len(str(inp)) != 2:
            return '0' + str(inp)
        else:
            return str(inp)
    return str(ahora.tm_year) + zero(ahora.tm_mon) + zero(ahora.tm_mday)
