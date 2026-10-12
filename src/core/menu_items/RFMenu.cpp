#include "RFMenu.h"
#include "core/display.h"
#include "core/settings.h"
#include "core/utils.h"
#include "modules/rf/record.h"
#include "modules/rf/rf_bruteforce.h"
#include "modules/rf/rf_jammer.h"
#include "modules/rf/rf_listen.h"
#include "modules/rf/rf_scan.h"
#include "modules/rf/rf_send.h"
#include "modules/rf/rf_utils.h"
#include "modules/rf/rf_spectrum.h"
#include "modules/rf/rf_waterfall.h"

void RFMenu::optionsMenu() {
    options = {
        // Rut gon: chi giu luong Quet -> Luu dang song -> Phat lai.
        {"Quét & Lưu",     [=]() { RFScan(); }       },  // quet, giai ma, luu (ca RAW), phat lai ngay
        {"Phát lại file",  sendCustomRF              },  // mo file .sub da luu va phat lai
        {"Cài đặt",        [this]() { configMenu(); }},
    };
    addOptionToMainMenu();

    delay(200);
    String txt = "Sóng vô tuyến";
    if (bruceConfigPins.rfModule == CC1101_SPI_MODULE) txt += " (CC1101)"; // Indicates if CC1101 is connected
    else txt += " Tx: " + String(bruceConfigPins.rfTx) + " Rx: " + String(bruceConfigPins.rfRx);

    loopOptions(options, MENU_TYPE_SUBMENU, txt.c_str());
}

void RFMenu::configMenu() {
    options = {
        {"Chân TX", lambdaHelper(gsetRfTxPin, true)},
        {"Chân RX", lambdaHelper(gsetRfRxPin, true)},
        {"Mô-đun RF", setRFModuleMenu},
        {"Tần số", setRFFreqMenu},
        {"Quay lại", [this]() { optionsMenu(); }},
    };

    loopOptions(options, MENU_TYPE_SUBMENU, "Cài đặt RF");
}

void RFMenu::drawIcon(float scale) {
    clearIconArea();
    int radius = scale * 7;
    int deltaRadius = scale * 10;
    int triangleSize = scale * 30;

    if (triangleSize % 2 != 0) triangleSize++;

    // Body
    tft.fillCircle(iconCenterX, iconCenterY - radius, radius, bruceConfig.priColor);
    tft.fillTriangle(
        iconCenterX,
        iconCenterY,
        iconCenterX - triangleSize / 2,
        iconCenterY + triangleSize,
        iconCenterX + triangleSize / 2,
        iconCenterY + triangleSize,
        bruceConfig.priColor
    );

    // Left Arcs
    tft.drawArc(
        iconCenterX,
        iconCenterY - radius,
        2.5 * radius,
        2 * radius,
        40,
        140,
        bruceConfig.priColor,
        bruceConfig.bgColor
    );
    tft.drawArc(
        iconCenterX,
        iconCenterY - radius,
        2.5 * radius + deltaRadius,
        2 * radius + deltaRadius,
        40,
        140,
        bruceConfig.priColor,
        bruceConfig.bgColor
    );
    tft.drawArc(
        iconCenterX,
        iconCenterY - radius,
        2.5 * radius + 2 * deltaRadius,
        2 * radius + 2 * deltaRadius,
        40,
        140,
        bruceConfig.priColor,
        bruceConfig.bgColor
    );

    // Right Arcs
    tft.drawArc(
        iconCenterX,
        iconCenterY - radius,
        2.5 * radius,
        2 * radius,
        220,
        320,
        bruceConfig.priColor,
        bruceConfig.bgColor
    );
    tft.drawArc(
        iconCenterX,
        iconCenterY - radius,
        2.5 * radius + deltaRadius,
        2 * radius + deltaRadius,
        220,
        320,
        bruceConfig.priColor,
        bruceConfig.bgColor
    );
    tft.drawArc(
        iconCenterX,
        iconCenterY - radius,
        2.5 * radius + 2 * deltaRadius,
        2 * radius + 2 * deltaRadius,
        220,
        320,
        bruceConfig.priColor,
        bruceConfig.bgColor
    );
}
