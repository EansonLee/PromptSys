import PromptGenerator from '@/components/PromptGenerator'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl font-bold text-center text-gray-800 mb-8">
          提示词生成系统
        </h1>
        <PromptGenerator />
      </div>
    </main>
  )
}
