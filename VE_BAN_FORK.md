# lily — firmware RF cho LilyGO T-Embed CC1101 (dựa trên Bruce)

Repo này là **bản phái sinh của [Bruce](https://github.com/pr3y/Bruce)** (firmware ESP32 mã nguồn mở),
dùng làm nền để phát triển bộ công cụ **phân tích và chẩn đoán RF** cho board **LilyGO T-Embed CC1101**
(ESP32-S3 + CC1101 sub-GHz + PN532 NFC + hồng ngoại).

## Giấy phép

Bruce dùng **GNU AGPL-3.0** (xem `LICENSE`). Bản phái sinh này cũng theo AGPL-3.0: mọi thay đổi giữ nguyên
giấy phép và ghi nguồn. Nguồn gốc: https://github.com/pr3y/Bruce

## Khác với Bruce gốc

- Nhập từ Bruce (một lần, theo commit gốc ghi trong lịch sử git). Có thể đồng bộ về sau qua remote `upstream`:
  `git fetch upstream && git merge upstream/main`.
- **Đã bỏ để giảm dung lượng** (không ảnh hưởng build firmware): thư mục `media/` (ảnh README) và `pcbs/`
  (file thiết kế mạch). Cần thì lấy lại từ repo Bruce gốc.

## Phạm vi phát triển (theo yêu cầu người dùng)

Tập trung vào **phân tích và phát lại tín hiệu của chính người dùng** trên thiết bị mình sở hữu:

1. **Dò phổ / tìm tần số** — quét dải, đọc RSSI, waterfall (`rf_spectrum`, `rf_waterfall`, `rf_scan`).
2. **Thu + giải mã** — thu OOK/ASK, FSK; giải mã giao thức; xem dạng sóng; lưu thẻ SD (`rf_listen`, `protocols`).
3. **Ghi / phát lại remote của chính mình** — ví dụ sao lưu remote cổng, chuông cửa của bạn (`record`, `emit`).
4. **Hồng ngoại + NFC** — remote IR của bạn, đọc thẻ NFC của bạn (`ir`, `rfid`).

**Không phát triển trong repo này:** module gây nhiễu (`rf_jammer`) và dò mã cuốn chiếu (`rf_bruteforce`)
của Bruce. Jammer gây nhiễu sóng (bất hợp pháp ở hầu hết các nước); bruteforce dùng để mở khóa thiết bị
không phải của mình.

## Lưu ý pháp lý

CC1101 phát được sóng. Ở Việt Nam, phát trên các dải sub-GHz phải đúng tần số và công suất được phép.
Chỉ thu/phân tích tín hiệu của chính mình, và chỉ phát lại tín hiệu của thiết bị mình sở hữu.

## Build cho T-Embed CC1101

Env PlatformIO: `lilygo-t-embed-cc1101` (trong `platformio.ini`). Xem thêm README của Bruce ở dưới.
