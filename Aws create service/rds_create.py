import boto3


def create_rds(dbname, mast_uname, mast_pass, dbinstance_type, engine_type, storage_alloc, retention_period,
               eng_version):
    rds = boto3.client('rds', region_name='ap-south-1')
    response = rds.create_db_instance(
        DBInstanceIdentifier=dbname,
        MasterUsername=mast_uname,
        MasterUserPassword=mast_pass,
        DBInstanceClass=dbinstance_type,
        Engine=engine_type,
        AllocatedStorage=storage_alloc,
        BackupRetentionPeriod=retention_period,
        EngineVersion=eng_version,
        DeletionProtection=True
    )


create_rds("Sample", "root", '12345678', 'db.t2.micro', 'postgres', 5, 30, '10.6')
