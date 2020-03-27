# coding=gbk
from decimal import *
from utils.BidConst import BidConst
from utils.DecimalFormatUtil import DecimalFormatUtil



class CalculatetUtil:
    __ONE_HUNDRED = Decimal('100.0000')#1/100
    __NUMBER_MONTHS_OF_YEAR = Decimal('12.0000')
    __ACCOUNT_MANAGER_CHARGE_RATE = Decimal('0.050') #管理费用
    __INTEREST_MANAGER_CHARGE_RATE = Decimal('0.1000')# 管理利息

    # 计算每月的利率
    @classmethod
    def getMonthlyRate(cls, yearRate):
        if yearRate == 0:
            return 0
        return yearRate / cls.__ONE_HUNDRED / cls.__NUMBER_MONTHS_OF_YEAR

#这个bug先留着，数据不精确
    @classmethod
    def cal_set(cls):
        # 设置全文计算精度和取值方式
        mycontext = Context(prec=BidConst.CAL_SCALE(), rounding=ROUND_HALF_UP)
        setcontext(mycontext)
        # 定义运算精度
    # / **
    # *计算借款总利息
    # *
    # * @ param
    # returnType
    # *还款类型
    # * @ param
    # bidRequestAmount
    # *借款金额
    # * @ param
    # yearRate
    # *年利率
    # * @ param
    # monthes2Return
    # *还款期限
    # * @ return
    # * /    # *计算借款总利息
    @classmethod
    def calTotalInterest(cls,returnType, bidRequestAmount, yearRate, monthes2Return):
        # cls.cal_set()

        bidRequestAmount = Decimal(str(bidRequestAmount))
        yearRate = Decimal(str(yearRate))
        totalInterest = Decimal('0.0000')
        monthlyRate = cls.getMonthlyRate(yearRate)
        if returnType == BidConst.GET_RETURN_TYPE_MONTH_INTEREST_PRINCIPAL(): #按月分期
            #只借款一个月
            if monthes2Return == 1:
                totalInterest = bidRequestAmount * monthlyRate
            else:
                temp1 = bidRequestAmount * monthlyRate
                temp2 = pow((Decimal('1') + monthlyRate), monthes2Return)
                temp3 = pow((Decimal('1') + monthlyRate),monthes2Return) - Decimal('1')
                #计算每月还款
                monthToReturnMoney = (temp1 * temp2) / temp3
                #计算总还款
                totalReturnMoney = monthToReturnMoney * Decimal(str(monthes2Return))
                #算出利息
                totalInterest = totalReturnMoney - bidRequestAmount
        elif returnType == BidConst.GET_RETURN_TYPE_MONTH_INTEREST(): #按月到期
            monthlyInterest = DecimalFormatUtil.amountformat((bidRequestAmount * monthlyRate))
            totalInterest = monthlyInterest * monthes2Return

        return  DecimalFormatUtil.formatBigDecimal(totalInterest, BidConst.STORE_SCALE())

# / **
# *计算每期利息
# *
# * @ param
# returnType
# *还款类型
# * @ param
# bidRequestAmount
# *借款金额
# * @ param
# yearRate
# *年利率
# * @ param
# monthIndex
# *第几期
# * @ param
# monthes2Return
# *还款期限
# * @ return
# * /
    @classmethod
    def calMonthlyInterest(cls, returnType,  bidRequestAmount, yearRate, monthIndex, monthes2Return):
        # cls.cal_set()

        bidRequestAmount = Decimal(str(bidRequestAmount))
        yearRate = Decimal(str(yearRate))
        monthlyInterest = Decimal('0.0000')
        monthlyRate = cls.getMonthlyRate(yearRate)
        if returnType == BidConst.GET_RETURN_TYPE_MONTH_INTEREST_PRINCIPAL(): #按月分期
            if monthes2Return == 1: #只借一个月
                monthlyInterest = bidRequestAmount * monthlyRate
            else:
                temp1 = bidRequestAmount * monthlyRate
                temp2 = pow(Decimal('1') + monthlyRate, monthes2Return)
                temp3 = pow(Decimal('1') + monthlyRate, monthes2Return) - Decimal('1')
                temp4 = pow(Decimal('1') + monthlyRate, monthIndex-1)
                #计算每月还款
                monthToReturnMoney = (temp1 * temp2) / temp3
                #算出总还款
                totalReturnMoney = monthToReturnMoney * Decimal(str(monthes2Return))
                #算出利息
                totalInterest = totalReturnMoney - bidRequestAmount

                if monthIndex < monthes2Return:
                    monthlyInterest = ((temp1 - monthToReturnMoney) * temp4)+monthToReturnMoney

                elif monthIndex == monthes2Return:
                    temp6 = Decimal('0.0000')
                    # 汇总最后一期之前所有利息之和
                    for i in range(1,monthes2Return):
                        temp5 = pow(Decimal('1') + monthlyRate, i-1)
                        monthlyInterest = ((temp1 - monthToReturnMoney) * temp5) + monthToReturnMoney
                        temp6 = temp6 + monthlyInterest

                    monthlyInterest = totalInterest - temp6

                    # for
        elif returnType == BidConst.GET_RETURN_TYPE_MONTH_INTEREST(): #按月到期
            monthlyInterest = DecimalFormatUtil.amountformat((bidRequestAmount * monthlyRate))

        return monthlyInterest

# / **
# *计算每期还款
# *
# * @ param
# returnType
# *还款类型
# * @ param
# bidRequestAmount
# *借款金额
# * @ param
# yearRate
# *年利率
# * @ param
# monthIndex
# *第几期
# * @ param
# monthes2Return
# *还款期限
# * @ return
# * /
    @classmethod
    def calMonthToReturnMoney(cls, returnType, bidRequestAmount,  yearRate, monthIndex, monthes2Return):
        # cls.cal_set()

        bidRequestAmount = Decimal(str(bidRequestAmount))
        yearRate = Decimal(str(yearRate))
        monthToReturnMoney =  Decimal('0.0000')
        monthlyRate = cls.getMonthlyRate(yearRate)
        if returnType == BidConst.GET_RETURN_TYPE_MONTH_INTEREST_PRINCIPAL():#按月分期
            if monthes2Return == 1:  # 只借一个月
                monthlyInterest = bidRequestAmount + (bidRequestAmount * monthlyRate)
            else:
                temp1 = bidRequestAmount * monthlyRate
                temp2 = pow(Decimal('1') + monthlyRate, monthes2Return)
                temp3 = pow(Decimal('1') + monthlyRate, monthes2Return) - Decimal('1')
                #计算每月还款
                monthToReturnMoney = (temp1 * temp2) / temp3
        elif returnType == BidConst.GET_RETURN_TYPE_MONTH_INTEREST(): #按月到期
            monthlyInterest = bidRequestAmount * monthlyRate
            if monthIndex == monthes2Return:
                monthToReturnMoney = bidRequestAmount + monthlyInterest
            elif monthIndex < monthes2Return:
                monthToReturnMoney = monthlyInterest
        return DecimalFormatUtil.formatBigDecimal(monthToReturnMoney,BidConst.STORE_SCALE())

# / **
# *计算一次投标实际获得的利息 = 投标金额 / 借款金额 * 总利息
# *
# * @ param
# bidRequestAmount
# *借款金额
# * @ param
# monthes2Return
# *还款期数
# * @ param
# yearRate
# *年利率
# * @ param
# returnType
# *还款类型
# * @ param
# acturalBidAmount
# *投标金额
# * @ return
# * /
    @classmethod
    def calBidInterest(cls, bidRequestAmount, monthes2Return,yearRate,  returnType, acturalBidAmount):
        cls.cal_set()

        acturalBidAmount =Decimal(str(acturalBidAmount))
        #// 借款产生的总利息
        totalInterest = cls.calTotalInterest(returnType, bidRequestAmount, yearRate, monthes2Return)
        #// 所占比例
        proportion = acturalBidAmount / bidRequestAmount
        bidInterest = totalInterest * proportion
        return DecimalFormatUtil.formatBigDecimal(bidInterest, BidConst.STORE_SCALE())

# / **
# *计算利息管理费
# *
# * @ param
# interest
# *利息
# * @ param
# interestManagerChargeRate
# *利息管理费比例
# * @ return
# * /
    @classmethod
    def calInterestManagerCharge(cls, interest):
        interest =Decimal(str(interest))
        return DecimalFormatUtil.formatBigDecimal(interest * cls.__INTEREST_MANAGER_CHARGE_RATE, BidConst.STORE_SCALE())


# / **
# *计算借款管理费
# *
# * @ param
# bidRequestAmount
# *借款金额
# * @ param
# returnType
# *还款类型
# * @ param
# monthes2Return
# *还款期限
# * @ return
# * /
    @classmethod
    def calAccountManagementCharge(cls,bidRequestAmount):
        bidRequestAmount = Decimal(str(bidRequestAmount))
        accountManagementCharge = DecimalFormatUtil.formatBigDecimal(bidRequestAmount * cls.__ACCOUNT_MANAGER_CHARGE_RATE, BidConst.STORE_SCALE())
        return accountManagementCharge