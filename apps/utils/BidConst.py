# coding=gbk

#约定  GET方法开头：只负责返回数据
      # 完整成员名：负责返回数据，并且用在数据库


class BidConst:

        # /**
     # * 定义存储精度
     # */
    __STORE_SCALE = 4
    # /**
    #  * 定义运算精度
    #  */
    __CAL_SCALE = 8

    # /**
    #  * 定义显示精度
    #  */
    __DISPLAY_SCALE = 2

    # /**
    #  * 定义系统级别的0
    #  */
    __ZERO = 0.0

    # /**
    #  * 定义初始授信额度
    #  */
    __INIT_BORROW_LIMIT = 5000.0000

    # / **
    # *要能借款需要达到的最低风控分数
    # * /
    __BASE_BORROW_SCORE = 30

    # // --------------------还款类型 - --------------------------
    __RETURN_TYPE_MONTH_INTEREST_PRINCIPAL = 0  #// 还款方式
                                                # // 按月分期还款(等额本息)

    __RETURN_TYPE_MONTH_INTEREST = 1 #// 还款方式
                                     # // 按月到期还款(每月还利息, 到期还本息)


    # // ---------------------标的类型 - -------------------------
    __BIDREQUEST_TYPE_NORMAL = 0 #// 普通信用标


    #// ---------------------借款状态 - --------------------------

    __BIDREQUEST_STATE_PUBLISH_PENDING = 0 #// 待发布
    __BIDREQUEST_STATE_BIDDING = 1 #// 招标中
    __BIDREQUEST_STATE_UNDO = 2 #// 已撤销
    __BIDREQUEST_STATE_BIDDING_OVERDUE = 3 #// 流标
    __BIDREQUEST_STATE_APPROVE_PENDING_1 = 4 #// 满标1审
    __BIDREQUEST_STATE_APPROVE_PENDING_2 = 5 #// 满标2审
    __BIDREQUEST_STATE_REJECTED = 6 #// 满标审核被拒绝
    __BIDREQUEST_STATE_PAYING_BACK = 7 #// 还款中
    __BIDREQUEST_STATE_COMPLETE_PAY_BACK = 8 #// 已还清
    __BIDREQUEST_STATE_PAY_BACK_OVERDUE = 9 #// 逾期
    __BIDREQUEST_STATE_PUBLISH_REFUSE = 10 #// 发标审核拒绝状态

    __SMALLEST_BID_AMOUNT = 50.0000 #// 系统规定的最小投标金额
    __SMALLEST_BIDREQUEST_AMOUNT = 500.0000 #// 系统规定的最小借款金额
    __SMALLEST_CURRENT_RATE = 5.0000 #// 系统最小借款利息
    __MAX_CURRENT_RATE = 20.0000 #// 系统最大借款利息
    __MIN_WITHDRAW_AMOUNT = 500.0000 #// 系统最小提现金额
    __MONEY_WITHDRAW_CHARGEFEE = 2.0000 #// 系统提现手续费

 # == == == == == == == == == == == == == == =账户流水类型 == == == == == == == == == == == == == == == ==

    __ACCOUNT_ACTIONTYPE_RECHARGE_OFFLINE = 0    #// 资金流水类别：线下充值
                                           # // 可用余额增加

    __ACCOUNT_ACTIONTYPE_WITHDRAW = 1 #// 资金流水类别：提现成功
                                    #// 冻结金额减少

    __ACCOUNT_ACTIONTYPE_BIDREQUEST_SUCCESSFUL = 2# // 资金流水类别：成功借款
                                                #// 可用余额增加

    __ACCOUNT_ACTIONTYPE_BID_SUCCESSFUL = 3 #// 资金流水类别：成功投标
                                            #// 冻结金额减少

    __ACCOUNT_ACTIONTYPE_RETURN_MONEY = 4 #// 资金流水类别：还款
                                            #// 可用余额减少

    __ACCOUNT_ACTIONTYPE_CALLBACK_MONEY = 5 #// 资金流水类别：回款
                                            #// 可用余额增加

    __ACCOUNT_ACTIONTYPE_CHARGE = 6 #// 资金流水类别：支付平台管理费
                                    #// 可用余额减少

    __ACCOUNT_ACTIONTYPE_INTEREST_SHARE = 7 #// 资金流水类别：利息管理费
                                            #// 可用余额减少

    __ACCOUNT_ACTIONTYPE_WITHDRAW_MANAGE_CHARGE = 8 #// 资金流水类别：提现手续费
                                                    #// 可用余额减少

    __ACCOUNT_ACTIONTYPE_RECHARGE_CHARGE = 9 #// 资金流水类别：充值手续费
                                            #// 可用余额减少

    __ACCOUNT_ACTIONTYPE_BID_FREEZED = 10 #// 资金流水类别：投标冻结金额
                                        #// 冻结金额增加
                                        #//可用余额减少

    __ACCOUNT_ACTIONTYPE_BID_UNFREEZED = 11 #// 资金流水类别：取消投标冻结金额
                                            #// 标审核失败
                                            #// 冻结金额减少
                                            #// 可用余额增加

    __ACCOUNT_ACTIONTYPE_WITHDRAW_FREEZED = 12 #// 资金流水类别：提现申请冻结金额
                                            #// 冻结金额增加
                                            #// 可用余额减少

    __ACCOUNT_ACTIONTYPE_WITHDRAW_UNFREEZED = 13 #// 资金流水类别: 提现申请失败取消冻结金额
                                                #// 冻结金额减少
                                                #// 可用余额增加


# / ** == == == == == == 系统账户流水类型 == == == == == == = * /

    __SYSTEM_ACCOUNT_ACTIONTYPE_MANAGE_CHARGE = 1 #// 系统账户收到账户管理费（借款管理费）

    __SYSTEM_ACCOUNT_ACTIONTYPE_INTREST_MANAGE_CHARGE = 2 #// 系统账户收到利息管理费

    __SYSTEM_ACCOUNT_ACTIONTYPE_WITHDRAW_MANAGE_CHARGE = 3 #// 系统账户收到提现手续费


# / ** == == == == =还款状态 == == == == == == == = * /

    __PAYMENT_STATE_NORMAL = 0 #// 正常待还

    __PAYMENT_STATE_DONE = 1 #// 已还

    __PAYMENT_STATE_OVERDUE = 2 #// 逾期



#类方法--------------------------------------------------------------------------《》
# =============================#约定  GET方法开头：只负责返回数据====================

    @classmethod
    def GET_RETURN_TYPE_MONTH_INTEREST_PRINCIPAL(cls):
        return cls.__RETURN_TYPE_MONTH_INTEREST_PRINCIPAL

    @classmethod
    def GET_RETURN_TYPE_MONTH_INTEREST(cls):
        return cls.__RETURN_TYPE_MONTH_INTEREST

    @classmethod
    def GET_BIDREQUEST_TYPE_NORMAL(cls):
        return cls.__BIDREQUEST_TYPE_NORMAL  # // 普通信用标
# // ---------------------借款状态 - --------------------------
    @classmethod
    def GET_BIDREQUEST_STATE_PUBLISH_PENDING(cls):
        return cls.__BIDREQUEST_STATE_PUBLISH_PENDING  # // 待发布

    @classmethod
    def GET_BIDREQUEST_STATE_BIDDING(cls):
        return cls.__BIDREQUEST_STATE_BIDDING  # // 招标中

    @classmethod
    def GET_BIDREQUEST_STATE_UNDO(cls):
        return cls.__BIDREQUEST_STATE_UNDO  # // 已撤销

    @classmethod
    def GET_BIDREQUEST_STATE_BIDDING_OVERDUE(cls):
        return cls.__BIDREQUEST_STATE_BIDDING_OVERDUE  # // 流标

    @classmethod
    def GET_BIDREQUEST_STATE_APPROVE_PENDING_1(cls):
        return cls.__BIDREQUEST_STATE_APPROVE_PENDING_1  # // 满标1审

    @classmethod
    def GET_BIDREQUEST_STATE_APPROVE_PENDING_2(cls):
        return cls.__BIDREQUEST_STATE_APPROVE_PENDING_2  # // 满标2审

    @classmethod
    def GET_BIDREQUEST_STATE_REJECTED(cls):
        return cls.__BIDREQUEST_STATE_REJECTED  # // 满标审核被拒绝

    @classmethod
    def GET_BIDREQUEST_STATE_PAYING_BACK(cls):
        return cls.__BIDREQUEST_STATE_PAYING_BACK  # // 还款中

    @classmethod
    def GET_BIDREQUEST_STATE_COMPLETE_PAY_BACK(cls):
        return cls.__BIDREQUEST_STATE_COMPLETE_PAY_BACK  # // 已还清

    @classmethod
    def GET_BIDREQUEST_STATE_PAY_BACK_OVERDUE(cls):
        return cls.__BIDREQUEST_STATE_PAY_BACK_OVERDUE  # // 逾期

    @classmethod
    def GET_BIDREQUEST_STATE_PUBLISH_REFUSE(cls):
        return cls.__BIDREQUEST_STATE_PUBLISH_REFUSE  # // 发标审核拒绝状态

 # == == == == == == == == == == == == == == =账户流水类型 == == == == == == == == == == == == == == == ==

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_RECHARGE_OFFLINE(cls):
        return cls.__ACCOUNT_ACTIONTYPE_RECHARGE_OFFLINE

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_WITHDRAW(cls):
        return cls.__ACCOUNT_ACTIONTYPE_WITHDRAW


    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_BIDREQUEST_SUCCESSFUL(cls):
        return cls.__ACCOUNT_ACTIONTYPE_BIDREQUEST_SUCCESSFUL


    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_BID_SUCCESSFUL(cls):
        return cls.__ACCOUNT_ACTIONTYPE_BID_SUCCESSFUL

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_RETURN_MONEY(cls):
        return cls.__ACCOUNT_ACTIONTYPE_RETURN_MONEY

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_CALLBACK_MONEY(cls):
        return cls.__ACCOUNT_ACTIONTYPE_CALLBACK_MONEY

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_CHARGE(cls):
        return cls.__ACCOUNT_ACTIONTYPE_CHARGE

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_INTEREST_SHARE(cls):
        return cls.__ACCOUNT_ACTIONTYPE_INTEREST_SHARE

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_WITHDRAW_MANAGE_CHARGE(cls):
        return cls.__ACCOUNT_ACTIONTYPE_WITHDRAW_MANAGE_CHARGE

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_RECHARGE_CHARGE(cls):
        return cls.__ACCOUNT_ACTIONTYPE_RECHARGE_CHARGE

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_BID_FREEZED(cls):
        return cls.__ACCOUNT_ACTIONTYPE_BID_FREEZED

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_BID_UNFREEZED(cls):
        return cls.__ACCOUNT_ACTIONTYPE_BID_UNFREEZED

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_WITHDRAW_FREEZED(cls):
        return cls.__ACCOUNT_ACTIONTYPE_WITHDRAW_FREEZED

    @classmethod
    def GET_ACCOUNT_ACTIONTYPE_WITHDRAW_UNFREEZED(cls):
        return cls.__ACCOUNT_ACTIONTYPE_WITHDRAW_UNFREEZED


# / ** == == == == == == 系统账户流水类型 == == == == == == = * /
    @classmethod
    def GET_SYSTEM_ACCOUNT_ACTIONTYPE_MANAGE_CHARGE(cls):
        return cls.__SYSTEM_ACCOUNT_ACTIONTYPE_MANAGE_CHARGE

    @classmethod
    def GET_SYSTEM_ACCOUNT_ACTIONTYPE_INTREST_MANAGE_CHARGE(cls):
        return cls.__SYSTEM_ACCOUNT_ACTIONTYPE_INTREST_MANAGE_CHARGE

    @classmethod
    def GET_SYSTEM_ACCOUNT_ACTIONTYPE_WITHDRAW_MANAGE_CHARGE(cls):
        return cls.__SYSTEM_ACCOUNT_ACTIONTYPE_WITHDRAW_MANAGE_CHARGE


# / ** == == == == =还款状态 == == == == == == == = * /
    @classmethod
    def GET_PAYMENT_STATE_NORMAL(cls):
        return cls.__PAYMENT_STATE_NORMAL
    @classmethod
    def GET_PAYMENT_STATE_DONE(cls):
        return cls.__PAYMENT_STATE_DONE
    @classmethod
    def GET_PAYMENT_STATE_OVERDUE(cls):
        return cls.__PAYMENT_STATE_OVERDUE


#类方法--------------------------------------------------------------------------《》
# =============================完整成员名：负责返回数据，并且用在数据库====================

    @classmethod
    def STORE_SCALE(cls):
        return cls.__STORE_SCALE

    @classmethod
    def CAL_SCALE(cls):
        return cls.__CAL_SCALE

    @classmethod
    def DISPLAY_SCALE(cls):
        return cls.__DISPLAY_SCALE

    @classmethod
    def ZERO(cls):
        return cls.__ZERO

    @classmethod
    def INIT_BORROW_LIMIT(cls):
        return cls.__INIT_BORROW_LIMIT

    @classmethod
    def BASE_BORROW_SCORE(cls):
        return cls.__BASE_BORROW_SCORE


    #// ---------------------借款状态 - --------------------------
    @classmethod
    def SMALLEST_BID_AMOUNT(cls):
        return cls.__SMALLEST_BID_AMOUNT

    @classmethod
    def SMALLEST_BIDREQUEST_AMOUNT(cls):
        return cls.__SMALLEST_BIDREQUEST_AMOUNT

    @classmethod
    def SMALLEST_CURRENT_RATE(cls):
        return cls.__SMALLEST_CURRENT_RATE

    @classmethod
    def MAX_CURRENT_RATE(cls):
        return cls.__MAX_CURRENT_RATE

    @classmethod
    def MIN_WITHDRAW_AMOUNT(cls):
        return cls.__MIN_WITHDRAW_AMOUNT

    @classmethod
    def MONEY_WITHDRAW_CHARGEFEE(cls):
        return cls.__MONEY_WITHDRAW_CHARGEFEE