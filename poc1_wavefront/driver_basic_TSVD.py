import sys, threading, logging
sys.path.insert(0, ".")
logging.disable(logging.CRITICAL) # Keeps the output clean

from basic_tsvd import instrument_wavefront
instrument_wavefront.install() # Here the swapping takes place. --> this is monkey-patching

from wavefront_sdk.common.metrics.registry import WavefrontSdkMetricsRegistry

registry = WavefrontSdkMetricsRegistry(wf_metric_sender=None) # Creating a shared object

def add_metrics(n):
    for i in range(n):
        registry.new_counter(f"metric_{i}")

def report(n):
    for _ in range(n):
        try:
            registry._report()
        except RuntimeError as e:
            print(f"(real crash also occurred: {e})")

if __name__ == "__main__":
    t1 = threading.Thread(target=add_metrics, args=(30,))
    t2 = threading.Thread(target=report, args=(5,))
    t1.start(); t2.start()
    t1.join(); t2.join()
    print("Done.")
