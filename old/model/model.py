 
from peewee import *
from playhouse.signals import Model as PModel
from playhouse.signals import post_save

database = DatabaseProxy()

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(PModel):
    class Meta:
        database = database

class LogBands(BaseModel):
    adif_name = CharField()
    frequency_max = DecimalField()
    frequency_min = DecimalField()
    frequency_unit = CharField(constraints=[SQL("DEFAULT 'MHz'")])
    name = CharField()

    class Meta:
        table_name = 'log_bands'

class LogDxcc(BaseModel):
    continent = CharField()
    country = CharField()
    cq_zone = IntegerField()
    entity = IntegerField()
    id = CharField(primary_key=True)
    itu_zone = IntegerField()
    latitude = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    longitude = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    time_offset = IntegerField()

    class Meta:
        table_name = 'log_dxcc'

class LogDxccPrefixes(BaseModel):
    cq_zone = IntegerField()
    dxcc = ForeignKeyField(column_name='dxcc_id', field='id', model=LogDxcc)
    entity = IntegerField()
    exact_match = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = CharField(primary_key=True)
    itu_zone = IntegerField()
    time_offset = IntegerField()

    class Meta:
        table_name = 'log_dxcc_prefixes'

class LogDxclusterSpots(BaseModel):
    band = ForeignKeyField(column_name='band_id', field='id', model=LogBands, null=True)
    callsign = CharField()
    callsign_dxcc_prefix = ForeignKeyField(column_name='callsign_dxcc_prefix_id', field='id', model=LogDxccPrefixes, null=True)
    comment = TextField(null=True)
    date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    frequency = DecimalField()
    new_dxcc = IntegerField(constraints=[SQL("DEFAULT 0")])
    new_locator = IntegerField(constraints=[SQL("DEFAULT 0")])
    spot = CharField(null=True)
    spotter = CharField()
    spotter_dxcc_prefix = ForeignKeyField(backref='log_dxcc_prefixes_spotter_dxcc_prefix_set', column_name='spotter_dxcc_prefix_id', field='id', model=LogDxccPrefixes, null=True)
    time_utc = CharField(null=True)

    class Meta:
        table_name = 'log_dxcluster_spots'

class LogDxclusters(BaseModel):
    host = CharField()
    password = CharField(null=True)
    port = IntegerField()
    position = IntegerField(constraints=[SQL("DEFAULT 100")])
    prompt_password = CharField(null=True)
    prompt_username = CharField()
    username = CharField()

    class Meta:
        table_name = 'log_dxclusters'

class LogImportjobStatus(BaseModel):
    description = CharField()

    class Meta:
        table_name = 'log_importjob_status'

class LogImportjobs(BaseModel):
    end_date = DateTimeField(null=True)
    import_fail = IntegerField(constraints=[SQL("DEFAULT 0")])
    import_success = IntegerField(constraints=[SQL("DEFAULT 0")])
    job_name = CharField()
    message = CharField(null=True)
    start_date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    status = ForeignKeyField(column_name='status_id', constraints=[SQL("DEFAULT 0")], field='id', model=LogImportjobStatus)

    class Meta:
        table_name = 'log_importjobs'

class LogImportjobLines(BaseModel):
    external_record = TextField(null=True)
    job = ForeignKeyField(column_name='job_id', field='id', model=LogImportjobs)
    message = TextField(null=True)
    status = ForeignKeyField(column_name='status_id', constraints=[SQL("DEFAULT 0")], field='id', model=LogImportjobStatus)

    class Meta:
        table_name = 'log_importjob_lines'

class LogLogbooks(BaseModel):
    deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    description = CharField()
    id = CharField(primary_key=True)
    mycall = CharField()
    parent_id = CharField(null=True)

    class Meta:
        table_name = 'log_logbooks'

class LogModes(BaseModel):
    description = CharField()
    id = CharField(primary_key=True)
    parent = CharField(null=True)

    class Meta:
        table_name = 'log_modes'

class LogRigs(BaseModel):
    description = CharField()
    hamlib_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = CharField(primary_key=True)
    remote_host = CharField(constraints=[SQL("DEFAULT '127.0.0.1'")])
    remote_port = IntegerField(constraints=[SQL("DEFAULT 4532")])

    class Meta:
        table_name = 'log_rigs'

class LogQslshipmentmodes(BaseModel):
    description = CharField()
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'log_qslshipmentmodes'

class LogLogs(BaseModel):
    band = ForeignKeyField(column_name='band_id', field='id', model=LogBands, null=True)
    comment = TextField(null=True)
    country = CharField(null=True)
    cq = CharField(null=True)
    distance = IntegerField(null=True)
    dok = CharField(null=True)
    dxcc = CharField(null=True)
    email = CharField(null=True)
    end_utc = TimeField(null=True)
    entity = IntegerField(null=True)
    frequency = DecimalField(null=True)
    itu = CharField(null=True)
    itu_prefix = CharField(null=True)
    locator = CharField(null=True)
    logbook = ForeignKeyField(column_name='logbook_id', field='id', model=LogLogbooks)
    logdate_utc = DateField(null=True)
    lognr = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    mode = ForeignKeyField(column_name='mode_id', field='id', model=LogModes)
    mytestnr = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    name = CharField(null=True)
    power = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    qsl_shipmentmode = ForeignKeyField(column_name='qsl_shipmentmode', field='id', model=LogQslshipmentmodes, null=True)
    qslrecv = IntegerField(constraints=[SQL("DEFAULT 0")])
    qslsend = IntegerField(constraints=[SQL("DEFAULT 0")])
    qth = CharField(null=True)
    rig = ForeignKeyField(column_name='rig_id', field='id', model=LogRigs, null=True)
    rxexchange1 = CharField(null=True)
    rxexchange2 = CharField(null=True)
    rxrst = IntegerField(null=True)
    source = CharField(null=True)
    start_utc = TimeField(null=True)
    txexchange1 = CharField(null=True)
    txexchange2 = CharField(null=True)
    txrst = IntegerField(null=True)
    viacall = CharField(null=True)
    web = CharField(null=True)
    yourcall = CharField()
    yourtestnr = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'log_logs'

class LogImportlogs(BaseModel):
    external_record = TextField(null=True)
    import_message = TextField(null=True)
    internal_record = TextField(null=True)
    log = ForeignKeyField(column_name='log_id', field='id', model=LogLogs, null=True)
    statuscode = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'log_importlogs'

class LogItuprefixe(BaseModel):
    description = CharField()
    itu_prefix = CharField(primary_key=True)

    class Meta:
        table_name = 'log_ituprefixe'

class LogRowids(BaseModel):
    lastrowid = IntegerField(constraints=[SQL("DEFAULT 0")])
    tablename = CharField(primary_key=True)

    class Meta:
        table_name = 'log_rowids'

class LogSettings(BaseModel):
    logbook = ForeignKeyField(column_name='logbook_id', field='id', model=LogLogbooks)
    name = CharField()
    value = CharField(null=True)

    class Meta:
        table_name = 'log_settings'
        indexes = (
            (('logbook', 'name'), True),
        )
        primary_key = CompositeKey('logbook', 'name')

class LogTmpAdifExport(BaseModel):
    idx = IntegerField(null=True)
    log_id = IntegerField(null=True)
    tag = CharField(null=True)
    value = TextField(null=True)

    class Meta:
        table_name = 'log_tmp_adif_export'

class LogTmpDebug(BaseModel):
    dbgmsg = TextField(null=True)
    src = CharField(null=True)

    class Meta:
        table_name = 'log_tmp_debug'

class LogVwDxclusterSpots(BaseModel):
    age_minutes = BigIntegerField(null=True)
    band = CharField()
    comment = TextField(null=True)
    continent = CharField()
    country = CharField()
    dx = CharField()
    dx_continent = CharField()
    dx_country = CharField()
    dx_dxcc = CharField()
    dxcc = CharField()
    frequency = DecimalField()
    new_dxcc = IntegerField(constraints=[SQL("DEFAULT 0")])
    new_locator = IntegerField(constraints=[SQL("DEFAULT 0")])
    spotter = CharField()
    time_utc = CharField(null=True)

    class Meta:
        table_name = 'log_vw_dxcluster_spots'
        primary_key = False

class MetaClasstypes(BaseModel):
    description = CharField()
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'meta_classtypes'

class MetaAutostart(BaseModel):
    classtype = ForeignKeyField(column_name='classtype_id', field='id', model=MetaClasstypes)
    description = CharField()
    enabled = IntegerField(constraints=[SQL("DEFAULT 1")])
    object_id = CharField(null=True)
    profile = CharField(constraints=[SQL("DEFAULT '*'")])

    class Meta:
        table_name = 'meta_autostart'

class MetaBackgroundtasks(BaseModel):
    classname = CharField()
    description = CharField()
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'meta_backgroundtasks'

class MetaDataExchangeConverters(BaseModel):
    classname_in = CharField(null=True)
    classname_out = CharField(null=True)
    description = CharField()
    enabled = IntegerField(constraints=[SQL("DEFAULT 1")])
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'meta_data_exchange_converters'

class MetaDataExchangeFields(BaseModel):
    converter = ForeignKeyField(column_name='converter_id', field='id', model=MetaDataExchangeConverters)
    external_fieldname = CharField()
    external_idx = IntegerField(constraints=[SQL("DEFAULT 100")])
    internal_datatype = CharField()
    internal_fieldname = CharField()
    internal_idx = IntegerField(constraints=[SQL("DEFAULT 100")])

    class Meta:
        table_name = 'meta_data_exchange_fields'
        indexes = (
            (('converter', 'external_fieldname', 'internal_fieldname', 'internal_datatype'), True),
        )
        primary_key = CompositeKey('converter', 'external_fieldname', 'internal_datatype', 'internal_fieldname')

class MetaDatabaseFieldtypes(BaseModel):
    internal_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    type_name = CharField(primary_key=True)

    class Meta:
        table_name = 'meta_database_fieldtypes'

class MetaDataforms(BaseModel):
    datacomponent = CharField()
    form_name = CharField()
    model_name = CharField()

    class Meta:
        table_name = 'meta_dataforms'
        indexes = (
            (('model_name', 'form_name'), True),
        )

class MetaDatasources(BaseModel):
    bound_column = IntegerField(constraints=[SQL("DEFAULT 0")])
    empty_item = IntegerField(constraints=[SQL("DEFAULT 0")])
    empty_item_text = CharField(constraints=[SQL("DEFAULT '-- Select item! --'")], null=True)
    id = CharField(primary_key=True)
    orderby_clause = TextField(null=True)
    select_clause = TextField(null=True)
    where_clause = TextField(null=True)

    class Meta:
        table_name = 'meta_datasources'

class MetaDataviews(BaseModel):
    fields = TextField(null=True)
    filter_clause = TextField(null=True)
    id_field_name = CharField(constraints=[SQL("DEFAULT 'id'")])
    model_name = CharField()
    open_path = TextField(null=True)
    order_by = TextField(null=True)
    page_size = IntegerField(constraints=[SQL("DEFAULT 5000")])
    view_name = CharField()
    where_clause = TextField(null=True)

    class Meta:
        table_name = 'meta_dataviews'
        indexes = (
            (('model_name', 'view_name'), True),
        )

class MetaForms(BaseModel):
    classname = CharField()
    description = CharField()
    id = CharField(primary_key=True)

    class Meta:
        table_name = 'meta_forms'

class MetaSubforms(BaseModel):
    classname = CharField()
    description = CharField()
    form = ForeignKeyField(column_name='form_id', field='id', model=MetaForms)
    id = CharField(primary_key=True)
    parent_container_name = CharField()
    position = IntegerField(constraints=[SQL("DEFAULT 0")])
    topic = CharField()

    class Meta:
        table_name = 'meta_subforms'

class MetaSubformComponents(BaseModel):
    component_classname = CharField()
    component_name = CharField()
    component_value = CharField(null=True)
    database_field = CharField(null=True)
    database_fieldtype = ForeignKeyField(column_name='database_fieldtype', field='type_name', model=MetaDatabaseFieldtypes, null=True)
    gridheight = IntegerField(constraints=[SQL("DEFAULT 0")])
    gridwidth = IntegerField(constraints=[SQL("DEFAULT 0")])
    gridx = IntegerField(constraints=[SQL("DEFAULT 0")])
    gridy = IntegerField(constraints=[SQL("DEFAULT 0")])
    insets_bottom = IntegerField(constraints=[SQL("DEFAULT 0")])
    insets_left = IntegerField(constraints=[SQL("DEFAULT 0")])
    insets_right = IntegerField(constraints=[SQL("DEFAULT 0")])
    insets_top = IntegerField(constraints=[SQL("DEFAULT 0")])
    subform = ForeignKeyField(column_name='subform_id', field='id', model=MetaSubforms)
    weightx = IntegerField(constraints=[SQL("DEFAULT 0")])
    weighty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'meta_subform_components'
        indexes = (
            (('subform', 'component_name'), True),
        )
        primary_key = CompositeKey('component_name', 'subform')

class MetaSysDbversion(BaseModel):
    description = CharField(null=True)
    version = CharField(primary_key=True)

    class Meta:
        table_name = 'meta_sys_dbversion'

class MetaUrlclassloaders(BaseModel):
    classname = CharField(primary_key=True)
    classpath = CharField()

    class Meta:
        table_name = 'meta_urlclassloaders'


