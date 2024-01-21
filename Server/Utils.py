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
def gcd(a, b):
    # Get the gcd of a and b
    if b == 0:
        return a
    
    return gcd(b, a % b)

@memoize_for_time(None)
def get_relprimes(n):
    # Return a list of numbers p=2...n-1 which are relative prime to n
    return [p for p in range(2, n) if gcd(p, n) == 1]

def get_relprime(n):
    # Return a number p < n which is relative prime to n
    return secrets.choice(get_relprimes(n))