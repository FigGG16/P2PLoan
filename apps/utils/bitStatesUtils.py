# coding=gbk

#约定  GET方法开头：只负责返回数据
      # 完整成员名：负责返回数据，并且用在数据库的状态位

class BitStatesUtils:
    __OP_BIND_PHONE = 1 << 0# 用户绑定手机状态码
    __OP_BIND_EMAIL = 1 <<1# 用户绑定邮箱
    __OP_BASIC_INFO = 1 <<2# 用户是否填写基本资料
    __OP_REAL_AUTH = 1 <<3# 用户是否实名认证
    __OP_VEDIO_AUTH = 1 <<4# 用户是否视频认证
    __OP_HAS_BIDREQUEST_PROCESS = 1 <<5# 用户是否有一个借款正在处理流程当中
    __OP_BIND_BANKINFO = 1 <<6# 用户是否绑定银行卡
    __OP_HAS_MONEYWITHDRAW_PROCESS = 1 <<7 # 用户是否有一个提现申请在处理中

    #后台审核状态信息

    __STATE_NORMAL = 0 # 正常
    __STATE_AUDIT = 1 # 审核通过
    __STATE_REJECT = 2 # 审核拒绝


    @classmethod
    def GET_OP_BIND_PHONE(cls):
        return cls.__OP_BIND_PHONE

    @classmethod
    def GET_OP_BIND_EMAIL(cls):
        return cls.__OP_BIND_EMAIL

    @classmethod
    def GET_OP_BASIC_INFO(cls):
        return cls.__OP_BASIC_INFO

    @classmethod
    def GET_OP_REAL_AUTH(cls):
        return cls.__OP_REAL_AUTH

    @classmethod
    def GET_OP_VEDIO_AUTH(cls):
        return cls.__OP_VEDIO_AUTH

    @classmethod
    def GET_OP_HAS_BIDREQUEST_PROCESS(cls):
        return cls.__OP_HAS_BIDREQUEST_PROCESS

    @classmethod
    def GET_OP_BIND_BANKINFO(cls):
        return cls.__OP_BIND_BANKINFO

    @classmethod
    def GET_HAS_MONEYWITHDRAW_PROCESS(cls):
        return cls.__OP_HAS_MONEYWITHDRAW_PROCESS

    @classmethod
    def STATE_NORMAL(cls):
        return cls.__STATE_NORMAL
    @classmethod
    def STATE_AUDIT(cls):
        return cls.__STATE_AUDIT
    @classmethod
    def STATE_REJECT(cls):
        return cls.__STATE_REJECT

    # / **
    # * @ param
    # states
    # *所有状态值
    # * @ param
    # value
    # *需要判断状态值
    # * @ return 是否存在
    # * /
    @classmethod
    def hasState(cls, states, value):
        return (states & value !=0)

    # / **
    # * @ param
    # states
    # *已有状态值
    # * @ param
    # value
    # *需要添加状态值
    # * @ return 新的状态值
    # * /
    @classmethod
    def addState(cls, states, value):
        if BitStatesUtils.hasState(states, value):
            return states
        return (states | value)

    # / **
    # * @ param
    # states
    # *已有状态值
    # * @ param
    # value
    # *需要删除状态值
    # * @ return 新的状态值
    # * /
    @classmethod
    def removeState(cls, states, value):
        if not BitStatesUtils.removeState(states, value):
            return states
        return states ^ value



