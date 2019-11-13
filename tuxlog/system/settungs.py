from model.model import LogSettings

class Setting():

    @staticmethod
    def get_setting_value(logbook_id, setting_name, default_value):
        setting=LogSettings.get_or_none((LogSettings.logbook_id==logbook_id) & (LogSettings.name==setting_name))
        if setting==None:
            setting=LogSettings.get_or_none((LogSettings.logbook_id=='*') & (LogSettings.name==setting_name))
            if setting==None:
                return default_value
            else:
                return setting.value
        else:
            return setting.value
