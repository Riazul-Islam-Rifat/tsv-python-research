import threading
import time

DELAY_SECONDS = 0.05 # The delay window
_traps_lock = threading.Lock() # making _traps thread-safe
_traps = {} # To sotre the object id & traps
_reported_pairs = set() # To store the reported pairs

class Trap:
    def __init__(self, thread_id, obj_id, loc, op):
        self.thread_id = thread_id
        self.obj_id = obj_id
        self.loc = loc
        self.op = op 

def on_call(obj_id, loc, op): # This methiod runs before actual read/write operation

    thread_id = threading.get_ident() # current thread
    trap = Trap(thread_id, obj_id, loc, op)
    with _traps_lock:
        existing = _traps.get(obj_id, [])
        for other in existing:
            if other.thread_id != thread_id and (other.op == "WRITE" or op == "WRITE"):
                pair = tuple(sorted([loc, other.loc]))
                if pair not in _reported_pairs:
                    _reported_pairs.add(pair)
                    print(f"CONFLICTING-PAIR DETECTED:\n"
                          f"    {other.loc}  ({other.op}, thread {other.thread_id})\n"
                          f"    {loc}  ({op}, thread {thread_id})\n"
                          f"    -> same object id={obj_id}, no lock, concurrent access\n")
        _traps.setdefault(obj_id, []).append(trap)
    time.sleep(DELAY_SECONDS)
    with _traps_lock:
        _traps[obj_id].remove(trap)