from sqlalchemy import create_engine

DB_URL = "mysql+pymysql://root:Root%40123@localhost:3306/escalation_ml_db"

engine = create_engine(DB_URL, pool_pre_ping=True)


