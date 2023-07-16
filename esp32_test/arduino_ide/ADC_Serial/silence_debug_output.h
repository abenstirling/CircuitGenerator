#ifndef SilenceDebugOutput_h
#define SilenceDebugOutput_h

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

#undef esp_log_write
inline void esp_log_write(uint32_t, const char*, const char*, ...) {}


#ifdef __cplusplus
}
#endif

#endif // SilenceDebugOutput_h
