from datetime import datetime
import secrets

def memoize_for_time(td):
    # Build a decorator which takes a timedelta, or None
    # The decorator will only run the function if the last time the function was run is more than timedelta away
    # If td is None, never call function after first run
    def memoize(func):
        nonlocal td
        # Build a version of a function which stores the return value
        # Only rerun func if the last run of the function is more than a day ago
        lastCall = dict()
        ret = dict()
        def memoized(*args):
            nonlocal lastCall
            nonlocal ret
            now = datetime.now()
            if args not in lastCall or (td != None and now - lastCall[args] > td):
                # If td is not none:
                # Only run function if not run before or it was run a while ago
                # If td is none:
                # Only run function if not called before
                print("Calling", func)
                lastCall[args] = now
                ret[args] = func(*args)
            return ret[args]
        return memoized
    return memoize

@memoize_for_time(None)
def get_nonfactors(n):
    # Return a list of nonfactors of an integer n
    return [p for p in range(2, n) if n % p != 0]

def get_nonfactor(n):
    # Return a number p < n so that p does not divide n
    return secrets.choice(get_nonfactors(n))