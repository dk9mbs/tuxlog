from model.model import LogDxccPrefixes

class DxCallInfo:

    def __init__(self):
        pass

    @classmethod
    def get_dxinfo_by_call(cls, call):
        prefix=DxCallInfo.get_prefix_by_call(call)
        if prefix!=None:
            return prefix

        for x in range(len(call)):
            part=call[:x*-1]
            print(part)
            prefix=DxCallInfo.get_prefix_by_call(part)
            if prefix!=None:
                return prefix

        return None

    @classmethod
    def get_prefix_by_call(cls, call):
        pref=LogDxccPrefixes().get_or_none(LogDxccPrefixes.id==call)
        return pref
