#include "HDTimer.h"

// Initialize the resolution of the timer
LARGE_INTEGER Timer::m_freq = \
           (QueryPerformanceFrequency(&Timer::m_freq), Timer::m_freq);
  
 // Calculate the overhead of the timer
LONGLONG Timer::m_overhead = Timer::GetOverhead();