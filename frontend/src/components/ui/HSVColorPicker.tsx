'use client'

import React, { useState, useRef, useEffect, useCallback, memo } from 'react';

interface HSVColor {
  h: number; // 0-360
  s: number; // 0-100  
  v: number; // 0-100
}

interface HSVColorPickerProps {
  color: string;
  onChange: (color: string) => void;
  className?: string;
}

const HSVColorPicker: React.FC<HSVColorPickerProps> = memo(({
  color,
  onChange,
  className = ''
}) => {
  const [hsv, setHsv] = useState<HSVColor>({ h: 0, s: 100, v: 100 });
  const [isDraggingSV, setIsDraggingSV] = useState(false);
  const [isDraggingH, setIsDraggingH] = useState(false);
  
  const svPanelRef = useRef<HTMLDivElement>(null);
  const hueBarRef = useRef<HTMLDivElement>(null);

  // 将十六进制颜色转换为HSV
  const hexToHsv = useCallback((hex: string): HSVColor => {
    const r = parseInt(hex.slice(1, 3), 16) / 255;
    const g = parseInt(hex.slice(3, 5), 16) / 255;
    const b = parseInt(hex.slice(5, 7), 16) / 255;

    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    const diff = max - min;

    let h = 0;
    if (diff !== 0) {
      if (max === r) {
        h = ((g - b) / diff) % 6;
      } else if (max === g) {
        h = (b - r) / diff + 2;
      } else {
        h = (r - g) / diff + 4;
      }
    }
    h = Math.round(h * 60);
    if (h < 0) h += 360;

    const s = max === 0 ? 0 : Math.round((diff / max) * 100);
    const v = Math.round(max * 100);

    return { h, s, v };
  }, []);

  // 将HSV转换为十六进制颜色
  const hsvToHex = useCallback((hsv: HSVColor): string => {
    const { h, s, v } = hsv;
    const sNorm = s / 100;
    const vNorm = v / 100;

    const c = vNorm * sNorm;
    const x = c * (1 - Math.abs(((h / 60) % 2) - 1));
    const m = vNorm - c;

    let r = 0, g = 0, b = 0;

    if (0 <= h && h < 60) {
      r = c; g = x; b = 0;
    } else if (60 <= h && h < 120) {
      r = x; g = c; b = 0;
    } else if (120 <= h && h < 180) {
      r = 0; g = c; b = x;
    } else if (180 <= h && h < 240) {
      r = 0; g = x; b = c;
    } else if (240 <= h && h < 300) {
      r = x; g = 0; b = c;
    } else if (300 <= h && h < 360) {
      r = c; g = 0; b = x;
    }

    r = Math.round((r + m) * 255);
    g = Math.round((g + m) * 255);
    b = Math.round((b + m) * 255);

    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`.toUpperCase();
  }, []);

  // 初始化HSV值
  useEffect(() => {
    if (color && color.match(/^#[0-9A-Fa-f]{6}$/)) {
      const newHsv = hexToHsv(color);
      setHsv(newHsv);
    }
  }, [color, hexToHsv]);

  // 更新颜色
  const updateColor = useCallback((newHsv: HSVColor) => {
    setHsv(newHsv);
    const hexColor = hsvToHex(newHsv);
    onChange(hexColor);
  }, [onChange, hsvToHex]);

  // 处理SV面板的鼠标事件
  const handleSVPanelMouseDown = useCallback((e: React.MouseEvent) => {
    setIsDraggingSV(true);
    const rect = svPanelRef.current?.getBoundingClientRect();
    if (rect) {
      const x = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      const y = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
      
      const newS = Math.round(x * 100);
      const newV = Math.round((1 - y) * 100);
      
      updateColor({ ...hsv, s: newS, v: newV });
    }
  }, [hsv, updateColor]);

  // 处理色相条的鼠标事件
  const handleHueBarMouseDown = useCallback((e: React.MouseEvent) => {
    setIsDraggingH(true);
    const rect = hueBarRef.current?.getBoundingClientRect();
    if (rect) {
      const y = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
      const newH = Math.round(y * 360);
      updateColor({ ...hsv, h: newH });
    }
  }, [hsv, updateColor]);

  // 鼠标移动事件
  useEffect(() => {
    const handleMouseMove = (e: MouseEvent) => {
      if (isDraggingSV && svPanelRef.current) {
        const rect = svPanelRef.current.getBoundingClientRect();
        const x = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
        const y = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
        
        const newS = Math.round(x * 100);
        const newV = Math.round((1 - y) * 100);
        
        updateColor({ ...hsv, s: newS, v: newV });
      }

      if (isDraggingH && hueBarRef.current) {
        const rect = hueBarRef.current.getBoundingClientRect();
        const y = Math.max(0, Math.min(1, (e.clientY - rect.top) / rect.height));
        const newH = Math.round(y * 360);
        updateColor({ ...hsv, h: newH });
      }
    };

    const handleMouseUp = () => {
      setIsDraggingSV(false);
      setIsDraggingH(false);
    };

    if (isDraggingSV || isDraggingH) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDraggingSV, isDraggingH, hsv, updateColor]);

  // 获取当前色相的纯色
  const getPureHueColor = useCallback((h: number) => {
    return hsvToHex({ h, s: 100, v: 100 });
  }, [hsvToHex]);

  // 计算SV面板指示器位置
  const svIndicatorStyle = {
    left: `${hsv.s}%`,
    top: `${100 - hsv.v}%`,
  };

  // 计算色相条指示器位置
  const hueIndicatorStyle = {
    top: `${(hsv.h / 360) * 100}%`,
  };

  return (
    <div className={`flex space-x-3 ${className}`}>
      {/* SV面板 - 饱和度和明度选择 */}
      <div className="relative">
        <div
          ref={svPanelRef}
          className="w-64 h-48 cursor-crosshair rounded-lg overflow-hidden border border-white/20"
          style={{
            background: `linear-gradient(to right, white, ${getPureHueColor(hsv.h)}), linear-gradient(to top, black, transparent)`
          }}
          onMouseDown={handleSVPanelMouseDown}
        >
          {/* 白色到色相的渐变 */}
          <div 
            className="absolute inset-0"
            style={{
              background: `linear-gradient(to right, white, ${getPureHueColor(hsv.h)})`
            }}
          />
          {/* 透明到黑色的渐变 */}
          <div 
            className="absolute inset-0"
            style={{
              background: 'linear-gradient(to top, black, transparent)'
            }}
          />
          
          {/* SV选择指示器 */}
          <div
            className="absolute w-3 h-3 border-2 border-white rounded-full shadow-lg transform -translate-x-1/2 -translate-y-1/2 pointer-events-none"
            style={svIndicatorStyle}
          >
            <div className="w-full h-full border border-gray-800 rounded-full"></div>
          </div>
        </div>
      </div>

      {/* 色相条 */}
      <div className="relative">
        <div
          ref={hueBarRef}
          className="w-6 h-48 cursor-pointer rounded overflow-hidden border border-white/20"
          style={{
            background: `linear-gradient(to bottom, 
              #ff0000 0%, 
              #ffff00 16.66%, 
              #00ff00 33.33%, 
              #00ffff 50%, 
              #0000ff 66.66%, 
              #ff00ff 83.33%, 
              #ff0000 100%)`
          }}
          onMouseDown={handleHueBarMouseDown}
        >
          {/* 色相选择指示器 */}
          <div
            className="absolute left-0 right-0 h-0.5 bg-white shadow-lg transform -translate-y-1/2 pointer-events-none"
            style={hueIndicatorStyle}
          >
            <div className="h-full border-t border-b border-gray-800"></div>
          </div>
        </div>
      </div>
    </div>
  );
});

HSVColorPicker.displayName = 'HSVColorPicker';

export default HSVColorPicker;