from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import random
import jieba
import jieba.posseg as pseg

# 设置jieba日志级别
jieba.setLogLevel(20)

@register("yinlan", "YourName", "高级淫语转换插件", "1.1.0")
class YinlanPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        # 解析配置
        self.yinlan_level = float(config.get("yinlan_level", "0.5"))
        self.yin_dict = self._parse_dict(config.get("dict", ""))
        self.pattern_rules = self._parse_pattern_rules(config.get("pattern_rules", ""))
        self._init_dict()
        
    def _init_dict(self):
        """初始化自定义词典"""
        # 添加词语替换中的多字词到分词词典
        for word in self.yin_dict:
            if len(word) > 1:
                jieba.add_word(word)

    def _parse_pattern_rules(self, rule_str: str) -> list:
        """解析模式规则字符串为列表"""
        rules = []
        for item in rule_str.split(','):
            parts = item.split('=')
            if len(parts) == 3:  # 格式: 词性=替换=概率
                rules.append({
                    "pattern": parts[0].strip(),
                    "replace": parts[1].strip(),
                    "probability": float(parts[2].strip())
                })
            elif len(parts) == 4:  # 格式: 词性=前缀=后缀=概率
                rules.append({
                    "pattern": parts[0].strip(),
                    "prefix": parts[1].strip(),
                    "suffix": parts[2].strip(),
                    "probability": float(parts[3].strip())
                })
        return rules

    def _parse_dict(self, dict_str: str) -> list:
        """解析淫乱字典字符串为列表"""
        return [w.strip() for w in dict_str.split(',') if w.strip()]
    
    def _apply_replacements(self, word: str, flag: str) -> str:
        """应用模式规则"""
        for rule in self.pattern_rules:
            if flag == rule.get('pattern') and random.random() < rule.get('probability', 1.0):
                if 'replace' in rule:
                    return rule['replace']
                prefix = rule.get('prefix', '')
                suffix = rule.get('suffix', '')
                return f"{prefix}{word}{suffix}"
        return word
    
    def convert_to_yin(self, text: str, yinlan_level: float = None) -> str:
        """将文本转换为淫语"""
        if yinlan_level is None:
            yinlan_level = self.yinlan_level
        words = pseg.cut(text)
        result = []
        
        for word, flag in words:
            # 根据淫乱度决定是否转换
            if random.random() > yinlan_level:
                result.append(word)
                continue
                
            # 应用替换规则
            converted = self._apply_replacements(word, flag)
            
            # 随机插入淫乱字典词
            if self.yin_dict and random.random() < 0.3:
                insert_word = random.choice(self.yin_dict)
                # 随机决定插入前还是后
                if random.random() < 0.5:
                    converted = f"{insert_word}{converted}"
                else:
                    converted = f"{converted}{insert_word}"
            
            # 添加随机效果
            if len(word) > 1 and random.random() < 0.2:
                converted = f'{word[0]}…{converted}'
            elif random.random() < 0.1:
                converted = f'…{converted}'
                
            result.append(converted)
            
        return ''.join(result)

    @filter.command("yl", "将文本转换为淫语")
    async def yinlan_convert(self, event: AstrMessageEvent, text: str = None):
        """将输入的文本转换为淫语
        
        Args:
            text(string): 要转换的文本
        """
        if not text or not text.strip():
            # 如果没有传入文本，输出帮助
            await self.yinlan_help(event)
            return

        try:
            result = self.convert_to_yin(text)
            yield event.plain_result(result)
        except Exception as e:
            logger.error(f"转换失败: {e}")
            yield event.plain_result("转换失败，请稍后再试")

    @filter.command("ylconfig", "配置淫乱插件参数")
    async def yinlan_config(self, event: AstrMessageEvent, text: str = None):
        """配置淫乱插件参数，支持 yinlan_level、dict、pattern_rules"""
        config = self.context.get_config()
        if not text or not text.strip():
            # 显示当前所有配置项及其值
            msg = (
                "当前配置：\n"
                f"yinlan_level = {config.get('yinlan_level', 0.8)}\n"
                f"dict = {config.get('dict', '……,❤,啊~,不要')}\n"
                f"pattern_rules = {config.get('pattern_rules', 'n=〇=0.5,v=嗯...=...啊=0.7')}\n"
                "\n用法示例：\n"
                "/ylconfig yinlan_level=0.7\n"
                "/ylconfig dict=……,❤,啊~,不要\n"
                "/ylconfig pattern_rules=n=〇=0.5,v=嗯...=...啊=0.7\n"
                "可一次设置多个参数：/ylconfig yinlan_level=0.7 dict=……,❤"
            )
            yield event.plain_result(msg)
            return

        # 支持多参数，空格分隔
        for item in text.strip().split():
            if '=' not in item:
                yield event.plain_result(f"参数格式错误: {item}，应为 key=value")
                continue
            key, value = item.split('=', 1)
            key = key.strip()
            value = value.strip()

            if key == "yinlan_level":
                try:
                    level = float(value)
                    if not 0 <= level <= 1:
                        yield event.plain_result("淫乱度必须是0~1之间的浮点数")
                        continue
                    config["yinlan_level"] = level
                    self.yinlan_level = level
                    yield event.plain_result(f"已设置淫乱度为{level}")
                except Exception:
                    yield event.plain_result("请输入0~1之间的浮点数")
            elif key == "dict":
                # 校验：不能全是空
                if not value.strip():
                    yield event.plain_result("字典不能为空")
                    continue
                config["dict"] = value
                self.yin_dict = self._parse_dict(value)
                self._init_dict()
                yield event.plain_result(f"已设置淫乱字典为: {value}")
            elif key == "pattern_rules":
                # 校验：必须包含=，且格式合理
                if not value or '=' not in value:
                    yield event.plain_result("模式规则格式错误，应为 pattern=replace=probability 或 pattern=prefix=suffix=probability")
                    continue
                config["pattern_rules"] = value
                self.pattern_rules = self._parse_pattern_rules(value)
                yield event.plain_result(f"已设置模式规则为: {value}")
            else:
                yield event.plain_result(f"不支持的配置项: {key}")

        # 保存配置
        config.save_config()

    @filter.command("ylhelp", "查看帮助")
    async def yinlan_help(self, event: AstrMessageEvent):
        """查看淫语插件帮助"""
        help_msg = (
            "淫语插件使用说明:\n"
            "/yl <文本> - 转换文本为淫语\n"
            "/ylconfig <参数> - 设置插件参数\n"
            "/ylhelp - 查看帮助\n"
            "\n配置项说明：\n"
            "yinlan_level：淫乱度(0~1之间)\n"
            "dict：淫乱字典，逗号分隔\n"
            "pattern_rules：模式规则，格式如 n=〇=0.5,v=嗯...=...啊=0.7\n"
            "\n配置示例：\n"
            "/ylconfig yinlan_level=0.7\n"
            "/ylconfig dict=……,❤,啊~,不要\n"
            "/ylconfig pattern_rules=n=〇=0.5,v=嗯...=...啊=0.7\n"
            "可一次设置多个参数：/ylconfig yinlan_level=0.7 dict=……,❤"
        )
        yield event.plain_result(help_msg)

    async def terminate(self):
        """插件卸载时清理"""
        pass 