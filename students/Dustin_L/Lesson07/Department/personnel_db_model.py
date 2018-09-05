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
    dept_name = pw.CharField(primary_key=True, max_length=30)

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
    PERSON_NAME = 0
    LIVES_IN_TOWN = 1
    NICKNAME = 2
    people = [('Andrew', 'Sumner', 'Andy'),
              ('Peter', 'Seattle', None),
              ('Susan', 'Boston', 'Beannie'),
              ('Pam', 'Coventry', 'PJ'),
              ('Steven', 'Colchester', None),
              ]

    DEPT_NAME = 0
    DEPT_MGR = 1
    DEPT_NUM = 2
    departments = [('R&D', 'Bertie', 'R100'),
                   ('Accounting', 'Beth', 'A100'),
                   ('Marketing', 'Marge', 'M100'),
                   ('HR', 'Lucy', 'H100')]

    JOB_NAME = 0
    START_DATE = 1
    END_DATE = 2
    DURATION = 3
    SALARY = 4
    PERSON_EMPLOYED = 5
    DEPARTMENT = 6
    jobs = [('Analyst', '2001-09-22', '2003-01-30', 495, 65500, 'Andrew', 'HR'),
            ('Senior analyst', '2003-02-01', '2006-10-22', 1359, 70000, 'Andrew', 'Accounting'),
            ('Senior business analyst', '2006-10-23', '2016-12-24', 3715, 80000, 'Andrew', 'Marketing'),
            ('Admin supervisor', '2012-10-01', '2014-11-10', 770, 45900, 'Peter', 'R&D'),
            ('Admin manager', '2014-11-14', '2018-01-05', 1148, 45900, 'Peter', 'Marketing')
            ]

    logger.info("Creating database datatables")
    with database as db:
        db.execute_sql('PRAGMA foreign_keys = ON;')
        db.create_tables([Department,
                          Job,
                          Person,
                          PersonNumKey])

        logger.info("Adding people to database")
        for person in people:
            Person.create(person_name=person[PERSON_NAME],
                          lives_in_town=person[LIVES_IN_TOWN],
                          nickname=person[NICKNAME])

        logger.info("Adding jobs to database")
        for job in jobs:
            Job.create(job_name=job[JOB_NAME],
                       start_date=job[START_DATE],
                       end_date=job[END_DATE],
                       duration_days=job[DURATION],
                       salary=job[SALARY],
                       person_employed=job[PERSON_EMPLOYED],
                       job_dept=job[DEPARTMENT])

        logger.info("Add departments to database")
        for dept in departments:
            Department.create(dept_name=dept[DEPT_NAME],
                              dept_mgr=dept[DEPT_MGR],
                              dept_num=dept[DEPT_NUM])
