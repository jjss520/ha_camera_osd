# Camera OSD - Home Assistant 自定义组件

一个用于在 Home Assistant 中集成和管理相机 OSD（On-Screen Display）功能的自定义组件。

## 功能特性

- 支持相机 OSD 配置和管理
- 提供中文界面支持
- 易于安装和配置

## 安装方法

### 方式一：通过 HACS 安装（推荐）

1. 确保已安装 [HACS](https://hacs.xyz/)
2. 在 HACS 中搜索 "Camera OSD"
3. 点击安装
4. 重启 Home Assistant

### 方式二：手动安装

1. 将 `custom_components/camera_osd` 文件夹复制到 Home Assistant 的 `config/custom_components/` 目录
2. 重启 Home Assistant
3. 在 **设置** > **设备与服务** > **添加集成** 中搜索 "Camera OSD"
4. 按照提示完成配置

## 配置

### 获取 OSD Token

在使用本插件前，需要先获取相机的 OSD Token。项目提供了 `find_token.py` 脚本来自动获取：

1. 安装依赖：
   ```bash
   pip install onvif-zeep requests urllib3
   ```

2. 编辑 `find_token.py` 文件，修改以下参数为你的相机信息：
   ```python
   CAM_IP = "192.168.1.2"    # 摄像机IP
   CAM_PORT = 80             # 默认通常是80
   CAM_USER = "admin"        # ONVIF 用户名
   CAM_PASS = "admin"        # 对应的密码
   ```

3. 运行脚本：
   ```bash
   python find_token.py
   ```

4. 脚本会输出所有可用的 OSD Token，将带单引号的 Token 名称填入 HA 插件配置中。

**注意**：请确认海康后台的「OSD设置」中已勾选「字符叠加」功能。

### Home Assistant 配置

安装完成后，可以通过 Home Assistant 的配置界面进行设置：

1. 进入 **设置** > **设备与服务**
2. 点击 **添加集成**
3. 搜索并选择 "Camera OSD"
4. 填写相机相关信息和获取到的 OSD Token

## 支持的语言

- 简体中文 (zh-Hans)

## 问题反馈

如果您在使用过程中遇到任何问题，请在 [GitHub Issues](https://github.com/jjss520/ha_camera_osd/issues) 中提交。

## 许可证

本项目遵循 MIT 许可证。
