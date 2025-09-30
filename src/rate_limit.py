from __future__ import annotations
import os, random, time
from datetime import datetime

def _now_hour_bucket(): return datetime.utcnow().strftime("%Y-%m-%dT%H")
def _now_day_bucket():  return datetime.utcnow().strftime("%Y-%m-%d")

def in_quiet_hours() -> bool:
    start = int(os.getenv("QUIET_HOURS_START", "21"))
    end   = int(os.getenv("QUIET_HOURS_END", "9"))
    hour = int(datetime.utcnow().strftime("%H"))
    return (hour >= start) or (hour < end)

def natural_delay():
    lo = int(os.getenv("MIN_DELAY_SECONDS", "40"))
    hi = int(os.getenv("MAX_DELAY_SECONDS", "120"))
    time.sleep(random.randint(min(lo,hi), max(lo,hi)))

class SendBudget:
    def __init__(self):
        self.per_hour = int(os.getenv("MAX_SEND_PER_HOUR", "15"))
        self.per_day  = int(os.getenv("MAX_SEND_PER_DAY", "50"))
        self._h_b = _now_hour_bucket(); self._h_c = 0
        self._d_b = _now_day_bucket();  self._d_c = 0
    def _roll(self):
        if _now_hour_bucket() != self._h_b: self._h_b, self._h_c = _now_hour_bucket(), 0
        if _now_day_bucket()  != self._d_b: self._d_b, self._d_c = _now_day_bucket(), 0
    def allow(self) -> bool:
        self._roll()
        return (self._h_c < self.per_hour) and (self._d_c < self.per_day)
    def mark(self):
        self._h_c += 1; self._d_c += 1
