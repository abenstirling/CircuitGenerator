#ifndef ESP32_HAL_LOG_H_
#define ESP32_HAL_LOG_H_

#ifdef __cplusplus
extern "C" {
#endif

void esp_log_write(uint32_t level, const char* tag, const char* format, ...);

#ifdef __cplusplus
}
#endif

#endif  // ESP32_HAL_LOG_H_
