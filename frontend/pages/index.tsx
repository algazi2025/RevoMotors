import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Simple Header */}
      <header className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold text-gray-900">RevoMotors</h1>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-gray-900 mb-4">
            Used Car AI Platform
          </h2>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Connect sellers with verified dealers. Get AI-powered offers instantly.
          </p>
        </div>

        {/* Action Cards */}
        <div className="grid md:grid-cols-2 gap-6 max-w-4xl mx-auto">
          {/* Seller Card */}
          <Link href="/seller/list-car">
            <div className="bg-white p-8 rounded-lg border-2 border-gray-200 hover:border-blue-500 hover:shadow-lg transition cursor-pointer">
              <div className="text-4xl mb-4">🚗</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">I'm a Seller</h3>
              <p className="text-gray-600 mb-4">
                List your car and receive competitive offers from verified dealers.
              </p>
              <span className="text-blue-600 font-semibold">Get Started →</span>
            </div>
          </Link>

          {/* Dealer Card */}
          <Link href="/dealer/dashboard">
            <div className="bg-white p-8 rounded-lg border-2 border-gray-200 hover:border-blue-500 hover:shadow-lg transition cursor-pointer">
              <div className="text-4xl mb-4">💼</div>
              <h3 className="text-2xl font-bold text-gray-900 mb-2">I'm a Dealer</h3>
              <p className="text-gray-600 mb-4">
                Access quality leads and make offers powered by AI insights.
              </p>
              <span className="text-blue-600 font-semibold">Access Dashboard →</span>
            </div>
          </Link>
        </div>

        {/* Features */}
        <div className="mt-16 grid md:grid-cols-3 gap-6 text-center">
          <div>
            <div className="text-3xl mb-2">⚡</div>
            <h4 className="font-semibold text-gray-900 mb-1">Fast Process</h4>
            <p className="text-sm text-gray-600">List in under 2 minutes</p>
          </div>
          <div>
            <div className="text-3xl mb-2">🤖</div>
            <h4 className="font-semibold text-gray-900 mb-1">AI Powered</h4>
            <p className="text-sm text-gray-600">Smart market pricing</p>
          </div>
          <div>
            <div className="text-3xl mb-2">✅</div>
            <h4 className="font-semibold text-gray-900 mb-1">Verified Dealers</h4>
            <p className="text-sm text-gray-600">Trusted professionals only</p>
          </div>
        </div>
      </main>
    </div>
  );
}