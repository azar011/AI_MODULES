from sqlalchemy import Table, Column, Integer, String, Float, Date, MetaData

metadata = MetaData()

department_wise_report = Table(
    "department_wise_report",
    metadata,

    Column("id", Integer, primary_key=True),
    Column("report_date", Date),
    Column("department_name", String(255)),

    Column("no_of_checklists", Integer),
    Column("no_of_spots", Integer),

    Column("no_of_targets", Integer),
    Column("no_of_submission", Integer),

    Column("completion_percentage", Float),

    Column("no_of_lapsed", Integer),
    Column("lapsed_percentage", Float)
)