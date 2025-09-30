from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import psutil
import time

app = FastAPI(title="DevOps Dashboard API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus metrics
cpu_usage = Gauge("cpu_usage_percent", "CPU Usage Percentage")
memory_usage = Gauge("memory_usage_percent", "Memory Usage Percentage")
memory_total = Gauge("memory_total_bytes", "Total Memory in Bytes")
memory_used = Gauge("memory_used_bytes", "Used Memory in Bytes")

@app.get("/")
def read_root():
    return {"message": "DevOps Dashboard API", "status": "healthy", "version": "1.0.0"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/system/metrics")
def get_system_metrics():
    """Get system metrics for frontend dashboard"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    
    return {
        "cpu_percent": cpu,
        "memory_total": memory.total,
        "memory_used": memory.used,
        "memory_percent": memory.percent,
        "disk_total": disk.total,
        "disk_used": disk.used,
        "disk_percent": (disk.used / disk.total) * 100,
        "timestamp": time.time()
    }

@app.get("/metrics")
def prometheus_metrics():
    """Prometheus metrics endpoint"""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    
    # Update metrics
    cpu_usage.set(cpu)
    memory_usage.set(memory.percent)
    memory_total.set(memory.total)
    memory_used.set(memory.used)
    
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
