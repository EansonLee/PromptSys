import PromptGeneratorRefactored from '@/components/PromptGeneratorRefactored';

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-4 sm:px-6 lg:px-8 max-w-3xl relative">
      {/* Main Content */}
      <PromptGeneratorRefactored className="animate-fade-in" />

      {/* Minimalist Footer */}
      <footer className="mt-16 text-center">
        <div className="glass-tertiary rounded-xl p-4">
          <p className="text-xs text-glass-muted">© 2024 提示词生成系统</p>
        </div>
      </footer>
    </div>
  );
}
