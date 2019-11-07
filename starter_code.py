import mock_db
import uuid
import time
from worker import worker_main
from threading import Thread, Lock
def lock_is_free():
    """
        CHANGE ME, POSSIBLY MY ARGS

        Return whether the lock is free
    """
    return db.find_one({"_id":  "Lock"}) is None
    
def lock_acquire(worker_hash):
    """
       require the lock
    """
    try:
        db.insert_one({"_id":  "Lock", "worker_hash": worker_hash})
        return True
    except Exception:
        return False
        
def lock_release():
    """
       release the lock
    """
    db.delete_one({"_id": "Lock"})
    

def attempt_run_worker(worker_hash, give_up_after, db, retry_interval):
    """
        CHANGE MY IMPLEMENTATION, BUT NOT FUNCTION SIGNATURE

        Run the worker from worker.py by calling worker_main

        Args:
            worker_hash: a random string we will use as an id for the running worker
            give_up_after: if the worker has not run after this many seconds, give up
            db: an instance of MockDB
            retry_interval: continually poll the locking system after this many seconds
                            until the lock is free, unless we have been trying for more
                            than give_up_after seconds
    """
    count= 0
    times= give_up_after/ retry_interval
    while count<= times:
        while not lock_is_free():
            time.sleep(retry_interval)
            count= count+ 1
            if count> times:
                break
        if lock_acquire(worker_hash):
            try:
                worker_main(worker_hash, db)
            except:
                print('Crashed')
            finally:
                lock_release()
            break
        else:
            count= count+ 1
            time.sleep(retry_interval)
    
if __name__ == "__main__":
    """
        DO NOT MODIFY

        Main function that runs the worker five times, each on a new thread
        We have provided hard-coded values for how often the worker should retry
        grabbing lock and when it should give up. Use these as you see fit, but
        you should not need to change them
    """

    db = mock_db.DB()
    threads = []
    for _ in range(25):
        t = Thread(target=attempt_run_worker, args=(uuid.uuid1(), 2000, db, 0.1))
        threads.append(t)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
