import threading
import requests

session = requests.Session() # the shared object

def mount_adapters(n):
    for i in range(n):
        session.mount(f"http://host{i}.example.com", requests.adapters.HTTPAdapter()) # Adding key to the session.adapters dictionary & it's a write operation

def get_adapters(n):
    for i in range(n):
        session.get_adapter(f"http://host{i % 50}.example.com/path") # This is a reader operation

if __name__ == "__main__":
    t1 = threading.Thread(target=mount_adapters, args=(2000,))
    t2 = threading.Thread(target=get_adapters, args=(2000,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    # print("Both threads joined.")