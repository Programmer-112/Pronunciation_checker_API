## Load Testing Results (k6)

### Baseline

**Test configuration:**  
- Duration: 1 minute  
- Virtual Users (VUs): 2–40  
- Endpoints tested: `/score-audio/`, `/health`  
- File uploaded: `iloveyou.wav`  
- Scenarios:
  - `health_check`: 5 VUs looping for 1m, graceful stop 30s  
  - `normal_traffic`: 10 VUs looping for 1m, graceful stop 30s  
  - `spike_test`: Up to 20 VUs over 3 stages for 30s, graceful stop 30s  
  - `stress_test`: 5 VUs looping for 1m, graceful stop 30s  

### Checks
| Metric | Result |
|--------|--------|
| Total checks | 185 |
| Successful checks | 100% (185/185) |
| Failed checks | 0% (0/185) |

### HTTP Requests
| Metric | Value |
|--------|-------|
| Total requests | 185 |
| Requests/sec | 2.77 req/s |
| Average request duration | 9.38 s |
| Median request duration | 7.42 s |
| Min / Max request duration | 0.72 s / 26.1 s |
| 90th percentile | 17.14 s |
| 95th percentile | 21.09 s |
| Failed requests | 0% |

### Iterations
| Metric | Value |
|--------|-------|
| Total iterations | 185 |
| Iterations/sec | 2.77 |
| Average iteration duration | 10.15 s |
| Median iteration duration | 7.54 s |
| Min / Max iteration duration | 1.72 s / 27.1 s |
| 90th percentile | 18.15 s |
| 95th percentile | 22.09 s |

### Virtual Users (VUs)
| Metric | Value |
|--------|-------|
| Min VUs | 2 |
| Max VUs | 40 |

### Network
| Metric | Value |
|--------|-------|
| Data sent | 12 MB |
| Data received | 38 kB |

### Observations
- All checks passed successfully.  
- `/score-audio/` requests are CPU-bound, resulting in high request durations.  
- The server handled up to 40 concurrent VUs with stable success rates.  
- Median latency (~7.4s) indicates most requests complete reasonably, while outliers reach ~26s.

## With Asynchronous Audio Processing

**Test configuration:**  
- Duration: 1m30s max (including graceful stop)  
- Virtual Users (VUs): 1–40  
- Scenarios:
  - `health_check`: 5 VUs looping for 1m, graceful stop 30s  
  - `normal_traffic`: 10 VUs looping for 1m, graceful stop 30s  
  - `spike_test`: Up to 20 VUs over 3 stages for 30s, graceful stop 30s  
  - `stress_test`: 5 VUs looping for 1m, graceful stop 30s  

### Checks
| Metric | Result |
|--------|--------|
| Total checks | 1697 |
| Successful checks | 100% (1697/1697) |
| Failed checks | 0% (0/1697) |

### HTTP Requests
| Metric | Value |
|--------|-------|
| Total requests | 1697 |
| Requests/sec | 27.8 req/s |
| Average request duration | 361.22 ms |
| Median request duration | 428.96 ms |
| Min / Max request duration | 0 ms / 688.52 ms |
| 90th percentile | 468.56 ms |
| 95th percentile | 484.86 ms |
| Failed requests | 0% |

### Iterations
| Metric | Value |
|--------|-------|
| Total iterations | 1697 |
| Iterations/sec | 27.8 |
| Average iteration duration | 955.44 ms |
| Median iteration duration | 1 s |
| Min / Max iteration duration | 342.64 ms / 1.68 s |
| 90th percentile | 1.45 s |
| 95th percentile | 1.47 s |

### Virtual Users (VUs)
| Metric | Value |
|--------|-------|
| Min VUs | 1 |
| Max VUs | 40 |

### Network
| Metric | Value |
|--------|-------|
| Data sent | 108 MB |
| Data received | 345 kB |

### Observations
- All checks passed successfully.  
- Average request duration (~361 ms) indicates **much faster response** than previous CPU-bound audio scoring test.  
- The system handled up to 40 concurrent VUs with stable success rates.  
- Spike scenario executed as expected; no request failures observed.  
- Network usage is dominated by audio uploads (108 MB sent).
