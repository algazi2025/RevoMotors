import React, { useEffect, useState } from 'react';

interface Filter {
  id: number;
  name: string;
  vehicle_filters: {
    makes: string[];
    models: string[];
    year_min: number | null;
    year_max: number | null;
    mileage_max: number | null;
    price_min: number | null;
    price_max: number | null;
  };
  location_filters: {
    zip_codes: string[];
    radius_miles: number;
  };
  marketplaces: {
    facebook: boolean;
    offerup: boolean;
    craigslist: boolean;
    autotrader: boolean;
    carscom: boolean;
  };
  is_active: boolean;
}

const API_BASE = 'https://revomotors.onrender.com/api/cars';

export default function DealerFilters() {
  const [filters, setFilters] = useState<Filter[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newFilter, setNewFilter] = useState({
    name: '',
    makes: [] as string[],
    models: [] as string[],
    year_min: '',
    year_max: '',
    mileage_max: '',
    price_min: '',
    price_max: '',
    zip_codes: '',
    radius_miles: 50,
    facebook: true,
    offerup: true,
    craigslist: true,
    autotrader: false,
    carscom: false,
  });

  const [allMakes, setAllMakes] = useState<string[]>([]);
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [loadingDropdowns, setLoadingDropdowns] = useState(false);
  
  const [makeSearchInput, setMakeSearchInput] = useState('');
  const [modelSearchInput, setModelSearchInput] = useState('');
  const [showMakeDropdown, setShowMakeDropdown] = useState(false);
  const [showModelDropdown, setShowModelDropdown] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('dealer_token');
    if (!token) {
      window.location.href = '/dealer/login';
      return;
    }
    
    fetchMakes();
    // fetchFilters(token);  // COMMENTED OUT - TESTING
  }, []);

  const fetchMakes = async () => {
    try {
      const response = await fetch(`${API_BASE}/makes`);
      if (response.ok) {
        const data = await response.json();
        setAllMakes(data.makes || []);
      }
    } catch (error) {
      console.error('Error fetching makes:', error);
    }
  };

  const filteredMakes = allMakes.filter(make =>
    make.toLowerCase().includes(makeSearchInput.toLowerCase())
  );

  const filteredModels = availableModels.filter(model =>
    model.toLowerCase().includes(modelSearchInput.toLowerCase())
  );

  const handleMakeToggle = async (make: string) => {
    const updatedMakes = newFilter.makes.includes(make)
      ? newFilter.makes.filter(m => m !== make)
      : [...newFilter.makes, make];
    
    setNewFilter({
      ...newFilter,
      makes: updatedMakes,
      models: [], // Clear models when make changes
    });
    
    setAvailableModels([]);
    setModelSearchInput('');

    // Fetch models for first selected make
    if (updatedMakes.length > 0) {
      setLoadingDropdowns(true);
      try {
        const response = await fetch(`${API_BASE}/models?make=${encodeURIComponent(updatedMakes[0])}`);
        if (response.ok) {
          const data = await response.json();
          setAvailableModels(data.models || []);
        }
      } catch (error) {
        console.error('Error fetching models:', error);
      } finally {
        setLoadingDropdowns(false);
      }
    }
  };

  const handleModelToggle = (model: string) => {
    const updatedModels = newFilter.models.includes(model)
      ? newFilter.models.filter(m => m !== model)
      : [...newFilter.models, model];
    setNewFilter({ ...newFilter, models: updatedModels });
  };

  const fetchFilters = async (token: string) => {
    try {
      const response = await fetch('https://revomotors.onrender.com/api/dealers/filters', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setFilters(data.filters || []);
      }
    } catch (error) {
      console.error('Error fetching filters:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateFilter = async () => {
    const token = localStorage.getItem('dealer_token');

    if (!newFilter.name.trim()) {
      alert('❌ Please give your filter a name');
      return;
    }

    if (newFilter.makes.length === 0) {
      alert('❌ Please select at least one make');
      return;
    }

    const payload = {
      name: newFilter.name,
      makes: newFilter.makes,
      models: newFilter.models,
      year_min: newFilter.year_min ? parseInt(newFilter.year_min) : null,
      year_max: newFilter.year_max ? parseInt(newFilter.year_max) : null,
      mileage_max: newFilter.mileage_max ? parseInt(newFilter.mileage_max) : null,
      price_min: newFilter.price_min ? parseFloat(newFilter.price_min) : null,
      price_max: newFilter.price_max ? parseFloat(newFilter.price_max) : null,
      zip_codes: newFilter.zip_codes ? newFilter.zip_codes.split(',').map(z => z.trim()) : [],
      radius_miles: newFilter.radius_miles,
      facebook_enabled: newFilter.facebook,
      offerup_enabled: newFilter.offerup,
      craigslist_enabled: newFilter.craigslist,
      autotrader_enabled: newFilter.autotrader,
      carscom_enabled: newFilter.carscom,
    };

    try {
      const response = await fetch('https://revomotors.onrender.com/api/dealers/filters', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        alert('✅ Filter created successfully!');
        setShowAddForm(false);
        // Reset form for next filter
        setNewFilter({
          name: '',
          makes: [],
          models: [],
          year_min: '',
          year_max: '',
          mileage_max: '',
          price_min: '',
          price_max: '',
          zip_codes: '',
          radius_miles: 50,
          facebook: true,
          offerup: true,
          craigslist: true,
          autotrader: false,
          carscom: false,
        });
        setAvailableModels([]);
        setMakeSearchInput('');
        setModelSearchInput('');
      }
    } catch (error) {
      console.error('Error creating filter:', error);
      alert('❌ Error creating filter');
    }
  };

  const handleDeleteFilter = async (filterId: number) => {
    const token = localStorage.getItem('dealer_token');
    if (!confirm('Delete this filter?')) return;

    try {
      const response = await fetch(`https://revomotors.onrender.com/api/dealers/filters/${filterId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (response.ok) {
        alert('✅ Filter deleted');
        // fetchFilters(token!);
      }
    } catch (error) {
      console.error('Error deleting filter:', error);
    }
  };

  const inputStyle = {
    width: '100%',
    padding: '10px',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '14px',
  };

  const labelStyle = {
    display: 'block' as const,
    fontWeight: '600' as const,
    marginBottom: '6px',
    fontSize: '13px',
    color: '#374151',
  };

  const dropdownContainerStyle = {
    position: 'relative' as const,
    width: '100%',
  };

  const dropdownListStyle = {
    position: 'absolute' as const,
    top: '100%',
    left: 0,
    right: 0,
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    backgroundColor: 'white',
    maxHeight: '250px',
    overflowY: 'auto' as const,
    zIndex: 1000,
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
  };

  const dropdownItemStyle = {
    padding: '10px 15px',
    cursor: 'pointer',
    borderBottom: '1px solid #f3f4f6',
    fontSize: '14px',
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui' }}>
      <header style={{ backgroundColor: 'white', borderBottom: '1px solid #e5e7eb', padding: '15px 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <a href="/dealer/dashboard" style={{ color: '#2563eb', textDecoration: 'none', fontSize: '14px', fontWeight: '500' }}>
            ← Back to Dashboard
          </a>
          <button
            onClick={() => setShowAddForm(true)}
            style={{
              padding: '10px 20px',
              backgroundColor: '#2563eb',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: '600',
              fontSize: '14px',
            }}
          >
            + Add New Filter
          </button>
        </div>
      </header>

      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '30px 20px' }}>
        {showAddForm && (
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', border: '1px solid #e5e7eb', marginBottom: '30px' }}>
            <h2 style={{ marginTop: 0, marginBottom: '25px', fontSize: '18px', fontWeight: '700' }}>Create New Filter</h2>

            {/* Filter Name */}
            <div style={{ marginBottom: '25px' }}>
              <label style={labelStyle}>Filter Name</label>
              <input
                type="text"
                value={newFilter.name}
                onChange={(e) => setNewFilter({ ...newFilter, name: e.target.value })}
                placeholder="e.g., Toyota & Honda SUVs"
                style={inputStyle}
              />
            </div>

            <div style={{ marginBottom: '25px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: '600', marginBottom: '15px', color: '#111827' }}>Vehicle Selection</h3>
              
              {/* Makes Selection */}
              <div style={{ marginBottom: '15px' }}>
                <label style={labelStyle}>Makes (select one or more)</label>
                <div style={dropdownContainerStyle}>
                  <input
                    type="text"
                    placeholder="Type to search makes..."
                    value={makeSearchInput}
                    onChange={(e) => setMakeSearchInput(e.target.value)}
                    onFocus={() => setShowMakeDropdown(true)}
                    onBlur={() => setTimeout(() => setShowMakeDropdown(false), 200)}
                    style={inputStyle}
                  />
                  
                  {showMakeDropdown && (
                    <div style={dropdownListStyle}>
                      {filteredMakes.length > 0 ? (
                        filteredMakes.map((make) => (
                          <label
                            key={make}
                            onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#f3f4f6')}
                            onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'white')}
                            style={{
                              ...dropdownItemStyle,
                              display: 'flex',
                              alignItems: 'center',
                              cursor: 'pointer',
                            }}
                          >
                            <input
                              type="checkbox"
                              checked={newFilter.makes.includes(make)}
                              onChange={() => handleMakeToggle(make)}
                              style={{ marginRight: '8px', cursor: 'pointer' }}
                            />
                            <span>{make}</span>
                          </label>
                        ))
                      ) : (
                        <div style={{ ...dropdownItemStyle, color: '#9ca3af' }}>
                          No makes found
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Selected Makes */}
                {newFilter.makes.length > 0 && (
                  <div style={{ marginTop: '10px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {newFilter.makes.map((make) => (
                      <span
                        key={make}
                        style={{
                          padding: '6px 12px',
                          backgroundColor: '#dbeafe',
                          color: '#1e40af',
                          borderRadius: '12px',
                          fontSize: '13px',
                          fontWeight: '500',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '6px',
                        }}
                      >
                        {make}
                        <button
                          onClick={() => handleMakeToggle(make)}
                          style={{
                            background: 'none',
                            border: 'none',
                            cursor: 'pointer',
                            fontSize: '16px',
                            padding: 0,
                            color: '#1e40af',
                          }}
                        >
                          ✕
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Models Selection (Optional) */}
              <div style={{ marginBottom: '15px' }}>
                <label style={labelStyle}>Models (optional - leave empty for all models)</label>
                {newFilter.makes.length > 0 ? (
                  loadingDropdowns ? (
                    <div style={{ padding: '10px', color: '#6b7280' }}>Loading models...</div>
                  ) : (
                    <>
                      <div style={dropdownContainerStyle}>
                        <input
                          type="text"
                          placeholder="Type to search models..."
                          value={modelSearchInput}
                          onChange={(e) => setModelSearchInput(e.target.value)}
                          onFocus={() => setShowModelDropdown(true)}
                          onBlur={() => setTimeout(() => setShowModelDropdown(false), 200)}
                          style={inputStyle}
                        />
                        
                        {showModelDropdown && (
                          <div style={dropdownListStyle}>
                            {filteredModels.length > 0 ? (
                              filteredModels.map((model) => (
                                <label
                                  key={model}
                                  onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = '#f3f4f6')}
                                  onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = 'white')}
                                  style={{
                                    ...dropdownItemStyle,
                                    display: 'flex',
                                    alignItems: 'center',
                                    cursor: 'pointer',
                                  }}
                                >
                                  <input
                                    type="checkbox"
                                    checked={newFilter.models.includes(model)}
                                    onChange={() => handleModelToggle(model)}
                                    style={{ marginRight: '8px', cursor: 'pointer' }}
                                  />
                                  <span>{model}</span>
                                </label>
                              ))
                            ) : (
                              <div style={{ ...dropdownItemStyle, color: '#9ca3af' }}>
                                No models found
                              </div>
                            )}
                          </div>
                        )}
                      </div>

                      {/* Selected Models */}
                      {newFilter.models.length > 0 && (
                        <div style={{ marginTop: '10px', display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                          {newFilter.models.map((model) => (
                            <span
                              key={model}
                              style={{
                                padding: '6px 12px',
                                backgroundColor: '#dbeafe',
                                color: '#1e40af',
                                borderRadius: '12px',
                                fontSize: '13px',
                                fontWeight: '500',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '6px',
                              }}
                            >
                              {model}
                              <button
                                onClick={() => handleModelToggle(model)}
                                style={{
                                  background: 'none',
                                  border: 'none',
                                  cursor: 'pointer',
                                  fontSize: '16px',
                                  padding: 0,
                                  color: '#1e40af',
                                }}
                              >
                                ✕
                              </button>
                            </span>
                          ))}
                        </div>
                      )}
                    </>
                  )
                ) : (
                  <div style={{ padding: '10px', color: '#9ca3af', fontSize: '14px' }}>Select a make first</div>
                )}
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px' }}>
                <div>
                  <label style={labelStyle}>Year Min</label>
                  <input
                    type="number"
                    value={newFilter.year_min}
                    onChange={(e) => setNewFilter({ ...newFilter, year_min: e.target.value })}
                    placeholder="e.g. 2015"
                    style={inputStyle}
                  />
                </div>
                <div>
                  <label style={labelStyle}>Year Max</label>
                  <input
                    type="number"
                    value={newFilter.year_max}
                    onChange={(e) => setNewFilter({ ...newFilter, year_max: e.target.value })}
                    placeholder="e.g. 2025"
                    style={inputStyle}
                  />
                </div>
              </div>
            </div>

            <div style={{ marginBottom: '25px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: '600', marginBottom: '15px', color: '#111827' }}>Price & Mileage</h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', marginBottom: '15px' }}>
                <div>
                  <label style={labelStyle}>Price Min ($)</label>
                  <input
                    type="number"
                    value={newFilter.price_min}
                    onChange={(e) => setNewFilter({ ...newFilter, price_min: e.target.value })}
                    placeholder="0"
                    style={inputStyle}
                  />
                </div>
                <div>
                  <label style={labelStyle}>Price Max ($)</label>
                  <input
                    type="number"
                    value={newFilter.price_max}
                    onChange={(e) => setNewFilter({ ...newFilter, price_max: e.target.value })}
                    placeholder="100000"
                    style={inputStyle}
                  />
                </div>
                <div>
                  <label style={labelStyle}>Max Mileage (mi)</label>
                  <input
                    type="number"
                    value={newFilter.mileage_max}
                    onChange={(e) => setNewFilter({ ...newFilter, mileage_max: e.target.value })}
                    placeholder="200000"
                    style={inputStyle}
                  />
                </div>
              </div>
            </div>

            <div style={{ marginBottom: '25px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: '600', marginBottom: '15px', color: '#111827' }}>Location</h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '15px', marginBottom: '15px' }}>
                <div>
                  <label style={labelStyle}>Zip Codes (comma separated)</label>
                  <input
                    type="text"
                    value={newFilter.zip_codes}
                    onChange={(e) => setNewFilter({ ...newFilter, zip_codes: e.target.value })}
                    placeholder="90210, 10001, 60601"
                    style={inputStyle}
                  />
                </div>
                <div>
                  <label style={labelStyle}>Radius (miles)</label>
                  <input
                    type="number"
                    value={newFilter.radius_miles}
                    onChange={(e) => setNewFilter({ ...newFilter, radius_miles: parseInt(e.target.value) || 50 })}
                    style={inputStyle}
                  />
                </div>
              </div>
            </div>

            <div style={{ marginBottom: '25px' }}>
              <h3 style={{ fontSize: '15px', fontWeight: '600', marginBottom: '15px', color: '#111827' }}>Monitor Marketplaces</h3>
              
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px' }}>
                <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
                  <input
                    type="checkbox"
                    checked={newFilter.facebook}
                    onChange={(e) => setNewFilter({...newFilter, facebook: e.target.checked})}
                    style={{ marginRight: '8px' }}
                  />
                  <span style={{ fontSize: '14px' }}>Facebook Marketplace</span>
                </label>
                <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
                  <input
                    type="checkbox"
                    checked={newFilter.offerup}
                    onChange={(e) => setNewFilter({...newFilter, offerup: e.target.checked})}
                    style={{ marginRight: '8px' }}
                  />
                  <span style={{ fontSize: '14px' }}>OfferUp</span>
                </label>
                <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
                  <input
                    type="checkbox"
                    checked={newFilter.craigslist}
                    onChange={(e) => setNewFilter({...newFilter, craigslist: e.target.checked})}
                    style={{ marginRight: '8px' }}
                  />
                  <span style={{ fontSize: '14px' }}>Craigslist</span>
                </label>
                <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
                  <input
                    type="checkbox"
                    checked={newFilter.autotrader}
                    onChange={(e) => setNewFilter({...newFilter, autotrader: e.target.checked})}
                    style={{ marginRight: '8px' }}
                  />
                  <span style={{ fontSize: '14px' }}>AutoTrader</span>
                </label>
                <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
                  <input
                    type="checkbox"
                    checked={newFilter.carscom}
                    onChange={(e) => setNewFilter({...newFilter, carscom: e.target.checked})}
                    style={{ marginRight: '8px' }}
                  />
                  <span style={{ fontSize: '14px' }}>Cars.com</span>
                </label>
              </div>
            </div>

            <div style={{ display: 'flex', gap: '10px' }}>
              <button
                onClick={handleCreateFilter}
                style={{
                  padding: '12px 30px',
                  backgroundColor: '#2563eb',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '600',
                  fontSize: '15px',
                }}
              >
                Create Filter
              </button>
              <button
                onClick={() => setShowAddForm(false)}
                style={{
                  padding: '12px 30px',
                  backgroundColor: '#e5e7eb',
                  color: '#374151',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '600',
                  fontSize: '15px',
                }}
              >
                Cancel
              </button>
            </div>
          </div>
        )}

        {loading ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#6b7280' }}>Loading filters...</div>
        ) : filters.length === 0 ? (
          <div style={{ backgroundColor: 'white', padding: '40px', borderRadius: '8px', border: '1px solid #e5e7eb', textAlign: 'center' }}>
            <div style={{ fontSize: '48px', marginBottom: '10px' }}>🔍</div>
            <p style={{ color: '#6b7280', marginBottom: '15px' }}>No filters set up yet</p>
            <button
              onClick={() => setShowAddForm(true)}
              style={{
                padding: '12px 24px',
                backgroundColor: '#2563eb',
                color: 'white',
                border: 'none',
                borderRadius: '6px',
                cursor: 'pointer',
                fontWeight: '600',
              }}
            >
              Create Your First Filter
            </button>
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '20px' }}>
            {filters.map((filter) => (
              <div
                key={filter.id}
                style={{
                  backgroundColor: 'white',
                  padding: '20px',
                  borderRadius: '8px',
                  border: '1px solid #e5e7eb',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '15px' }}>
                  <div>
                    <h3 style={{ margin: '0 0 5px 0', fontSize: '16px', fontWeight: '700' }}>{filter.name}</h3>
                    <span style={{
                      display: 'inline-block',
                      padding: '4px 10px',
                      backgroundColor: filter.is_active ? '#d1fae5' : '#fee2e2',
                      color: filter.is_active ? '#065f46' : '#991b1b',
                      borderRadius: '12px',
                      fontSize: '12px',
                      fontWeight: '600',
                    }}>
                      {filter.is_active ? '✓ Active' : '✕ Inactive'}
                    </span>
                  </div>
                  <button
                    onClick={() => handleDeleteFilter(filter.id)}
                    style={{
                      padding: '6px 12px',
                      backgroundColor: '#fee2e2',
                      color: '#991b1b',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '13px',
                      fontWeight: '500',
                    }}
                  >
                    Delete
                  </button>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '15px', fontSize: '14px' }}>
                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '4px' }}>Makes:</div>
                    <div style={{ fontWeight: '500' }}>
                      {filter.vehicle_filters.makes.length > 0 ? filter.vehicle_filters.makes.join(', ') : 'Any'}
                    </div>
                  </div>

                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '4px' }}>Models:</div>
                    <div style={{ fontWeight: '500' }}>
                      {filter.vehicle_filters.models.length > 0 ? filter.vehicle_filters.models.join(', ') : 'Any'}
                    </div>
                  </div>

                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '4px' }}>Year Range:</div>
                    <div style={{ fontWeight: '500' }}>
                      {filter.vehicle_filters.year_min || 'Any'} - {filter.vehicle_filters.year_max || 'Any'}
                    </div>
                  </div>

                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '4px' }}>Max Mileage:</div>
                    <div style={{ fontWeight: '500' }}>
                      {filter.vehicle_filters.mileage_max ? `${filter.vehicle_filters.mileage_max.toLocaleString()} mi` : 'Any'}
                    </div>
                  </div>

                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '4px' }}>Price Range:</div>
                    <div style={{ fontWeight: '500' }}>
                      ${filter.vehicle_filters.price_min?.toLocaleString() || 'Any'} - ${filter.vehicle_filters.price_max?.toLocaleString() || 'Any'}
                    </div>
                  </div>

                  <div>
                    <div style={{ color: '#6b7280', marginBottom: '4px' }}>Location:</div>
                    <div style={{ fontWeight: '500' }}>
                      {filter.location_filters.radius_miles} mi radius
                    </div>
                  </div>
                </div>

                <div style={{ marginTop: '15px', paddingTop: '15px', borderTop: '1px solid #e5e7eb' }}>
                  <div style={{ color: '#6b7280', marginBottom: '8px', fontSize: '13px' }}>Monitoring:</div>
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                    {filter.marketplaces.facebook && <span style={{ padding: '4px 10px', backgroundColor: '#dbeafe', color: '#1e40af', borderRadius: '12px', fontSize: '12px' }}>Facebook</span>}
                    {filter.marketplaces.offerup && <span style={{ padding: '4px 10px', backgroundColor: '#dbeafe', color: '#1e40af', borderRadius: '12px', fontSize: '12px' }}>OfferUp</span>}
                    {filter.marketplaces.craigslist && <span style={{ padding: '4px 10px', backgroundColor: '#dbeafe', color: '#1e40af', borderRadius: '12px', fontSize: '12px' }}>Craigslist</span>}
                    {filter.marketplaces.autotrader && <span style={{ padding: '4px 10px', backgroundColor: '#dbeafe', color: '#1e40af', borderRadius: '12px', fontSize: '12px' }}>AutoTrader</span>}
                    {filter.marketplaces.carscom && <span style={{ padding: '4px 10px', backgroundColor: '#dbeafe', color: '#1e40af', borderRadius: '12px', fontSize: '12px' }}>Cars.com</span>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
