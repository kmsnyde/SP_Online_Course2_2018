#!/usr/bin/env python3
"""
    Simple database examle with Peewee ORM, sqlite and Python
    Here we define the schema
"""
import logging
import peewee as pw

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

database = pw.SqliteDatabase('personnel.db')


class BaseModel(pw.Model):
    """This class defines the base class for all Peewee data tables"""
    class Meta:
        """Meta class required for Peewee"""
        database = database


class Department(BaseModel):
    """
    This class defines Department, which maintains details of the department
    in which a person held a job.
    """
    dept_num_check = 'upper( substr( dept_num, 1, 1 ) BETWEEN "A" AND "Z" )'

    logger.info('The department name')
    dept_name = pw.CharField(max_length=30)

    logger.info('The department manager')
    dept_mgr = pw.CharField(max_length=30)

    logger.info('The department number')
    dept_num = pw.CharField(max_length=4,
                            constraints=[pw.Check(dept_num_check)])


class Person(BaseModel):
    """
    This class defines Person, which maintains details of someone
    for whom we want to research career to date.
    """
    logger.info('Note how we defined the class')
    logger.info('Specify fields in our model, their lengths and if mandatory')
    logger.info('Must be a unique identifier for each person')

    person_name = pw.CharField(primary_key=True, max_length=30)
    lives_in_town = pw.CharField(max_length=40)
    nickname = pw.CharField(max_length=20, null=True)


class PersonNumKey(BaseModel):
    """
    This class defines Person, which maintains details of someone
    for whom we want to research career to date.

    *** I am implemented with a numeric PK that is generated by the system ***
    """
    logger.info('An alternate Person class')
    logger.info("Note: no primary key so we're give one 'for free'")

    person_name = pw.CharField(max_length=30)
    lives_in_town = pw.CharField(max_length=40)
    nickname = pw.CharField(max_length=20, null=True)


class Job(BaseModel):
    """
    This class defines Job, which maintains details of past Jobs
    held by a Person.
    """
    logger.info('Now the Job class with a simlar approach')
    job_name = pw.CharField(primary_key=True, max_length=30)

    logger.info('Job Dates')
    start_date = pw.DateField(formats='YYYY-MM-DD')
    end_date = pw.DateField(formats='YYYY-MM-DD')

    logger.info('Job duration')
    duration_days = pw.IntegerField()

    logger.info('Job Number')
    salary = pw.DecimalField(max_digits=7, decimal_places=2)

    logger.info('Which person had the Job')
    person_employed = pw.ForeignKeyField(Person,
                                         related_name='was_filled_by',
                                         null=False)

    logger.info('Which department this job is in')
    job_dept = pw.ForeignKeyField(Department, backref='jobs')


if __name__ == '__main__':
    logger.info("Creating database datatables")
    with database as db:
        db.execute_sql('PRAGMA foreign_keys = ON;')
        db.create_tables([Department,
                          Job,
                          Person,
                          PersonNumKey])
