# FastNavGenerator v4.0

![](public/1.png)
![](public/2.png)

## 项目概述

FastNavGenerator 是一个功能强大的导航网站生成工具，专为开发团队和项目组设计。它可以从 JSON 配置文件生成美观的导航网页，并支持一键部署为 Windows 系统服务。

### 核心特性

`🎨 美观的导航界面`：支持列表和网格两种布局，响应式设计
`⚙️ 一键服务部署`：通过 NSSM 将网站部署为 Windows 系统服务
`📱 多设备访问`：支持局域网内其他设备访问
`🔄 自动重启`：服务崩溃后自动恢复
`📊 日志管理`：自动日志轮转，防止日志文件过大
`🔧 完整的管理界面`：通过批处理脚本提供完整的管理功能

## 目录结构

```asciidoc
FastNavGenerator/
 ├── nssm/              # NSSM 服务管理器
 │   ├── win32/         # 32位版本
 │   │   └── nssm.exe
 │   └── win64/         # 64位版本（主要使用）
 │       └── nssm.exe
 ├── webhttp/           # HTTP 服务器程序
 │   ├── nhttp.exe      # 主HTTP服务器
 │   └── simple-http-server.exe  # 备用服务器
 ├── FastNavGenerator.bat     # 主管理界面
 ├── FastNavGenerator.json    # 配置文件
 ├── FastNavGenerator.exe     # 生成器程序（可选）
 └── index.html               # 生成的网站

```

## 快速开始

### 1. 准备二进制文件

首次使用前，请确保以下文件已放置到正确位置：

1. `NSSM 服务管理器`：
   - 下载 [NSSM](https://nssm.cc/download)
   - 将 `nssm.exe` 放入 `nssm/win64/` 文件夹

2. `HTTP 服务器`：
   - 将 `nhttp.exe` 或 `simple-http-server.exe` 放入 `webhttp/` 文件夹

### 2. 运行管理界面

以`管理员身份`运行 `FastNavGenerator.bat`：

`右键点击 FastNavGenerator.bat → 以管理员身份运行`

### 3. 主要功能菜单

```asciidoc
========================================
   FastNav Generator - Main Menu
========================================
 1. Generate HTML Website          # 生成网站
 2. Start Local Server (Temporary) # 启动临时服务器
 3. Install as Windows Service     # 安装为系统服务 ⭐
 4. Uninstall Windows Service      # 卸载服务
 5. Start Service                  # 启动服务
 6. Stop Service                   # 停止服务
 7. Restart Service                # 重启服务
 8. Check Service Status           # 检查状态
 9. View Service Logs              # 查看日志
10. Config Management              # 配置管理
13. Test Service Access            # 测试访问
14. System Diagnostics             # 系统诊断
15. Exit                           # 退出
```


### 4. 安装为系统服务（推荐）

选择菜单选项 `3`，程序将自动：
- 生成导航网站
- 配置 NSSM 服务
- 安装为 Windows 系统服务
- 设置开机自启动
- 启动服务并打开浏览器

### 5. 访问网站

服务安装成功后，可通过以下地址访问：
- `本地访问`：http://localhost:8002
- `局域网访问`：http://[你的IP地址]:8002

## 配置管理

### 配置文件结构

编辑 `FastNavGenerator.json` 来自定义你的导航网站：

```json
{
  "site": {
    "title": "我的导航中心",
    "default_layout": "list",
    "port": 8002
  },
  "categories": [
    {
      "name": "开发工具",
      "icon": "🛠️",
      "type": "normal"
    }
  ],
  "normal": {
    "开发工具": {
      "links": [
        {
          "name": "Visual Studio Code",
          "url": "https://code.visualstudio.com/",
          "description": "强大的代码编辑器",
          "type": "Editor",
          "tag": "IDE"
        }
      ]
    }
  }
}
```


### 通过菜单修改配置

在主菜单中选择 `10` 进入配置管理：
- 编辑配置文件
- 修改服务器端口
- 切换自动打开浏览器设置
- 更换 HTTP 服务器

## 系统服务管理

### 常用命令

```bash
# 启动服务
nssm\win64\nssm.exe start FastNavWebService

# 停止服务  
nssm\win64\nssm.exe stop FastNavWebService

# 重启服务
nssm\win64\nssm.exe restart FastNavWebService

# 查看状态
nssm\win64\nssm.exe status FastNavWebService

# 卸载服务
nssm\win64\nssm.exe remove FastNavWebService confirm
```


### 日志文件

- `service.log` - 服务运行日志
- `service_error.log` - 错误日志

日志自动轮转：最大 10MB，每天轮转一次。

## 故障排除

### 常见问题

1. `服务启动失败`
   - 检查是否以管理员身份运行
   - 查看 `service_error.log` 文件
   - 确保端口 8002 未被占用

2. `无法访问网站`
   - 运行菜单选项 `14` 进行系统诊断
   - 检查防火墙设置
   - 确认服务正在运行

3. `缺少二进制文件`
   - 确保 `nssm/win64/nssm.exe` 存在
   - 确保 `webhttp/nhttp.exe` 存在

### 诊断工具

使用菜单选项 `14` 获取完整的系统诊断信息，包括：
- 服务状态
- 端口占用情况
- 文件完整性检查
- 网络配置信息

## 发布版本

### 自动构建

项目使用 GitHub Actions 自动构建发布版本。每个标签推送都会触发构建流程，生成包含以下内容的 ZIP 包：

- `FastNavGenerator.exe` - 主程序
- `FastNavGenerator.bat` - 管理界面
- `FastNavGenerator.json` - 配置文件
- 目录结构（需要用户自行添加二进制文件）

### 手动构建

如果需要手动构建可执行文件：

`pip install pyinstaller
pyinstaller --onefile --noconsole FastNavGenerator.py`

## 技术支持

- `GitHub`：[项目仓库](https://github.com/yourusername/FastNavGenerator)
- `版本`：v4.0 (NSSM Edition)
- `更新日期`：2025年2月

---

## 升级说明

### v4.0 版本重大改进

1. `移除 Python 依赖`：不再需要安装 Python 和 pywin32
2. `NSSM 服务管理`：使用 NSSM 作为服务管理器，更稳定可靠
3. `独立的 HTTP 服务器`：使用 `nhttp.exe` 提供网页服务
4. `完整的服务管理`：安装、启动、停止、重启、日志查看一体化
5. `更好的故障恢复`：服务崩溃后自动重启

### 从旧版本迁移

如果从 v3.x 版本升级：
1. 卸载旧版本服务（使用旧版本的卸载功能）
2. 下载 v4.0 版本
3. 按照"快速开始"步骤重新安装