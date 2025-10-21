import React from 'react';
import Link from 'next/link';

export default function DealerDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-6xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-xl font-bold">Dealer Dashboard</h1>
          <Link href="/" className="text-blue-600 hover:underline">Logout</Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Active Leads</h2>

        <div className="bg-white rounded-lg border p-6">
          <p className="text-gray-600 text-center py-8">
            No active leads yet. Check back soon!
          </p>
        </div>

        <div className="mt-8 grid md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg border">
            <div className="text-3xl font-bold text-blue-600 mb-2">0</div>
            <div className="text-gray-600">Active Leads</div>
          </div>
          <div className="bg-white p-6 rounded-lg border">
            <div className="text-3xl font-bold text-green-600 mb-2">0</div>
            <div className="text-gray-600">Offers Made</div>
          </div>
          <div className="bg-white p-6 rounded-lg border">
            <div className="text-3xl font-bold text-purple-600 mb-2">0</div>
            <div className="text-gray-600">Deals Closed</div>
          </div>
        </div>
      </main>
    </div>
  );
}