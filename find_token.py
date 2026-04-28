from onvif import ONVIFCamera
import zeep
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= 填入你的海康信息 =================
CAM_IP = "192.168.1.2"  # 摄像机IP
CAM_PORT = 80           # 默认通常是80
CAM_USER = "admin"      # 刚刚在集成协议里创建的 ONVIF 用户名
CAM_PASS = "admin"   # 对应的密码
# ===================================================

def find_osd_tokens():
    print(f"正在连接海康摄像机 {CAM_IP}...")
    try:
        session = requests.Session()
        session.verify = False
        cam = ONVIFCamera(
            CAM_IP, CAM_PORT, CAM_USER, CAM_PASS, 
            transport=zeep.transports.Transport(session=session)
        )
        media = cam.create_media_service()
        
        # 获取所有 OSD 配置
        osds = media.GetOSDs()
        
        if not osds:
            print("❌ 未找到任何 OSD 配置。请确认海康后台的'OSD设置'中是否已勾选'字符叠加'。")
            return
            
        print("\n✅ 成功获取！请将下方带单引号的 Token 名称填入 HA 插件中：")
        print("-" * 50)
        for osd in osds:
            text = "无文本"
            if hasattr(osd, 'TextString') and osd.TextString:
                text = osd.TextString.PlainText
            print(f"OSD Token 名称: '{osd.token}'  (当前显示的文字: {text})")
        print("-" * 50)
        
    except Exception as e:
        print(f"\n❌ 连接或获取失败，请检查账号密码及 ONVIF 是否开启。\n错误信息: {e}")

if __name__ == "__main__":
    find_osd_tokens()