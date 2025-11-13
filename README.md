[TOC]

# 中文版
用于在特定时间自动获取一个车位
## 使用说明
- 依据浏EDGE版本下载对应驱动
- 修改**configuration.xml**中：*position_kind*、*username*、*password*、*car_id*，*URL*为实际值
- **configuration.xml**中：*target_time*、*fresh_interval*建议保持默认值或依实际情况酌情改变
- **configuration.xml**中*debug*开启后不会点击提交，其他流程维持不变
- 确保**configuration.xml**与启动py脚本或exe在同一路径下，启动程序，等待结果

## 更新日志
V0.1 not know
V0.2 not know
V0.3 first stable version
V0.4 fix sometimes break when waiting success result
V0.5 fix sometimes wait too long when refresh page
V0.6 redirect logs to file for convenient debug
# English Version

# park
get a park postition

