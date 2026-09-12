import sys, threading, logging, time
sys.path.insert(0, ".") # ensures the path location

logging.disable(logging.CRITICAL) # disable logging in the output terminal

from wavefront_sdk.common.metrics.registry import WavefrontSdkMetricsRegistry # import the actual buggy class

# In real cases, this is used with a real sender that sends metrics to Wavefront. 

class SlowMockSender: # represents a slow sender that takes 0.3ms to send a metric or delta counter
    def send_metric(self, *a, **k): 
        time.sleep(0.0003)

    def send_delta_counter(self, *a, **k): 
        time.sleep(0.0003)

registry = WavefrontSdkMetricsRegistry(wf_metric_sender=SlowMockSender()) # Shared registry onject for the test

def add_metrics(n): # Thread1 adds new counters --> that's a write operation
    for i in range(n):
        registry.new_counter(f"metric_{i}")
        time.sleep(0.001)

def report(n): # Thread2 reports metrics --> that's a read operation
    for _ in range(n):
        registry._report()

if __name__ == "__main__":
    t1 = threading.Thread(target=add_metrics, args=(300,))
    t2 = threading.Thread(target=report, args=(15,))
    t1.start(); t2.start()
    t1.join(); t2.join()
  
