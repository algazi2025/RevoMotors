import React, { useState, useEffect, useRef } from 'react';

export default function ListCar() {
  const [formData, setFormData] = useState({
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
    sellerName: '',
    email: '',
    phone: '',
    zipCode: '',
    description: '',
    askingPrice: '',
  });

  const [photos, setPhotos] = useState<File[]>([]);
  const [loading, setLoading] = useState(false);
  
  // Autocomplete state
  const [makes, setMakes] = useState<string[]>([]);
  const [models, setModels] = useState<string[]>([]);
  const [filteredMakes, setFilteredMakes] = useState<string[]>([]);
  const [filteredModels, setFilteredModels] = useState<string[]>([]);
  const [showMakeDropdown, setShowMakeDropdown] = useState(false);
  const [showModelDropdown, setShowModelDropdown] = useState(false);
  
  const makeRef = useRef<HTMLDivElement>(null);
  const modelRef = useRef<HTMLDivElement>(null);

  // Fetch makes on mount
  useEffect(() => {
    const fetchMakes = async () => {
      try {
        const response = await fetch('https://revomotors-api.onrender.com/api/cars/makes');
        if (!response.ok) throw new Error('Failed to fetch makes');
        const data = await response.json();
        setMakes(data);
        setFilteredMakes(data);
      } catch (error) {
        console.error('Error fetching makes:', error);
      }
    };
    fetchMakes();
  }, []);

  // Fetch models when make changes
  useEffect(() => {
    if (formData.make) {
      const fetchModels = async () => {
        try {
          const response = await fetch(`https://revomotors-api.onrender.com/api/cars/models?make=${formData.make}`);
          if (!response.ok) throw new Error('Failed to fetch models');
          const data = await response.json();
          setModels(data);
          setFilteredModels(data);
        } catch (error) {
          console.error('Error fetching models:', error);
        }
      };
      fetchModels();
    } else {
      setModels([]);
      setFilteredModels([]);
    }
  }, [formData.make]);

  // Handle make input
  const handleMakeInput = (value: string) => {
    setFormData({...formData, make: value, model: ''});
    
    if (value.length > 0) {
      const filtered = makes.filter(m => m.toLowerCase().includes(value.toLowerCase()));
      setFilteredMakes(filtered);
      setShowMakeDropdown(true);
    } else {
      setFilteredMakes(makes);
      setShowMakeDropdown(false);
    }
  };

  // Handle model input
  const handleModelInput = (value: string) => {
    setFormData({...formData, model: value});
    
    if (value.length > 0 && formData.make) {
      const filtered = models.filter(m => m.toLowerCase().includes(value.toLowerCase()));
      setFilteredModels(filtered);
      setShowModelDropdown(true);
    } else {
      setFilteredModels(models);
      setShowModelDropdown(false);
    }
  };

  // Click outside to close dropdowns
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (makeRef.current && !makeRef.current.contains(event.target as Node)) {
        setShowMakeDropdown(false);
      }
      if (modelRef.current && !modelRef.current.contains(event.target as Node)) {
        setShowModelDropdown(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setPhotos(Array.from(e.target.files));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
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
        seller_contact_name: formData.sellerName,
        seller_contact_email: formData.email,
        seller_contact_phone: formData.phone,
        photos: photoUrls,
      };

      const response = await fetch('https://revomotors-api.onrender.com/api/leads/webhook/lead_received', {
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
    display: 'block' as const,
    fontWeight: '500' as const,
    marginBottom: '8px',
    fontSize: '14px',
  };

  const sectionStyle = {
    marginBottom: '30px',
    paddingBottom: '20px',
    borderBottom: '1px solid #e5e7eb',
  };

  const dropdownStyle = {
    position: 'absolute' as const,
    top: '100%',
    left: 0,
    right: 0,
    backgroundColor: 'white',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    maxHeight: '250px',
    overflowY: 'auto' as const,
    zIndex: 10,
    marginTop: '4px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  };

  const optionStyle = {
    padding: '10px 12px',
    cursor: 'pointer',
    borderBottom: '1px solid #f3f4f6',
    transition: 'background-color 0.2s',
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

              {/* Make Dropdown */}
              <div style={{ position: 'relative' }} ref={makeRef}>
                <label style={labelStyle}>Make *</label>
                <input
                  type="text"
                  required
                  value={formData.make}
                  onChange={(e) => handleMakeInput(e.target.value)}
                  onFocus={() => {
                    setShowMakeDropdown(true);
                    if (formData.make === '') {
                      setFilteredMakes(makes);
                    }
                  }}
                  style={inputStyle}
                  placeholder="Click to select or type..."
                />
                {showMakeDropdown && filteredMakes.length > 0 && (
                  <div style={dropdownStyle}>
                    {filteredMakes.map((make) => (
                      <div
                        key={make}
                        onClick={() => {
                          setFormData({...formData, make, model: ''});
                          setShowMakeDropdown(false);
                        }}
                        onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#f3f4f6')}
                        onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'white')}
                        style={optionStyle}
                      >
                        {make}
                      </div>
                    ))}
                  </div>
                )}
              </div>

              {/* Model Dropdown */}
              <div style={{ position: 'relative' }} ref={modelRef}>
                <label style={labelStyle}>Model *</label>
                <input
                  type="text"
                  required
                  disabled={!formData.make}
                  value={formData.model}
                  onChange={(e) => handleModelInput(e.target.value)}
                  onFocus={() => {
                    if (formData.make) {
                      setShowModelDropdown(true);
                      if (formData.model === '') {
                        setFilteredModels(models);
                      }
                    }
                  }}
                  style={{
                    ...inputStyle,
                    backgroundColor: !formData.make ? '#f3f4f6' : 'white',
                    cursor: !formData.make ? 'not-allowed' : 'text',
                  }}
                  placeholder={formData.make ? 'Click to select or type...' : 'Select make first'}
                />
                {showModelDropdown && formData.make && filteredModels.length > 0 && (
                  <div style={dropdownStyle}>
                    {filteredModels.map((model) => (
                      <div
                        key={model}
                        onClick={() => {
                          setFormData({...formData, model});
                          setShowModelDropdown(false);
                        }}
                        onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#f3f4f6')}
                        onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'white')}
                        style={optionStyle}
                      >
                        {model}
                      </div>
                    ))}
                  </div>
                )}
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
                <label style={labelStyle}>Condition</label>
                <select
                  value={formData.condition}
                  onChange={(e) => setFormData({...formData, condition: e.target.value})}
                  style={inputStyle}
                >
                  <option>excellent</option>
                  <option>good</option>
                  <option>fair</option>
                  <option>poor</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Transmission</label>
                <select
                  value={formData.transmission}
                  onChange={(e) => setFormData({...formData, transmission: e.target.value})}
                  style={inputStyle}
                >
                  <option>automatic</option>
                  <option>manual</option>
                  <option>cvt</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Fuel Type</label>
                <select
                  value={formData.fuelType}
                  onChange={(e) => setFormData({...formData, fuelType: e.target.value})}
                  style={inputStyle}
                >
                  <option>gasoline</option>
                  <option>diesel</option>
                  <option>hybrid</option>
                  <option>electric</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Title Status</label>
                <select
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                  style={inputStyle}
                >
                  <option>clean</option>
                  <option>salvage</option>
                  <option>rebuilt</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Accident History</label>
                <select
                  value={formData.accidents}
                  onChange={(e) => setFormData({...formData, accidents: e.target.value})}
                  style={inputStyle}
                >
                  <option>none</option>
                  <option>minor</option>
                  <option>major</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Number of Owners</label>
                <select
                  value={formData.owners}
                  onChange={(e) => setFormData({...formData, owners: e.target.value})}
                  style={inputStyle}
                >
                  <option>1</option>
                  <option>2</option>
                  <option>3+</option>
                </select>
              </div>

              <div>
                <label style={labelStyle}>Asking Price ($)</label>
                <input
                  type="number"
                  value={formData.askingPrice}
                  onChange={(e) => setFormData({...formData, askingPrice: e.target.value})}
                  style={inputStyle}
                  placeholder="25000"
                />
              </div>
            </div>

            <div style={{ marginTop: '20px' }}>
              <label style={labelStyle}>Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                style={{...inputStyle, minHeight: '100px', fontFamily: 'system-ui'}}
                placeholder="Describe the condition, features, maintenance history..."
              />
            </div>

            <div style={{ marginTop: '20px' }}>
              <label style={labelStyle}>Photos</label>
              <input
                type="file"
                multiple
                accept="image/*"
                onChange={handleFileChange}
                style={{...inputStyle, padding: '8px'}}
              />
              {photos.length > 0 && (
                <p style={{ color: '#059669', marginTop: '8px' }}>
                  ✓ {photos.length} photo(s) selected
                </p>
              )}
            </div>
          </div>

          {/* Seller Information */}
          <div style={sectionStyle}>
            <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '20px' }}>
              👤 Seller Information
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
                <label style={labelStyle}>Phone *</label>
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
                <label style={labelStyle}>Zip Code *</label>
                <input
                  type="text"
                  required
                  value={formData.zipCode}
                  onChange={(e) => setFormData({...formData, zipCode: e.target.value})}
                  style={inputStyle}
                  placeholder="95814"
                />
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '14px',
              backgroundColor: loading ? '#9ca3af' : '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              fontSize: '16px',
              fontWeight: '600',
              cursor: loading ? 'not-allowed' : 'pointer',
            }}
          >
            {loading ? 'Listing Your Car...' : '✓ List My Car'}
          </button>
        </form>
      </div>
    </div>
  );
}
