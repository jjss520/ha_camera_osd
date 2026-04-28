import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector

DOMAIN = "camera_osd"

def get_data_schema(defaults: dict):
    """采用 suggested_value 避免空值崩溃，完美适配新版实体选择器"""
    
    return vol.Schema({
        vol.Required("cam_ip", default=str(defaults.get("cam_ip", "10.10.10.203"))): str,
        vol.Required("cam_port", default=int(defaults.get("cam_port", 80))): int,
        vol.Required("cam_user", default=str(defaults.get("cam_user", "admin"))): str,
        vol.Required("cam_pass", default=str(defaults.get("cam_pass", ""))): str,
        vol.Required("osd_token", default=str(defaults.get("osd_token", "OsdToken_102"))): str,
        
        # 使用 suggested_value 替代 default，解决空实体加载报 500 的问题
        vol.Optional("slot1_label", description={"suggested_value": defaults.get("slot1_label", "温度")}): str,
        vol.Optional("slot1_entity", description={"suggested_value": defaults.get("slot1_entity")}): selector.EntitySelector(selector.EntitySelectorConfig()),
        
        vol.Optional("slot2_label", description={"suggested_value": defaults.get("slot2_label", "湿度")}): str,
        vol.Optional("slot2_entity", description={"suggested_value": defaults.get("slot2_entity")}): selector.EntitySelector(selector.EntitySelectorConfig()),
        
        vol.Optional("slot3_label", description={"suggested_value": defaults.get("slot3_label", "进度")}): str,
        vol.Optional("slot3_entity", description={"suggested_value": defaults.get("slot3_entity")}): selector.EntitySelector(selector.EntitySelectorConfig()),

        vol.Optional("update_interval", default=int(defaults.get("update_interval", 10))): int,
    })


class CameraOSDFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title=f"OSD: {user_input.get('cam_ip')}", data=user_input)
        return self.async_show_form(step_id="user", data_schema=get_data_schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CameraOSDOptionsFlowHandler(config_entry)


class CameraOSDOptionsFlowHandler(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        # ⚠️ 核心修复：把变量名从 config_entry 改为 my_config_entry，避开系统只读属性冲突
        self.my_config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
            
        # 使用我们自己定义的变量读取配置数据
        conf = {**self.my_config_entry.data, **self.my_config_entry.options}
        return self.async_show_form(step_id="init", data_schema=get_data_schema(conf))