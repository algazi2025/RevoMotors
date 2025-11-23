import React, { useState, useEffect, useRef } from 'react';

export default function ListCar() {
  const BACKEND_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://revomotors-backend.onrender.com';

  const [formData, setFormData] = useState({
    year: '',
    make: '',
    model: '',
    trim: '',
    mileage: '',
    condition: 'good',
    vin: '',
    color: '',
    engine: '',
    transmission: '',
    driveType: '',
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
  const [vinDecoding, setVinDecoding] = useState(false);
  
  // Dropdown state
  const [years, setYears] = useState<string[]>([]);
  const [makes, setMakes] = useState<string[]>([]);
  const [models, setModels] = useState<string[]>([]);
  const [trims, setTrims] = useState<string[]>([]);
  const [colors, setColors] = useState<string[]>([]);
  const [engines, setEngines] = useState<string[]>([]);
  const [transmissions, setTransmissions] = useState<string[]>([]);
  const [driveTypes, setDriveTypes] = useState<string[]>([]);

  // Autocomplete/filter state
  const [filteredMakes, setFilteredMakes] = useState<string[]>([]);
  const [filteredModels, setFilteredModels] = useState<string[]>([]);
  const [showMakeDropdown, setShowMakeDropdown] = useState(false);
  const [showModelDropdown, setShowModelDropdown] = useState(false);
  
  const makeRef = useRef<HTMLDivElement>(null);
  const modelRef = useRef<HTMLDivElement>(null);

  // Generate years (2000 to 2025)
  useEffect(() => {
    const currentYear = new Date().getFullYear();
    const yearList = [];
    for (let i = currentYear; i >= 2000; i--) {
      yearList.push(i.toString());
    }
    setYears(yearList);
  }, []);

  // Fetch makes when year changes
  useEffect(() => {
    if (!formData.year) return;
    
    const fetchMakes = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/api/cars/makes?year=${formData.year}`);
        if (!response.ok) throw new Error('Failed to fetch makes');
        const data = await response.json();
        setMakes(data || []);
        setFilteredMakes(data || []);
        setFormData(prev => ({ ...prev, make: '', model: '', trim: '', engines: '', transmissions: '', driveType: '' }));
      } catch (error) {
        console.error('Error fetching makes:', error);
        setMakes([]);
      }
    };
    fetchMakes();
  }, [formData.year]);

  // Fetch models when make changes
  useEffect(() => {
    if (!formData.make || !formData.year) return;
    
    const fetchModels = async () => {
      try {
        const response = await fetch(`${BACKEND_URL}/api/cars/models?make=${formData.make}&year=${formData.year}`);
        if (!response.ok) throw new Error('Failed to fetch models');
        const data = await response.json();
        setModels(data || []);
        setFilteredModels(data || []);
        setFormData(prev => ({ ...prev, model: '', trim: '', engine: '', transmission: '', driveType: '' }));
      } catch (error) {
        console.error('Error fetching models:', error);
        setModels([]);
      }
    };
    fetchModels();
  }, [formData.make, formData.year]);

  // Fetch trims, colors, engines, transmissions, drive types when model changes
  useEffect(() => {
    if (!formData.model || !formData.make || !formData.year) return;

    const fetchCarDetails = async () => {
      try {
        const [trimsRes, enginesRes, transRes, driveRes, colorRes] = await Promise.all([
          fetch(`${BACKEND_URL}/api/cars/trims?make=${formData.make}&model=${formData.model}&year=${formData.year}`),
          fetch(`${BACKEND_URL}/api/cars/engines?make=${formData.make}&model=${formData.model}&year=${formData.year}`),
          fetch(`${BACKEND_URL}/api/cars/transmissions?make=${formData.make}&model=${formData.model}&year=${formData.year}`),
          fetch(`${BACKEND_URL}/api/cars/drivetypes?make=${formData.make}&model=${formData.model}&year=${formData.year}`),
          fetch(`${BACKEND_URL}/api/cars/colors`),
        ]);

        const trimsData = await trimsRes.json();
        const enginesData = await enginesRes.json();
        const transData = await transRes.json();
        const driveData = await driveRes.json();
        const colorData = await colorRes.json();

        setTrims(trimsData || []);
        setEngines(enginesData || []);
        setTransmissions(transData || []);
        setDriveTypes(driveData || []);
        setColors(colorData || []);
      } catch (error) {
        console.error('Error fetching car details:', error);
      }
    };

    fetchCarDetails();
  }, [formData.model, formData.make, formData.year]);

  // VIN Decoder
  const handleVinChange = async (vin: string) => {
    const vinUpper = vin.toUpperCase();
    setFormData(prev => ({ ...prev, vin: vinUpper }));

    if (vinUpper.length === 17) {
      setVinDecoding(true);
      try {
        const response = await fetch(`${BACKEND_URL}/api/cars/decode-vin?vin=${vinUpper}`);
        const data = await response.json();

        console.log('[VIN Decoder] Response:', data);

        if (data.error) {
          console.error('VIN Error:', data.error);
        } else {
          console.log('[VIN Decoder] Got data:', {
            year: data.year,
            make: data.make,
            model: data.model,
            fuelType: data.fuelType
          });

          // Auto-populate form with decoded VIN data
          const newFormData = {
            year: data.year || '',
            make: data.make || '',
            model: data.model || '',
            fuelType: (data.fuelType || 'gasoline').toLowerCase(),
            vin: vinUpper,
          };

          console.log('[VIN Decoder] Setting form data:', newFormData);
          setFormData(prev => ({ ...prev, ...newFormData }));
        }
      } catch (error) {
        console.error('Error decoding VIN:', error);
      } finally {
        setVinDecoding(false);
      }
    }
  };

  // Handle make input for autocomplete
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

  // Handle model input for autocomplete
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

  // Close dropdowns on click outside
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
        vin: formData.vin,
        year: formData.year,
        make: formData.make,
        model: formData.model,
        trim: formData.trim,
        mileage: parseInt(formData.mileage),
        color: formData.color,
        transmission: formData.transmission,
        fuelType: formData.fuelType,
        titleStatus: formData.title,
        accidentHistory: formData.accidents,
        askingPrice: formData.askingPrice ? parseFloat(formData.askingPrice) : null,
        description: formData.description,
      };

      const response = await fetch(`${BACKEND_URL}/api/leads/webhook/lead_received`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (data.success) {
        alert(
          `✅ Success! Your car has been listed.\n\n` +
          `Listing ID: ${data.listing_id}\n` +
          `AI Fair Offer: $${data.ai_draft_offer?.fair || 'N/A'}\n` +
          `Price Range: $${data.ai_draft_offer?.low || 'N/A'} - $${data.ai_draft_offer?.max || 'N/A'}\n\n` +
          `Dealers will contact you soon!`
        );
        
        setFormData({
          year: '', make: '', model: '', trim: '', mileage: '', condition: 'good',
          vin: '', color: '', engine: '', transmission: '', driveType: '', fuelType: 'gasoline',
          title: 'clean', accidents: 'none', owners: '1',
          sellerName: '', email: '', phone: '', zipCode: '',
          description: '', askingPrice: '',
        });
        setPhotos([]);
      } else {
        alert(`Error: ${data.errors ? JSON.stringify(data.errors) : data.error || 'Failed to submit listing'}`);
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

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: '0 auto' }}>
      <h1 style={{ marginBottom: '10px', fontSize: '28px', fontWeight: '700' }}>📋 List Your Car</h1>
      <p style={{ color: '#6b7280', marginBottom: '30px' }}>Complete the form to list your vehicle on RevoMotors</p>

      <form onSubmit={handleSubmit}>
        {/* Car Information */}
        <div style={sectionStyle}>
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '20px' }}>🚗 Car Information</h2>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
            {/* Year */}
            <div>
              <label style={labelStyle}>Year *</label>
              <select
                required
                value={formData.year}
                onChange={(e) => setFormData({...formData, year: e.target.value})}
                style={inputStyle}
              >
                <option value="">Select Year</option>
                {years.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
            </div>

            {/* Make */}
            <div ref={makeRef} style={{ position: 'relative' as const }}>
              <label style={labelStyle}>Make *</label>
              <input
                type="text"
                required
                value={formData.make}
                onChange={(e) => handleMakeInput(e.target.value)}
                onFocus={() => setShowMakeDropdown(true)}
                style={inputStyle}
                placeholder="Select or type Make"
              />
              {showMakeDropdown && filteredMakes.length > 0 && (
                <div style={dropdownStyle}>
                  {filteredMakes.map((make, idx) => (
                    <div
                      key={idx}
                      onClick={() => {
                        setFormData({...formData, make});
                        setShowMakeDropdown(false);
                      }}
                      style={{
                        padding: '10px 12px',
                        cursor: 'pointer',
                        borderBottom: '1px solid #f3f4f6',
                        transition: 'background-color 0.2s',
                      }}
                      onMouseEnter={(e) => {e.currentTarget.style.backgroundColor = '#f3f4f6';}}
                      onMouseLeave={(e) => {e.currentTarget.style.backgroundColor = 'transparent';}}
                    >
                      {make}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Model */}
            <div ref={modelRef} style={{ position: 'relative' as const }}>
              <label style={labelStyle}>Model *</label>
              <input
                type="text"
                required
                value={formData.model}
                onChange={(e) => handleModelInput(e.target.value)}
                onFocus={() => setShowModelDropdown(true)}
                style={inputStyle}
                placeholder="Select or type Model"
              />
              {showModelDropdown && filteredModels.length > 0 && (
                <div style={dropdownStyle}>
                  {filteredModels.map((model, idx) => (
                    <div
                      key={idx}
                      onClick={() => {
                        setFormData({...formData, model});
                        setShowModelDropdown(false);
                      }}
                      style={{
                        padding: '10px 12px',
                        cursor: 'pointer',
                        borderBottom: '1px solid #f3f4f6',
                        transition: 'background-color 0.2s',
                      }}
                      onMouseEnter={(e) => {e.currentTarget.style.backgroundColor = '#f3f4f6';}}
                      onMouseLeave={(e) => {e.currentTarget.style.backgroundColor = 'transparent';}}
                    >
                      {model}
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Trim */}
            <div>
              <label style={labelStyle}>Trim</label>
              <select
                value={formData.trim}
                onChange={(e) => setFormData({...formData, trim: e.target.value})}
                style={inputStyle}
              >
                <option value="">Select Trim</option>
                {trims.map((trim, idx) => (
                  <option key={idx} value={trim}>{trim}</option>
                ))}
              </select>
            </div>

            {/* Mileage */}
            <div>
              <label style={labelStyle}>Mileage *</label>
              <input
                type="number"
                required
                value={formData.mileage}
                onChange={(e) => setFormData({...formData, mileage: e.target.value})}
                style={inputStyle}
                placeholder="45000"
                min="0"
                max="999999"
              />
            </div>

            {/* VIN - WITH DECODER */}
            <div>
              <label style={labelStyle}>VIN Number * {vinDecoding && <span style={{color: '#2563eb'}}>🔍 Decoding...</span>}</label>
              <input
                type="text"
                required
                minLength={17}
                maxLength={17}
                value={formData.vin}
                onChange={(e) => handleVinChange(e.target.value)}
                style={inputStyle}
                placeholder="1HGBH41JXMN109186"
              />
              <p style={{fontSize: '12px', color: '#6b7280', marginTop: '4px'}}>Enter VIN to auto-populate vehicle info</p>
            </div>

            {/* Color */}
            <div>
              <label style={labelStyle}>Color</label>
              <select
                value={formData.color}
                onChange={(e) => setFormData({...formData, color: e.target.value})}
                style={inputStyle}
              >
                <option value="">Select Color</option>
                {colors.map((color, idx) => (
                  <option key={idx} value={color}>{color}</option>
                ))}
              </select>
            </div>

            {/* Engine */}
            <div>
              <label style={labelStyle}>Engine</label>
              <select
                value={formData.engine}
                onChange={(e) => setFormData({...formData, engine: e.target.value})}
                style={inputStyle}
              >
                <option value="">Select Engine</option>
                {engines.map((engine, idx) => (
                  <option key={idx} value={engine}>{engine}</option>
                ))}
              </select>
            </div>

            {/* Transmission */}
            <div>
              <label style={labelStyle}>Transmission</label>
              <select
                value={formData.transmission}
                onChange={(e) => setFormData({...formData, transmission: e.target.value})}
                style={inputStyle}
              >
                <option value="">Select Transmission</option>
                {transmissions.map((trans, idx) => (
                  <option key={idx} value={trans}>{trans}</option>
                ))}
              </select>
            </div>

            {/* Drive Type - NEW */}
            <div>
              <label style={labelStyle}>Drive Type</label>
              <select
                value={formData.driveType}
                onChange={(e) => setFormData({...formData, driveType: e.target.value})}
                style={inputStyle}
              >
                <option value="">Select Drive Type</option>
                {driveTypes.map((drive, idx) => (
                  <option key={idx} value={drive}>{drive}</option>
                ))}
              </select>
            </div>

            {/* Fuel Type */}
            <div>
              <label style={labelStyle}>Fuel Type</label>
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

            {/* Condition */}
            <div>
              <label style={labelStyle}>Condition</label>
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

            {/* Title Status */}
            <div>
              <label style={labelStyle}>Title Status</label>
              <select
                value={formData.title}
                onChange={(e) => setFormData({...formData, title: e.target.value})}
                style={inputStyle}
              >
                <option value="clean">Clean</option>
                <option value="salvage">Salvage</option>
                <option value="rebuilt">Rebuilt</option>
              </select>
            </div>

            {/* Accident History */}
            <div>
              <label style={labelStyle}>Accident History</label>
              <select
                value={formData.accidents}
                onChange={(e) => setFormData({...formData, accidents: e.target.value})}
                style={inputStyle}
              >
                <option value="none">None</option>
                <option value="minor">Minor</option>
                <option value="major">Major</option>
              </select>
            </div>

            {/* Number of Owners */}
            <div>
              <label style={labelStyle}>Number of Owners</label>
              <select
                value={formData.owners}
                onChange={(e) => setFormData({...formData, owners: e.target.value})}
                style={inputStyle}
              >
                <option value="1">1</option>
                <option value="2">2</option>
                <option value="3+">3+</option>
              </select>
            </div>

            {/* Asking Price */}
            <div>
              <label style={labelStyle}>Asking Price ($)</label>
              <input
                type="number"
                value={formData.askingPrice}
                onChange={(e) => setFormData({...formData, askingPrice: e.target.value})}
                style={inputStyle}
                placeholder="25000"
                min="1"
                max="999999"
              />
            </div>
          </div>

          {/* Description */}
          <div style={{ marginTop: '20px' }}>
            <label style={labelStyle}>Description</label>
            <textarea
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
              style={{...inputStyle, minHeight: '100px', fontFamily: 'system-ui'}}
              placeholder="Describe the condition, features, maintenance history..."
            />
          </div>

          {/* Photos */}
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
          <h2 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '20px' }}>👤 Seller Information</h2>

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
  );
}
