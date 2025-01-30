"""
Provides basic telemetry for Clean Coder via OpenTelemetry.
Enabled by default unless TELEMETRY_DISABLED=1 is set.
Metrics are exported to OTLP endpoint if OTEL_EXPORTER_OTLP_ENDPOINT is set,
otherwise falls back to console output.
"""

import os
from urllib.parse import urlparse

TELEMETRY_ENABLED = (os.getenv("TELEMETRY_DISABLED") != "1")
OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")

_telemetry_initialized = False
_meter = None
_counters = {}

def telemetry_event(event_name: str):
    """
    Single function to (1) lazily initialize OpenTelemetry, and
    (2) record a usage event with the given event_name.
    """
    global _telemetry_initialized, _meter, _counters
    if not TELEMETRY_ENABLED:
        return

    if not _telemetry_initialized:
        try:
            from opentelemetry.sdk.metrics import MeterProvider
            from opentelemetry.sdk.resources import Resource
            from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
            from opentelemetry.metrics import get_meter
            from opentelemetry.metrics import set_meter_provider

            # Try to import OTLP exporter first
            try:
                from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
                if OTLP_ENDPOINT:
                    # Parse endpoint to handle different URL formats
                    parsed_url = urlparse(OTLP_ENDPOINT)
                    # Remove http:// or https:// as OTLP gRPC doesn't use these prefixes
                    endpoint = parsed_url.netloc or parsed_url.path
                    
                    exporter = OTLPMetricExporter(
                        endpoint=endpoint,
                        insecure=True  # For local development without TLS
                    )
                else:
                    raise ImportError("OTLP endpoint not configured")
            except (ImportError, Exception) as e:
                print(f"Falling back to console exporter due to: {str(e)}")
                # Fall back to console exporter if OTLP is not available/configured
                from opentelemetry.sdk.metrics.export import ConsoleMetricExporter
                exporter = ConsoleMetricExporter()

            resource = Resource(attributes={
                "service.name": "clean-coder-telemetry",
                "service.version": "1.0.0",  # Update this when version changes
                "deployment.environment": os.getenv("DEPLOYMENT_ENVIRONMENT", "production")
            })
            
            reader = PeriodicExportingMetricReader(
                exporter,
                export_interval_millis=30000
            )
            provider = MeterProvider(resource=resource, metric_readers=[reader])
            
            # Set the global meter provider
            set_meter_provider(provider)
            
            # Get meter from the global provider
            _meter = get_meter("clean_coder_meter")

            _telemetry_initialized = True

        except ImportError as e:
            print(f"Telemetry initialization failed: {str(e)}")
            # If OpenTelemetry is not installed, do nothing.
            return

    if event_name not in _counters and _meter is not None:
        _counters[event_name] = _meter.create_counter(
            f"{event_name}_runs",
            description=f"Number of times {event_name} was executed",
            unit="1"
        )
    if event_name in _counters:
        _counters[event_name].add(1)
