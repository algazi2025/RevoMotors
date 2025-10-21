import React, { useState } from 'react';
import Link from 'next/link';
import { ArrowLeft, Car } from 'lucide-react';

export default function ListCar() {
  const [formData, setFormData] = useState({
    year: '',
    make: '',
    model: '',
    mileage: '',
    condition: 'good',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    alert('Form submitted! (Connect to your backend API here)');
    console.log('Form data:', formData);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link href="/" className="flex items-center text-blue-600 hover:text-blue-700">
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Home
          </Link>
          <Car className="w-6 h-6 text-blue-600" />
        </div>
      </header>

      <main className="max-w-2xl mx-auto px-4 py-12">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">List Your Car</h1>
        <p className="text-gray-600 mb-8">Fill out the details below to get AI-powered offers</p>

        <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-sm border">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Year
              </label>
              <input
                type="number"
                required
                value={formData.year}
                onChange={(e) => setFormData({...formData, year: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="2020"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Make
              </label>
              <input
                type="text"
                required
                value={formData.make}
                onChange={(e) => setFormData({...formData, make: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Honda"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Model
              </label>
              <input
                type="text"
                required
                value={formData.model}
                onChange={(e) => setFormData({...formData, model: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Civic"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Mileage
              </label>
              <input
                type="number"
                required
                value={formData.mileage}
                onChange={(e) => setFormData({...formData, mileage: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="45000"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Condition
              </label>
              <select
                value={formData.condition}
                onChange={(e) => setFormData({...formData, condition: e.target.value})}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="excellent">Excellent</option>
                <option value="good">Good</option>
                <option value="fair">Fair</option>
                <option value="poor">Poor</option>
              </select>
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 text-white py-4 rounded-lg font-semibold hover:bg-blue-700 transition shadow-lg"
            >
              Get AI Offers
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}