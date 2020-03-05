
from utils.BidConst import BidConst
from decimal import *

mycontext = Context(prec=BidConst.CAL_SCALE(), rounding=ROUND_HALF_UP)
setcontext(mycontext)

class DecimalFormatUtil:
    @classmethod
    def amountformat(cls, number):
        number = Decimal(str(number)).quantize(Decimal('.0000'), rounding=ROUND_HALF_UP)
        return number

    @classmethod
    def formatBigDecimal(cls,data, scal):
        data = Decimal(str(data))
        if scal == BidConst.STORE_SCALE():
            return data.quantize(Decimal('0.0000'), rounding=ROUND_HALF_UP)
        elif scal == BidConst.DISPLAY_SCALE():
            return data.quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
        #“Ï≥£¥¶¿Ì
        return data