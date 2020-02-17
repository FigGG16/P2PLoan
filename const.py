# Python的常量相对其他语言，可能略显麻烦。
# 不仅仅只是单靠const就可以完成常量定义的。在Python中定义常量需要用对象的方法来创建。
# 我们需要在Lib的目录下创建一个const.py的文件。
class _const(object):
    class ConstError(PermissionError):pass
    def __setattr__(self, name, value):
        if name in self.__dict__.keys():
            raise self.ConstError("Can't rebind const(%s)" % name)
        self.__dict__[name]=value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise  self.ConstError("Can't unbind const(%s)" % name)
        raise  NameError(name)


XXX =_const()

XXX.value=100


# import sys
# sys.modules[__name__]=_const()






