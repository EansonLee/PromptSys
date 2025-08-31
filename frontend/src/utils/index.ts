export function extractFunctionModules(functionOutput: string): string {
  if (!functionOutput) return '';
  
  // Remove example content
  let content = functionOutput.replace(/\*\*示例展示[：:]\*\*[\s\S]*?(?=\n\n|$)/g, '');
  
  // Remove end markers
  const endMarkers = [
    'UI要求：',
    'UI 要求：', 
    '权限说明：',
    '数据采集逻辑：',
    '任务执行完'
  ];
  
  for (const marker of endMarkers) {
    const markerIndex = content.indexOf(marker);
    if (markerIndex !== -1) {
      content = content.substring(0, markerIndex).trim();
      break;
    }
  }
  
  const lines = content.split('\n');
  const moduleStartIndexes: number[] = [];
  
  // Find module titles
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i]?.trim() || '';
    const modulePatterns = [
      /###\s*🔹?\s*模块\s*\d+/i,
      /🔹\s*模块\s*\d+/i,
      /模块\s*\d+[：:]/i,
      /模块\s*\d+\s*[（(]/i
    ];
    
    const isModuleTitle = modulePatterns.some(pattern => pattern.test(line));
    
    if (isModuleTitle) {
      moduleStartIndexes.push(i);
    }
  }
  
  if (moduleStartIndexes.length === 0) {
    return content.trim();
  }
  
  const modules: string[] = [];
  
  for (let i = 0; i < moduleStartIndexes.length; i++) {
    const startLineIndex = moduleStartIndexes[i];
    const endLineIndex = i < moduleStartIndexes.length - 1 ? moduleStartIndexes[i + 1] : lines.length;
    
    const moduleLines = lines.slice(startLineIndex, endLineIndex);
    
    const filteredLines = moduleLines.filter(line => {
      const trimmed = (line || '').trim();
      return trimmed !== '' && trimmed !== '---' && trimmed !== '###' && trimmed !== '======';
    });
    
    const moduleContent = filteredLines.join('\n').trim();
    
    if (moduleContent && moduleContent.length > 10) {
      modules.push(moduleContent);
    }
  }
  
  return modules.length > 0 ? modules.join('\n\n---\n\n') : content.trim();
}

export function generateId(prefix = 'id'): string {
  return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

export function formatTimestamp(timestamp: string): string {
  try {
    return new Date(timestamp).toLocaleString('zh-CN');
  } catch {
    return timestamp;
  }
}

export function copyToClipboard(text: string): Promise<void> {
  if (navigator.clipboard && window.isSecureContext) {
    return navigator.clipboard.writeText(text);
  } else {
    // Fallback for older browsers
    const textArea = document.createElement('textarea');
    textArea.value = text;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();
    
    return new Promise((resolve, reject) => {
      if (document.execCommand('copy')) {
        resolve();
      } else {
        reject(new Error('Unable to copy to clipboard'));
      }
      document.body.removeChild(textArea);
    });
  }
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): T & { cancel: () => void } {
  let timeout: NodeJS.Timeout | null = null;

  const debounced = ((...args: Parameters<T>) => {
    const later = () => {
      timeout = null;
      func(...args);
    };
    
    if (timeout !== null) {
      clearTimeout(timeout);
    }
    timeout = setTimeout(later, wait);
  }) as T & { cancel: () => void };

  debounced.cancel = () => {
    if (timeout !== null) {
      clearTimeout(timeout);
      timeout = null;
    }
  };

  return debounced;
}

export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): T {
  let inThrottle: boolean;
  return ((...args: Parameters<T>) => {
    if (!inThrottle) {
      func.apply(null, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  }) as T;
}