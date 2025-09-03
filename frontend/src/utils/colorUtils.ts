// 颜色处理工具函数

export interface ColorInfo {
  original: string;    // 原始输入
  hex: string;        // 十六进制格式
  rgb: string;        // RGB格式
  isValid: boolean;   // 是否是有效颜色
}

export interface ParsedColors {
  colors: ColorInfo[];
  hasValidColors: boolean;
  invalidInputs: string[];
}

// 中文颜色名映射到十六进制
const CHINESE_COLORS: Record<string, string> = {
  // 基本色
  '红色': '#FF0000',
  '绿色': '#00FF00',
  '蓝色': '#0000FF',
  '黄色': '#FFFF00',
  '青色': '#00FFFF',
  '洋红': '#FF00FF',
  '紫色': '#800080',
  '粉色': '#FFC0CB',
  '橙色': '#FFA500',
  '棕色': '#A52A2A',
  '黑色': '#000000',
  '白色': '#FFFFFF',
  '灰色': '#808080',
  
  // 常用色调
  '深红': '#8B0000',
  '浅红': '#FFB6C1',
  '深蓝': '#00008B',
  '浅蓝': '#ADD8E6',
  '深绿': '#006400',
  '浅绿': '#90EE90',
  '深紫': '#4B0082',
  '浅紫': '#DDA0DD',
  '深灰': '#2F4F4F',
  '浅灰': '#D3D3D3',
  
  // 特殊色调描述
  '蓝色科技感': '#0066CC',
  '绿色清新': '#32CD32',
  '紫色梦幻': '#9370DB',
  '粉色温馨': '#FFB6C1',
  '橙色活力': '#FF7F50',
  '金色豪华': '#FFD700',
  '银色现代': '#C0C0C0',
  '黑色简约': '#1A1A1A',
  '白色简洁': '#F8F8FF',
  
  // 渐变色描述（取主色调）
  '渐变蓝': '#4169E1',
  '渐变紫': '#6A5ACD',
  '渐变粉': '#FF69B4',
  '渐变橙': '#FF6347',
  '彩虹色': '#FF0080'
};

// 英文颜色名映射到十六进制
const ENGLISH_COLORS: Record<string, string> = {
  'red': '#FF0000',
  'green': '#00FF00',
  'blue': '#0000FF',
  'yellow': '#FFFF00',
  'cyan': '#00FFFF',
  'magenta': '#FF00FF',
  'purple': '#800080',
  'pink': '#FFC0CB',
  'orange': '#FFA500',
  'brown': '#A52A2A',
  'black': '#000000',
  'white': '#FFFFFF',
  'gray': '#808080',
  'grey': '#808080',
  
  // 扩展色彩
  'darkred': '#8B0000',
  'lightblue': '#ADD8E6',
  'darkblue': '#00008B',
  'lightgreen': '#90EE90',
  'darkgreen': '#006400',
  'gold': '#FFD700',
  'silver': '#C0C0C0'
};

/**
 * 验证十六进制颜色格式
 */
export function isValidHexColor(color: string): boolean {
  const hexPattern = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/;
  return hexPattern.test(color);
}

/**
 * 验证RGB颜色格式
 */
export function isValidRgbColor(color: string): boolean {
  const rgbPattern = /^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$/;
  const match = color.match(rgbPattern);
  if (!match) return false;
  
  const [, r, g, b] = match;
  const red = parseInt(r!, 10);
  const green = parseInt(g!, 10);
  const blue = parseInt(b!, 10);
  
  return red >= 0 && red <= 255 && green >= 0 && green <= 255 && blue >= 0 && blue <= 255;
}

/**
 * 将RGB转换为十六进制
 */
export function rgbToHex(r: number, g: number, b: number): string {
  const toHex = (n: number) => {
    const hex = n.toString(16);
    return hex.length === 1 ? '0' + hex : hex;
  };
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`.toUpperCase();
}

/**
 * 将十六进制转换为RGB
 */
export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return result ? {
    r: parseInt(result[1]!, 16),
    g: parseInt(result[2]!, 16),
    b: parseInt(result[3]!, 16)
  } : null;
}

/**
 * 解析单个颜色输入
 */
export function parseColor(input: string): ColorInfo {
  const trimmed = input.trim();
  
  // 十六进制格式
  if (isValidHexColor(trimmed)) {
    const rgb = hexToRgb(trimmed);
    return {
      original: input,
      hex: trimmed.toUpperCase(),
      rgb: rgb ? `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})` : '',
      isValid: true
    };
  }
  
  // RGB格式
  if (isValidRgbColor(trimmed)) {
    const match = trimmed.match(/^rgb\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*\)$/);
    if (match) {
      const [, r, g, b] = match;
      const red = parseInt(r!, 10);
      const green = parseInt(g!, 10);
      const blue = parseInt(b!, 10);
      return {
        original: input,
        hex: rgbToHex(red, green, blue),
        rgb: trimmed,
        isValid: true
      };
    }
  }
  
  // 中文颜色名
  const chineseColor = CHINESE_COLORS[trimmed];
  if (chineseColor) {
    const rgb = hexToRgb(chineseColor);
    return {
      original: input,
      hex: chineseColor,
      rgb: rgb ? `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})` : '',
      isValid: true
    };
  }
  
  // 英文颜色名
  const englishColor = ENGLISH_COLORS[trimmed.toLowerCase()];
  if (englishColor) {
    const rgb = hexToRgb(englishColor);
    return {
      original: input,
      hex: englishColor,
      rgb: rgb ? `rgb(${rgb.r}, ${rgb.g}, ${rgb.b})` : '',
      isValid: true
    };
  }
  
  // 无效颜色
  return {
    original: input,
    hex: '',
    rgb: '',
    isValid: false
  };
}

/**
 * 解析多颜色输入字符串
 */
export function parseMultipleColors(input: string): ParsedColors {
  if (!input || !input.trim()) {
    return {
      colors: [],
      hasValidColors: false,
      invalidInputs: []
    };
  }
  
  // 使用多种分隔符分割：逗号、顿号、分号、空格
  const colorInputs = input
    .split(/[,，、;；\s]+/)
    .map(s => s.trim())
    .filter(s => s.length > 0);
  
  const colors: ColorInfo[] = [];
  const invalidInputs: string[] = [];
  
  for (const colorInput of colorInputs) {
    const colorInfo = parseColor(colorInput);
    colors.push(colorInfo);
    
    if (!colorInfo.isValid) {
      invalidInputs.push(colorInput);
    }
  }
  
  return {
    colors,
    hasValidColors: colors.some(c => c.isValid),
    invalidInputs
  };
}

/**
 * 将颜色信息数组转换为显示字符串
 */
export function colorsToDisplayString(colors: ColorInfo[]): string {
  return colors
    .filter(c => c.isValid)
    .map(c => c.hex)
    .join('、');
}

/**
 * 生成颜色的CSS样式
 */
export function getColorStyle(hex: string): React.CSSProperties {
  return {
    backgroundColor: hex,
    color: getContrastColor(hex)
  };
}

/**
 * 根据背景色获取对比色（用于文字）
 */
export function getContrastColor(hex: string): string {
  const rgb = hexToRgb(hex);
  if (!rgb) return '#000000';
  
  // 计算亮度
  const brightness = (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
  return brightness > 128 ? '#000000' : '#FFFFFF';
}

/**
 * 获取颜色的亮度（0-255）
 */
export function getColorBrightness(hex: string): number {
  const rgb = hexToRgb(hex);
  if (!rgb) return 0;
  
  return (rgb.r * 299 + rgb.g * 587 + rgb.b * 114) / 1000;
}

/**
 * 判断颜色是否为深色
 */
export function isDarkColor(hex: string): boolean {
  return getColorBrightness(hex) < 128;
}

/**
 * 生成随机颜色
 */
export function generateRandomColor(): string {
  const letters = '0123456789ABCDEF';
  let color = '#';
  for (let i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

/**
 * 预设颜色调色板
 */
export const PRESET_COLORS = [
  // 科技蓝色系
  '#0066CC', '#4A90E2', '#2196F3', '#03A9F4', '#00BCD4',
  // 绿色系
  '#4CAF50', '#8BC34A', '#CDDC39', '#32CD32', '#00C851',
  // 紫色系
  '#9C27B0', '#673AB7', '#3F51B5', '#9370DB', '#8A2BE2',
  // 红色系
  '#F44336', '#E91E63', '#FF5722', '#FF6B6B', '#FF4757',
  // 橙黄色系
  '#FF9800', '#FFC107', '#FFEB3B', '#FFD700', '#FFA726',
  // 中性色系
  '#607D8B', '#9E9E9E', '#795548', '#424242', '#263238'
];

/**
 * 获取预设颜色分组
 */
export const getPresetColorGroups = () => [
  {
    name: '科技蓝',
    colors: ['#0066CC', '#4A90E2', '#2196F3', '#03A9F4', '#00BCD4']
  },
  {
    name: '自然绿',
    colors: ['#4CAF50', '#8BC34A', '#CDDC39', '#32CD32', '#00C851']
  },
  {
    name: '梦幻紫',
    colors: ['#9C27B0', '#673AB7', '#3F51B5', '#9370DB', '#8A2BE2']
  },
  {
    name: '活力红',
    colors: ['#F44336', '#E91E63', '#FF5722', '#FF6B6B', '#FF4757']
  },
  {
    name: '温暖橙',
    colors: ['#FF9800', '#FFC107', '#FFEB3B', '#FFD700', '#FFA726']
  },
  {
    name: '中性灰',
    colors: ['#607D8B', '#9E9E9E', '#795548', '#424242', '#263238']
  }
];