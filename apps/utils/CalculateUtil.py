# coding=gbk
from decimal import *
from utils.BidConst import BidConst

#定义运算精度
getcontext().prec = 8

class CalculatetUtil:
    ONE_HUNDRED = Decimal(100.0000)
    __NUMBER_MONTHS_OF_YEAR = Decimal(12.0000)
    __ACCOUNT_MANAGER_CHARGE_RATE = Decimal(0.0500)
    __INTEREST_MANAGER_CHARGE_RATE = Decimal(0.1000)

    @classmethod
    def getMonthlyRate(cls, yearRate):
        if yearRate == None:
            return 0



x = Decimal('-3.333333333') + Decimal('-2.222222222')
print(x)   # -5.555555555
print(x.quantize(Decimal('1.0000'), ROUND_HALF_EVEN))    # -5.5556
print(x.quantize(Decimal('1.0000'), ROUND_HALF_DOWN))    # -5.5556
print(x.quantize(Decimal('1.0000'), ROUND_CEILING))      # -5.5555
print(x.quantize(Decimal('1.0000'), ROUND_FLOOR))        # -5.8599
print(x.quantize(Decimal('1.0000'), ROUND_UP))           # -5.8599
print(x.quantize(Decimal('1.0000'), ROUND_DOWN))         # -5.5555
print(x.quantize(Decimal('1.0000'), ROUND_HALF_UP))


print("我是----------")
x = Decimal('-3.333333333') + Decimal('-1.111111111')
print(x)   # 4.444444444
print(x.quantize(Decimal('1.0000'), ROUND_HALF_EVEN))    # -4.4444
print(x.quantize(Decimal('1.0000'), ROUND_HALF_DOWN))    # -4.4444
print(x.quantize(Decimal('1.0000'), ROUND_CEILING))      # -4.4444
print(x.quantize(Decimal('1.0000'), ROUND_FLOOR))        # -4.4445
print(x.quantize(Decimal('1.0000'), ROUND_UP))           # -4.4445
print(x.quantize(Decimal('1.0000'), ROUND_DOWN))         # -4.4444
print(x.quantize(Decimal('1.0000'), ROUND_HALF_UP))


print("我是----------")
x = Decimal('3.333333333') + Decimal('1.111111111')
print(x)   # 4.444444444
print(x.quantize(Decimal('1.0000'), ROUND_HALF_EVEN))    # 4.4444
print(x.quantize(Decimal('1.0000'), ROUND_HALF_DOWN))    # 4.4444
print(x.quantize(Decimal('1.0000'), ROUND_CEILING))      # 4.4445
print(x.quantize(Decimal('1.0000'), ROUND_FLOOR))        # 4.4444
print(x.quantize(Decimal('1.0000'), ROUND_UP))           # 4.4445
print(x.quantize(Decimal('1.0000'), ROUND_DOWN))         # 4.4444
print(x.quantize(Decimal('1.0000'), ROUND_HALF_UP))


x = Decimal('3.333333333') + Decimal('2.222222222')
print(x)   # 5.555555555
print(x.quantize(Decimal('1.0000'), ROUND_HALF_EVEN))    # 5.5556
print(x.quantize(Decimal('1.0000'), ROUND_HALF_DOWN))    # 5.5556
print(x.quantize(Decimal('1.0000'), ROUND_CEILING))      # 5.5556
print(x.quantize(Decimal('1.0000'), ROUND_FLOOR))        # 5.5555
print(x.quantize(Decimal('1.0000'), ROUND_UP))           # 5.5556
print(x.quantize(Decimal('1.0000'), ROUND_DOWN))         # 5.5555
print(x.quantize(Decimal('1.0000'), ROUND_HALF_UP))