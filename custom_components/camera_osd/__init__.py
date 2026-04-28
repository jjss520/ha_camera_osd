import logging
import os
import onvif
from datetime import timedelta
from onvif import ONVIFCamera

from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

_LOGGER = logging.getLogger(__name__)
DOMAIN = "camera_osd"

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry):
    entry.async_on_unload(entry.add_update_listener(update_listener))
    conf = {**entry.data, **entry.options}
    
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {"last_text": None, "timer_unsub": None}

    async def set_camera_osd_text_async(text):
        try:
            correct_wsdl_dir = os.path.join(os.path.dirname(onvif.__file__), "wsdl")
            cam = ONVIFCamera(
                conf["cam_ip"],
                int(conf.get("cam_port", 80)),
                conf["cam_user"],
                conf["cam_pass"],
                wsdl_dir=correct_wsdl_dir
            )
            
            await cam.update_xaddrs()
            media = await cam.create_media_service()
            
            osd_config = await media.GetOSD({"OSDToken": conf["osd_token"]})
            osd = osd_config.OSD if hasattr(osd_config, "OSD") else osd_config

            if not hasattr(osd, "TextString") or osd.TextString is None:
                _LOGGER.error("当前 OSD 不包含 TextString")
                return

            osd.TextString.Type = "Plain"
            osd.TextString.PlainText = text
            await media.SetOSD({"OSD": osd})
            _LOGGER.info(f"OSD 成功更新：{text}")
        except Exception as e:
            _LOGGER.error(f"更新摄像机失败: {e}")

    def get_entity_data(entity_id):
        # 安全过滤空实体
        if not entity_id or str(entity_id).strip() in ("", "None"):
            return None, ""
            
        state_obj = hass.states.get(entity_id)
        if state_obj is None or state_obj.state in [None, "", "unknown", "unavailable"]:
            return None, ""
            
        return state_obj.state, state_obj.attributes.get("unit_of_measurement", "")

    async def update_osd_task(now=None):
        items = []
        for i in range(1, 4):
            label = conf.get(f"slot{i}_label", "").strip()
            entity_id = conf.get(f"slot{i}_entity")
            
            val, unit = get_entity_data(entity_id)
            if val is not None:
                prefix = f"{label}:" if label else ""
                try:
                    val = f"{float(val):.1f}" if "." in str(val) else str(val)
                except ValueError:
                    pass
                items.append(f"{prefix}{val}{unit}")

        # 去掉了末尾的 ^ 换行符
        text = "  ".join(items) if items else " 暂无数据"

        if text == hass.data[DOMAIN][entry.entry_id]["last_text"]:
            return  

        hass.data[DOMAIN][entry.entry_id]["last_text"] = text
        await set_camera_osd_text_async(text)

    # 首次运行不阻塞 HA 启动，防止插件被判定为“加载失败”导致选项按钮消失
    hass.async_create_task(update_osd_task())

    interval = timedelta(seconds=int(conf.get("update_interval", 10)))
    timer_unsub = async_track_time_interval(hass, update_osd_task, interval)
    hass.data[DOMAIN][entry.entry_id]["timer_unsub"] = timer_unsub

    return True

async def update_listener(hass: HomeAssistant, entry):
    await hass.config_entries.async_reload(entry.entry_id)

async def async_unload_entry(hass, entry):
    timer_unsub = hass.data[DOMAIN][entry.entry_id].get("timer_unsub")
    if timer_unsub:
        timer_unsub()
    hass.data[DOMAIN].pop(entry.entry_id)
    return True