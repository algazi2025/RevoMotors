import React, { useState } from 'react';

export default function ListCar() {
  const [formData, setFormData] = useState({
    // Vehicle Info
    year: '',
    make: '',
    model: '',
    trim: '',
    mileage: '',
    condition: 'good',
    vin: '',
    color: '',
    transmission: 'automatic',
    fuelType: 'gasoline',
    title: 'clean',
    accidents: 'none',
    owners: '1',
    
    // Seller Info
    sellerName: '',
    email: '',
    phone: '',
    zipCode: '',
    
    // Additional
    description: '',
    askingPrice: '',
  });

  const [photos, setPhotos] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setPhotos(Array.from(e.target.files));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Convert photos to base64 for sending to API (optional - you can also use FormData)
      const photoUrls: string[] = [];
      for (const photo of photos) {
        const reader = new FileReader();
        const base64 = await new Promise<string>((resolve) => {
          reader.onloadend = () => resolve(reader.result as string);
          reader.readAsDataURL(photo);
        });
        photoUrls.push(base64);
      }

      const payload = {
        marketplace: 'direct',
        title: `${formData.year} ${formData.make} ${formData.model} ${formData.trim}`.trim(),
        year: parseInt(formData.year),
        make: formData.make,
        model: formData.model,
        trim: formData.trim,
        mileage: parseInt(formData.mileage),
        condition: formData.condition,
        vin: formData.vin,
        color: formData.color,
        transmission: formData.transmission,
        fuel_type: formData.fuelType,
        title_status: formData.title,
        accident_history: formData.accidents,
        number_of_owners: parseInt(formData.owners),
        asking_price: formData.askingPrice ? parseFloat(formData.askingPrice) : null,
        description: formData.description,
        region: formData.zipCode,
        
        // Seller contact info
        seller_contact_name: formData.sellerName,
        seller_contact_email: formData.email,
        seller_contact_phone: formData.phone,
        
        // Photos (as base64 or URLs)
        photos: photoUrls,
      };

      const response = await fetch('https://revomotors.onrender.com/api/leads/webhook/lead_received', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        alert(
          `✅ Success! Your car has been listed.\n\n` +
          `Listing ID: ${data.listing_id}\n` +
          `AI Fair Offer: $${data.ai_draft_offer?.fair || 'N/A'}\n` +
          `Price Range: $${data.ai_draft_offer?.low || 'N/A'} - $${data.ai_draft_offer?.max || 'N/A'}\n\n` +
          `Dealers will contact you soon!`
        );
        
        // Reset form
        setFormData({
          year: '', make: '', model: '', trim: '', mileage: '', condition: 'good',
          vin: '', color: '', transmission: 'automatic', fuelType: 'gasoline',
          title: 'clean', accidents: 'none', owners: '1',
          sellerName: '', email: '', phone: '', zipCode: '',
          description: '', askingPrice: '',
        });
        setPhotos([]);
      } else {
        alert(`Error: ${data.detail || 'Failed to submit listing'}`);
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error connecting to server. Please check your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  const inputStyle = {
    width: '100%',
    padding: '12px',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '16px',
  };

  const labelStyle = {
    display: 'block',
    fontWeight: '500',
    marginBottom: '8px',
    fontSize: '14px',
  };

  const sectionStyle = {
    marginBottom: '30px',
    paddingBottom: '20px',
    borderBottom: '1px solid #e5e7eb',
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui' }}>
      <div style={{ backgroundColor: 'white', borderBottom: '1px solid #e5e7eb', padding: '20px' }}>
        <div style={{ maxWidth: '900px', margin: '0 auto' }}>
          <a href="/" style={{ color: '#2563eb', textDecoration: 'none', fontSize: '14px' }}>
            ← Back to Home
          </a>
        </div>
      </div>

      <div style={{ maxWidth: '900px', margin: '0 auto', padding: '40px 20px' }}>
        <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '10px' }}>
          List Your Car
        </h1>
        <p style={{ color: '#6b7280', marginBottom: '30px' }}>
          Fill out all the details below to get accurate AI-powered offers from verified dealers
        </p>

        <form onSubmit={handleSubmit} style={{ backgroundColor: 'white', padding: '40px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
          
          {/* Vehicle Information */}
          <div style={sectionStyle}>
            <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '20px' }}>
              🚗 Vehicle Information
            </h2>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
              <div>
                <label style={labelStyle}>Year *</label>
                <input
                  type="number"
                  required
                  min="1990"
                  max="2025"
                  value={formData.year}
                  onChange={(e) => setFormData({...formData, year: e.target.value})}
                  style={inputStyle}
                  placeholder="2020"
                />
              </div>

              <div>
                <label style={labelStyle}>Make *</label>
                <input
                  type="text"
                  required
                  value={formData.make}
                  onChange={(e) => setFormData({...formData, make: e.target.value})}
                  style={inputStyle}
                  placeholder="Honda"
                />
              </div>

              <div>
                <label style={labelStyle}>Model *</label>
                <input
                  type="text"
                  required
                  value={formData.model}
                  onChange={(e) => setFormData({...formData, model: e.target.value})}
                  style={inputStyle}
                  placeholder="Civic"
                />
              </div>

              <div>
                <label style={labelStyle}>Trim</label>
                <input
                  type="text"
                  value={formData.trim}
                  onChange={(e) => setFormData({...formData, trim: e.target.value})}
                  style={inputStyle}
                  placeholder="EX, LX, Sport"
                />
              </div>

              <div>
                <label style={labelStyle}>Mileage *</label>
                <input
                  type="number"
                  required
                  value={formData.mileage}
                  onChange={(e) => setFormData({...formData, mileage: e.target.value})}
                  style={inputStyle}
                  placeholder="45000"
                />
              </div>

              <div>
                <label style={labelStyle}>VIN Number *</label>
                <input
                  type="text"
                  required
                  minLength={17}
                  maxLength={17}
                  value={formData.vin}
                  onChange={(e) => setFormData({...formData, vin: e.target.value.toUpperCase()})}
                  style={inputStyle}
                  placeholder="1HGBH41JXMN109186"
                />
              </div>

              <div>
                <label style={labelStyle}>Color</label>
                <input
                  type="text"
                  value={formData.color}
                  onChange={(e) => setFormData({...formData, color: e.target.value})}
                  style={inputStyle}
                  placeholder="Black, White, Silver"
                />
              </div>

              <div>
                <label style={labelStyle}>Condition *</label>
                <select
                  value={formData.condition}
                  onChange={(e) => setFormData({...formData, condition: e.target.value})}
                  style={inputStyle}
                >
                  <option value="excellent">Excellent</option>
                  <option value="good">Good</option>
                  <option value="fair">Fair</option>
                  <option value="poor">Poor</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Transmission *</label>
                <select
                  value={formData.transmission}
                  onChange={(e) => setFormData({...formData, transmission: e.target.value})}
                  style={inputStyle}
                >
                  <option value="automatic">Automatic</option>
                  <option value="manual">Manual</option>
                  <option value="cvt">CVT</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Fuel Type *</label>
                <select
                  value={formData.fuelType}
                  onChange={(e) => setFormData({...formData, fuelType: e.target.value})}
                  style={inputStyle}
                >
                  <option value="gasoline">Gasoline</option>
                  <option value="diesel">Diesel</option>
                  <option value="hybrid">Hybrid</option>
                  <option value="electric">Electric</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Title Status *</label>
                <select
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  style={inputStyle}
                >
                  <option value="clean">Clean</option>
                  <option value="salvage">Salvage</option>
                  <option value="rebuilt">Rebuilt</option>
                  <option value="lien">Lien</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Accident History *</label>
                <select
                  value={formData.accidents}
                  onChange={(e) => setFormData({...formData, accidents: e.target.value})}
                  style={inputStyle}
                >
                  <option value="none">No Accidents</option>
                  <option value="minor">Minor Accident</option>
                  <option value="moderate">Moderate Damage</option>
                  <option value="major">Major Accident</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Number of Owners *</label>
                <select
                  value={formData.owners}
                  onChange={(e) => setFormData({...formData, owners: e.target.value})}
                  style={inputStyle}
                >
                  <option value="1">1 Owner</option>
                  <option value="2">2 Owners</option>
                  <option value="3">3 Owners</option>
                  <option value="4+">4+ Owners</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Your Asking Price (Optional)</label>
                <input
                  type="number"
                  value={formData.askingPrice}
                  onChange={(e) => setFormData({...formData, askingPrice: e.target.value})}
                  style={inputStyle}
                  placeholder="18000"
                />
              </div>
            </div>

            <div style={{ marginTop: '20px' }}>
              <label style={labelStyle}>Description (Optional)</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                style={{ ...inputStyle, minHeight: '100px', fontFamily: 'inherit' }}
                placeholder="Add any additional details about your car (maintenance history, modifications, etc.)"
              />
            </div>
          </div>

          {/* Photos */}
          <div style={sectionStyle}>
            <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '20px' }}>
              📸 Photos
            </h2>
            <div>
              <label style={labelStyle}>Upload Photos (Recommended)</label>
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={handleFileChange}
                style={{ ...inputStyle, padding: '8px' }}
              />
              <p style={{ fontSize: '12px', color: '#6b7280', marginTop: '5px' }}>
                Upload up to 10 photos. Good photos help you get better offers!
              </p>
              {photos.length > 0 && (
                <p style={{ fontSize: '14px', color: '#10b981', marginTop: '10px' }}>
                  ✓ {photos.length} photo(s) selected
                </p>
              )}
            </div>
          </div>

          {/* Seller Information */}
          <div style={{ marginBottom: '20px' }}>
            <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '20px' }}>
              👤 Your Contact Information
            </h2>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
              <div>
                <label style={labelStyle}>Full Name *</label>
                <input
                  type="text"
                  required
                  value={formData.sellerName}
                  onChange={(e) => setFormData({...formData, sellerName: e.target.value})}
                  style={inputStyle}
                  placeholder="John Doe"
                />
              </div>

              <div>
                <label style={labelStyle}>Email *</label>
                <input
                  type="email"
                  required
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  style={inputStyle}
                  placeholder="john@example.com"
                />
              </div>

              <div>
                <label style={labelStyle}>Phone Number *</label>
                <input
                  type="tel"
                  required
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  style={inputStyle}
                  placeholder="(555) 123-4567"
                />
              </div>

              <div>
                <label style={labelStyle}>ZIP Code *</label>
                <input
                  type="text"
                  required
                  pattern="[0-9]{5}"
                  value={formData.zipCode}
                  onChange={(e) => setFormData({...formData, zipCode: e.target.value})}
                  style={inputStyle}
                  placeholder="90210"
                />
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '16px',
              backgroundColor: loading ? '#9ca3af' : '#2563eb',
              color: 'white',
              fontSize: '18px',
              fontWeight: '600',
              borderRadius: '8px',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer',
              marginTop: '20px',
            }}
          >
            {loading ? 'Submitting...' : '🚀 Get AI-Powered Offers'}
          </button>

          <p style={{ textAlign: 'center', fontSize: '12px', color: '#6b7280', marginTop: '15px' }}>
            By submitting, you agree to be contacted by verified dealers
          </p>
        </form>
      </div>
    </div>
  );
}