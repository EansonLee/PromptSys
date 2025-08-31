"""
Theme configuration management module.

This module handles theme detection and provides theme-specific content
for prompt generation. It extracts theme-related functionality from
the monolithic prompt generator.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import logging


@dataclass
class ThemeData:
    """Data class representing a theme's configuration."""
    keywords: List[str]
    content: str


class ThemeConfig:
    """
    Manages theme-specific configurations and content detection.
    
    This class provides theme detection based on keywords and returns
    appropriate fixed content for different themes.
    """
    
    def __init__(self):
        """Initialize theme configuration with predefined themes."""
        self.logger = logging.getLogger(__name__)
        
        # Theme-specific content mapping
        self._theme_configurations = self._initialize_theme_configurations()
        
        # Default fixed content (for backward compatibility)
        self._default_fixed_content = self._get_default_content()
        
        self.logger.info(f"ThemeConfig initialized with {len(self._theme_configurations)} themes")
    
    def _initialize_theme_configurations(self) -> Dict[str, ThemeData]:
        """Initialize all theme configurations."""
        return {
            'wifi': ThemeData(
                keywords=['wifi', 'WiFi', 'WIFI', '网络', '信号', '热点', '连接'],
                content="""
### 5. 数据采集逻辑：
- 使用 @/module-wifi 中的工具类，参考 中获取WiFi列表的方式来获取周围网络列表
如需要跳转Dialog参考 
- 参考 @/module-wifi  中的工具类获取WiFi、信号等信息;
- 图表使用MpChart，参考 @FreeRankFragment.kt@free_fragment_rank.xml 中图表、流量获取的用法;
- 参考 @/module_fake 中使用数据库的方法进行数据库存储，在本变体中进行编写数据库文件即可

6. 权限说明：
参考 @/variant 中其他变体以及 @PermissionComplianceManager.kt 中的申请权限的方法修改;
当前变体，同一个权限使用同一个key

- 参考 @FreeRankFragment.kt 中申请应用使用权限的方法;
7. 参考 @SpeedFragment.kt 中Fragment的可见性逻辑，对 进行修改，不需要马上进行扫描，只有进入Fragment点击按钮，给了权限后才进行扫描;
8. 新建的 Fragment逻辑也跟第 7.一样;
9. 参考 @BabyAppAdapter.kt 新建"RecycleView"的"Adapter";
10. 参考 @BabyChangeDialog.kt 新建Dialog;
11. 参考 @BabyFlowChangeActivity.kt 新建Activity;
12. 参考 @StatisticsFragment.kt 中流量的获取、使用方法;
13. 都要真实数据，WiFi无信号，没WiFi、WiFi不可用，没信号直接展示无数据即可，不要生成、展示模拟数据
14. 不执行任务编译、测试、命令
15. 不需要生成readMe文档"""
            ),
            'clean': ThemeData(
                keywords=['清理', '清洁', '净化', '清除', '整理', '优化'],
                content="""
### 权限说明：
- 不需敏感系统权限，所有数据来源于应用本地题库记录  
所有数据仅存于本地数据库（Room）

---

- 参考 @variant\\variant_clean190626\\src\\main\\java\\com\\variant\\notification\\ 中的数据库实现与写法
- 参考 @AppUsageSettingActivity.kt 中使用"KeyValueUtils"进行持久化存储
- 如需要跳转Dialog 参考 @LinkPermissionDialog.kt 
- 如需跳转 Activity 参考 @AppUsageSettingActivity.kt 
- 参考 @variant_clean190616/ 中数据库的实现与写法
不需要执测试命令进行测试

##任务执行完，最后打印**任务已经执行完成**"""
            ),
            'big': ThemeData(
                keywords=['大字版', '放大', '大字', '老年', '视力', '字体'],
                content="""
### 5. 数据采集逻辑：

如需要跳转Dialog参考 @variant\\variant_big131091\\src\\main\\java\\com\\dodg\\diverg\\ChaoqingTipDialog.kt 


6. 权限说明：
参考 @/variant  中其他变体以及 @base\\src\\main\\java\\com\\ljh\\major\\base\\utils\\PermissionComplianceManager.kt 中的申请权限的方法修改;
当前变体，同一个权限使用同一个key

7. 参考 @variant_big131125 中数据库的使用方式，数据库存放在变体下即可
8. 参考 @variant\\variant_big131125\\src\\main\\java\\com\\big\\adapter\\NoteEventAdapter.kt 编写RecycleView 的 Adapter
9. 不需要执测试命令进行测试
##任务执行完，最后打印**任务已经执行完成**"""
            ),
            'traffic': ThemeData(
                keywords=['流量', '数据', '网络', '上网', '消耗'],
                content="""
### 5. 数据采集逻辑：
- 使用 @/module-wifi 中的工具类，参考 中获取WiFi列表的方式来获取周围网络列表
如需要跳转Dialog参考 
- 参考 @/module-wifi  中的工具类获取WiFi、信号等信息;
- 图表使用MpChart，参考 @FreeRankFragment.kt@free_fragment_rank.xml 中图表、流量获取的用法;
- 参考 @/module_fake 中使用数据库的方法进行数据库存储，在本变体中进行编写数据库文件即可

6. 权限说明：
参考 @/variant 中其他变体以及 @PermissionComplianceManager.kt 中的申请权限的方法修改;
当前变体，同一个权限使用同一个key

- 参考 @FreeRankFragment.kt 中申请应用使用权限的方法;
7. 参考 @SpeedFragment.kt 中Fragment的可见性逻辑，对 进行修改，不需要马上进行扫描，只有进入Fragment点击按钮，给了权限后才进行扫描;
8. 新建的 Fragment逻辑也跟第 7.一样;
9. 参考 @BabyAppAdapter.kt 新建"RecycleView"的"Adapter";
10. 参考 @BabyChangeDialog.kt 新建Dialog;
11. 参考 @BabyFlowChangeActivity.kt 新建Activity;
12. 参考 @StatisticsFragment.kt 中流量的获取、使用方法;
13. 都要真实数据，WiFi无信号，没WiFi、WiFi不可用，没信号直接展示无数据即可，不要生成、展示模拟数据
14. 不执行任务编译、测试、命令
15. 不需要生成readMe文档"""
            )
        }
    
    def _get_default_content(self) -> str:
        """Get default fixed content for backward compatibility."""
        return """
### 5. 数据采集逻辑：
- 使用 @/module-wifi 中的工具类，参考 中获取WiFi列表的方式来获取周围网络列表
如需要跳转Dialog参考 
- 参考 @/module-wifi  中的工具类获取WiFi、信号等信息;
- 图表使用MpChart，参考 @FreeRankFragment.kt@free_fragment_rank.xml 中图表、流量获取的用法;
- 参考 @/module_fake 中使用数据库的方法进行数据库存储，在本变体中进行编写数据库文件即可

6. 权限说明：
参考 @/variant 中其他变体以及 @PermissionComplianceManager.kt 中的申请权限的方法修改;
当前变体，同一个权限使用同一个key

- 参考 @FreeRankFragment.kt 中申请应用使用权限的方法;
7. 参考 @SpeedFragment.kt 中Fragment的可见性逻辑，对 进行修改，不需要马上进行扫描，只有进入Fragment点击按钮，给了权限后才进行扫描;
8. 新建的 Fragment逻辑也跟第 7.一样;
9. 参考 @BabyAppAdapter.kt 新建"RecycleView"的"Adapter";
10. 参考 @BabyChangeDialog.kt 新建Dialog;
11. 参考 @BabyFlowChangeActivity.kt 新建Activity;
12. 参考 @StatisticsFragment.kt 中流量的获取、使用方法;
13. 都要真实数据，WiFi无信号，没WiFi、WiFi不可用，没信号直接展示无数据即可，不要生成、展示模拟数据"""
    
    def detect_theme_type(self, theme: str) -> str:
        """
        Detect theme type based on content analysis.
        
        Args:
            theme: The theme text to analyze
            
        Returns:
            The detected theme type or 'default' if no match found
        """
        theme_lower = theme.lower()
        
        # Check each theme type's keywords
        for theme_type, config in self._theme_configurations.items():
            for keyword in config.keywords:
                if keyword.lower() in theme_lower:
                    self.logger.info(f"Detected theme type: {theme_type}, keyword: {keyword}")
                    return theme_type
        
        self.logger.info("No specific theme type detected, using default fixed content")
        return 'default'
    
    def get_fixed_content(self, theme: str) -> str:
        """
        Get fixed content based on theme analysis.
        
        Args:
            theme: The theme text to analyze
            
        Returns:
            The appropriate fixed content for the theme
        """
        theme_type = self.detect_theme_type(theme)
        
        if theme_type in self._theme_configurations:
            return self._theme_configurations[theme_type].content
        else:
            return self._default_fixed_content
    
    def get_available_themes(self) -> List[str]:
        """
        Get list of available theme types.
        
        Returns:
            List of available theme names
        """
        return list(self._theme_configurations.keys())
    
    def get_theme_keywords(self, theme_type: str) -> Optional[List[str]]:
        """
        Get keywords for a specific theme type.
        
        Args:
            theme_type: The theme type to get keywords for
            
        Returns:
            List of keywords or None if theme type not found
        """
        if theme_type in self._theme_configurations:
            return self._theme_configurations[theme_type].keywords
        return None