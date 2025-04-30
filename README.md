# astrbot_plugin_yinlish

![@astrbot_plugin_yinlish](https://count.getloli.com/get/@astrbot_plugin_yinlish?theme=booru-lewd&darkmode=auto)

## 插件简介

本插件为 [AstrBot](https://astrbot.app) 提供强大的"淫语"文本转换功能。支持自定义淫乱度、插入词典、模式规则。

## 功能特性

- 支持将普通文本转换为"淫语"风格
- 可自定义"淫乱度"控制转换强度
- 支持自定义插入词典（如"……,❤,啊~,不要"等）
- 支持自定义模式规则（如按词性加前后缀、概率替换等）
- 支持命令行和管理面板双配置
- 支持多参数批量配置

## 安装方法

1. 将本插件文件夹放入 AstrBot 插件目录
2. 安装依赖（如未自动安装）：
   ```
   %pip install jieba
   ```
3. 在 AstrBot 管理面板启用本插件

## 使用方法

### 基本命令

- `/yl <文本>`  
  将文本转换为淫语风格。例如：  
  `/yl 不行，那里不行。`

- `/ylconfig <参数>`  
  配置插件参数。支持如下参数，均可单独或批量设置：
  - `yinlan_level`：淫乱度（0~1之间，数值越大越"奇怪"）
  - `dict`：插入词典，逗号分隔
  - `pattern_rules`：模式规则，格式如 `n=〇=0.5,v=嗯...=...啊=0.7`

  **示例：**
  ```
  /ylconfig yinlan_level=0.7
  /ylconfig dict=……,❤,啊~,不要
  /ylconfig pattern_rules=n=〇=0.5,v=嗯...=...啊=0.7
  /ylconfig yinlan_level=0.7 dict=……,❤
  ```

- `/ylhelp`  
  查看插件详细帮助和配置说明。

### 查看/修改当前配置

- `/ylconfig`  
  不带参数时，显示当前所有配置项及其值和用法示例。

## 配置项说明

- **yinlan_level**：淫乱度（0~1之间，默认0.8）
- **dict**：淫乱字典，逗号分隔（如 `……,❤,啊~,不要`）
- **pattern_rules**：模式规则，格式如 `n=〇=0.5,v=嗯...=...啊=0.7`  
  - `n=〇=0.5` 表示名词（n）有50%概率替换为"〇"
  - `v=嗯...=...啊=0.7` 表示动词（v）有70%概率加前缀"嗯..."、后缀"...啊"

## 许可证

本插件遵循 AGPL-3.0 开源协议，详情见 LICENSE 文件。

[帮助文档](https://astrbot.app)