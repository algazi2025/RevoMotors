import React from 'react';
import Link from 'next/link';
import { Car, TrendingUp, CheckCircle } from 'lucide-react';

export default function DealerDashboard() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-2">
            <Car className="w-6 h-6 text-blue-600" />
            <h1 className="text-xl font-bold">Dealer Dashboard</h1>
          </div>
          <Link href="/" className="text-blue-600 hover:underline">Logout</Link>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Active Leads</h2>

        <div className="bg-white rounded-lg border p-8 mb-8">
          <p className="text-gray-600 text-center py-8">
            No active leads yet. Check back soon!
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-white p-6 rounded-lg border">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl font-bold text-blue-600">0</div>
              <Car className="w-8 h-8 text-blue-200" />
            </div>
            <div className="text-gray-600">Active Leads</div>
          </div>
          <div className="bg-white p-6 rounded-lg border">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl font-bold text-green-600">0</div>
              <TrendingUp className="w-8 h-8 text-green-200" />
            </div>
            <div className="text-gray-600">Offers Made</div>
          </div>
          <div className="bg-white p-6 rounded-lg border">
            <div className="flex items-center justify-between mb-4">
              <div className="text-3xl font-bold text-purple-600">0</div>
              <CheckCircle className="w-8 h-8 text-purple-200" />
            </div>
            <div className="text-gray-600">Deals Closed</div>
          </div>
        </div>
      </main>
    </div>
  );
}