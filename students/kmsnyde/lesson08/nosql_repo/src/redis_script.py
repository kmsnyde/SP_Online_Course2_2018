"""
    demonstrate use of Redis
"""


import login_database
import utilities


def run_example():
    """
        uses non-presistent Redis only (as a cache)

    """

    log = utilities.configure_logger('default', '../logs/redis_script.log')

    try:
        log.info('Step 1: connect to Redis')
        r = login_database.login_redis_cloud()
        log.info('Step 2: cache some data in Redis')
        r.set('andy', 'andy@somewhere.com')

        log.info('Step 3: now I can read it')
        email = r.get('andy')
        log.info('But I must know the key')
        log.info(f'The results of r.get: {email}')

        log.info('Step 4: cache more data in Redis')
        r.set('pam', 'pam@anywhere.com')
        r.set('fred', 'fred@fearless.com')

        log.info('Step : delete from cache')
        r.delete('andy')
        log.info(f'r.delete means andy is now: {email}')

        log.info('Step 6: Redis can maintain a unique ID or count very efficiently')
        r.set('user_count', 21)
        r.incr('user_count')
        r.incr('user_count')
        r.decr('user_count')
        result = r.get('user_count')
        log.info('I could use this to generate unique ids')
        log.info(f'Redis says 21+1+1-1={result}')

        log.info('Step 7: richer data for a SKU')
        r.rpush('186675', 'chair')
        r.rpush('186675', 'red')
        r.rpush('186675', 'leather')
        r.rpush('186675', '5.99')

        log.info('Step 8: pull some data from the structure')
        cover_type = r.lindex('186675', 2)
        log.info(f'Type of cover = {cover_type}')
        
        log.info('Trying new stuff for the course')
        r.hmset('Karl', {'Telephone': '444-333-1234', 'Zip': '90120'})
        r.hmset('Mike', {'Telephone': '123-456-7890', 'Zip': '12345'})
        r.hmset('Sherri', {'Telephone': '888-777-6666', 'Zip': '42157'})
        r.hmset('Zulu', {'Telephone': '999-111-5555', 'Zip': '84591'})
        r.hmset('Abbi', {'Telephone': '978-765-5432', 'Zip': '21478'})
        r.hmset('Larry', {'Telephone': '789-345-5678', 'Zip': '62143'})
        Karl_phone = r.hmget('Karl', 'Telephone')
        Abbi_zip = r.hmget('Abbi', 'Zip')
        Sherri_phone = r.hmget('Sherri', 'Telephone')
        log.info(f'Karl\'s Telephone number is : {Karl_phone}')
        log.info(f'Abbi\'s Zip is: {Abbi_zip}')
        log.info(f'Larry\'s phone is :{r.hmget("Larry", "Telephone")}, while Zulu\'s zip is {r.hmget("Zulu", "Zip")}')
        

    except Exception as e:
        print(f'Redis error: {e}')

