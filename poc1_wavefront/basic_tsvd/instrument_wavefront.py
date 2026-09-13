from wavefront_sdk.common.metrics.registry import WavefrontSdkMetricsRegistry # Import the actual class we want to instrument
from basic_tsvd import runtime

_original_get_or_add = WavefrontSdkMetricsRegistry._get_or_add # Saving a reference of the actual method
_original_report = WavefrontSdkMetricsRegistry._report

def _proxy_get_or_add(self, name, metric): # Proxy for write
    runtime.on_call(id(self.metrics), "registry.py:_get_or_add (write self.metrics[name])", "WRITE")
    return _original_get_or_add(self, name, metric)

def _proxy_report(self, timeout_secs=None): # Proxy for read
    runtime.on_call(id(self.metrics), "registry.py:_report (iterate self.metrics)", "READ")
    return _original_report(self, timeout_secs)

def install(): # This method swaps the original methods with the proxy methods to instrument the WavefrontSdkMetricsRegistry class
    WavefrontSdkMetricsRegistry._get_or_add = _proxy_get_or_add
    WavefrontSdkMetricsRegistry._report = _proxy_report
    print("Instrumentation installed on WavefrontSdkMetricsRegistry (_get_or_add, _report)")
