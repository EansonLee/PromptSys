import PromptGeneratorRefactored from '@/components/PromptGeneratorRefactored';

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8 sm:px-6 lg:px-8 relative">
      {/* Premium Header with Enhanced Glass Effect */}
      <header className="text-center mb-16 relative">
        {/* Background Aurora Effect */}
        <div className="absolute inset-0 rounded-3xl overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-50/20 via-purple-50/10 to-pink-50/20 animate-gradient-shift"></div>
        </div>
        
        <div className="glass-premium-header rounded-3xl p-8 sm:p-10 lg:p-12 mb-8 animate-glass-glow relative z-10">
          {/* Title with Enhanced Effects */}
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent mb-6 animate-shimmer relative">
            提示词生成系统
            {/* Title Glow Effect */}
            <span className="absolute inset-0 bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent opacity-50 blur-sm -z-10">
              提示词生成系统
            </span>
          </h1>
          
          <p className="text-lg sm:text-xl text-glass-primary max-w-2xl mx-auto mb-8 leading-relaxed font-medium">
            AI驱动的创意提示词生成平台，支持多主题模板和自动化工作流
          </p>
          
          {/* Enhanced Feature Badge */}
          <div className="flex justify-center">
            <div className="glass-premium rounded-full px-8 py-4 flex items-center space-x-4 text-sm text-glass-primary hover:scale-105 transition-all duration-500 group">
              <div className="w-3 h-3 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full animate-pulse-glow"></div>
              <svg className="w-5 h-5 group-hover:rotate-12 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span className="font-semibold">使用先进的AI技术为您的项目生成专业提示词</span>
            </div>
          </div>
        </div>

        {/* Enhanced Decorative Elements */}
        <div className="absolute -top-6 -left-6 w-12 h-12 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full opacity-30 animate-floating blur-sm"></div>
        <div className="absolute -top-3 -right-8 w-8 h-8 bg-gradient-to-r from-purple-400 to-pink-400 rounded-full opacity-40 animate-floating" style={{ animationDelay: '1.5s' }}></div>
        <div className="absolute -bottom-6 left-1/3 w-6 h-6 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full opacity-35 animate-floating" style={{ animationDelay: '0.5s' }}></div>
        <div className="absolute -bottom-3 right-1/4 w-4 h-4 bg-gradient-to-r from-pink-400 to-purple-400 rounded-full opacity-25 animate-floating" style={{ animationDelay: '2s' }}></div>
        
        {/* Light rays */}
        <div className="absolute top-0 left-1/2 w-px h-20 bg-gradient-to-b from-blue-400/30 to-transparent transform -translate-x-1/2 -translate-y-10"></div>
        <div className="absolute top-0 left-1/3 w-px h-16 bg-gradient-to-b from-purple-400/20 to-transparent transform -translate-x-1/2 -translate-y-8" style={{ animationDelay: '1s' }}></div>
        <div className="absolute top-0 right-1/3 w-px h-12 bg-gradient-to-b from-pink-400/25 to-transparent transform -translate-x-1/2 -translate-y-6" style={{ animationDelay: '2s' }}></div>
      </header>

      {/* Main Content */}
      <PromptGeneratorRefactored className="animate-fade-in" />

      {/* Premium Footer with Glass Effect */}
      <footer className="mt-20 text-center relative">
        <div className="glass-tertiary rounded-2xl p-6 backdrop-blur-sm">
          <div className="text-sm text-glass-muted">
            <p>© 2024 提示词生成系统. 基于 Next.js 15 和 React 19 构建</p>
          </div>
        </div>
        
        {/* Footer decorative element */}
        <div className="absolute -bottom-2 left-1/2 transform -translate-x-1/2 w-16 h-1 bg-gradient-to-r from-transparent via-purple-400 to-transparent opacity-50 rounded-full"></div>
      </footer>
    </div>
  );
}
