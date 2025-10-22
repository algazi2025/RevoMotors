import React, { useEffect, useState } from 'react';

interface Filter {
  id: number;
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

export default function DealerFilters() {
  const [filters, setFilters] = useState<Filter[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newFilter, setNewFilter] = useState({
    makes: '',
    models: '',
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

  // Dropdown data
  const [allMakes, setAllMakes] = useState<string[]>([]);
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [availableYears, setAvailableYears] = useState<number[]>([]);
  const [selectedMakes, setSelectedMakes] = useState<string[]>([]);
  const [selectedModels, setSelectedModels] = useState<string[]>([]);

  useEffect(() => {
    const token = localStorage.getItem('dealer_token');
    if (!token) {
      window.location.href = '/dealer/login';
      return;
    }
    fetchFilters(token);
  }, []);

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
    
    const payload = {
      makes: newFilter.makes ? newFilter.makes.split(',').map(m => m.trim()) : [],
      models: newFilter.models ? newFilter.models.split(',').map(m => m.trim()) : [],
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
        fetchFilters(token!);
        // Reset form
        setNewFilter({
          makes: '', models: '', year_min: '', year_max: '', mileage_max: '',
          price_min: '', price_max: '', zip_codes: '', radius_miles: 50,
          facebook: true, offerup: true, craigslist: true, autotrader: false, carscom: false,
        });
      }
    } catch (error) {
      console.error('Error creating filter:', error);
      alert('Error creating filter');
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
        fetchFilters(token!);
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
    display: 'block',
    fontWeight: '600',
    marginBottom: '6px',
    fontSize: '13px',
    color: '#374151',
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui' }}>
      {/* Header */}
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
        <div style={{ marginBottom: '20px' }}>
          <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '8px' }}>Marketplace Filters</h1>
          <p style={{ color: '#6b7280', fontSize: '15px' }}>
            Set up filters to automatically receive leads from marketplaces when new cars matching your criteria are listed.
          </p>
        </div>

        {/* Info Box */}
        <div style={{ backgroundColor: '#eff6ff', padding: '15px', borderRadius: '8px', marginBottom: '25px', fontSize: '14px', color: '#1e40af' }}>
          <strong>🤖 AI Auto-Detection:</strong> Our AI scans Facebook Marketplace, OfferUp, Craigslist, and other platforms 24/7. When a car matching your filters is listed, you'll get a lead with an AI-generated message ready to send!
        </div>

        {/* Add Filter Form */}
        {showAddForm && (
          <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb', marginBottom: '25px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
              <h2 style={{ fontSize: '18px', fontWeight: 'bold' }}>Create New Filter</h2>
              <button
                onClick={() => setShowAddForm(false)}
                style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer', color: '#6b7280' }}
              >
                ✕
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '15px', marginBottom: '20px' }}>
              <div>
                <label style={labelStyle}>Makes (comma-separated)</label>
                <input
                  type="text"
                  value={newFilter.makes}
                  onChange={(e) => setNewFilter({...newFilter, makes: e.target.value})}
                  style={inputStyle}
                  placeholder="Honda, Toyota, Ford"
                />
              </div>

              <div>
                <label style={labelStyle}>Models (comma-separated)</label>
                <input
                  type="text"
                  value={newFilter.models}
                  onChange={(e) => setNewFilter({...newFilter, models: e.target.value})}
                  style={inputStyle}
                  placeholder="Civic, Camry, F-150"
                />
              </div>

              <div>
                <label style={labelStyle}>Year Min</label>
                <input
                  type="number"
                  value={newFilter.year_min}
                  onChange={(e) => setNewFilter({...newFilter, year_min: e.target.value})}
                  style={inputStyle}
                  placeholder="2015"
                />
              </div>

              <div>
                <label style={labelStyle}>Year Max</label>
                <input
                  type="number"
                  value={newFilter.year_max}
                  onChange={(e) => setNewFilter({...newFilter, year_max: e.target.value})}
                  style={inputStyle}
                  placeholder="2023"
                />
              </div>

              <div>
                <label style={labelStyle}>Max Mileage</label>
                <input
                  type="number"
                  value={newFilter.mileage_max}
                  onChange={(e) => setNewFilter({...newFilter, mileage_max: e.target.value})}
                  style={inputStyle}
                  placeholder="100000"
                />
              </div>

              <div>
                <label style={labelStyle}>Price Range</label>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <input
                    type="number"
                    value={newFilter.price_min}
                    onChange={(e) => setNewFilter({...newFilter, price_min: e.target.value})}
                    style={inputStyle}
                    placeholder="Min $"
                  />
                  <input
                    type="number"
                    value={newFilter.price_max}
                    onChange={(e) => setNewFilter({...newFilter, price_max: e.target.value})}
                    style={inputStyle}
                    placeholder="Max $"
                  />
                </div>
              </div>

              <div>
                <label style={labelStyle}>ZIP Codes (comma-separated)</label>
                <input
                  type="text"
                  value={newFilter.zip_codes}
                  onChange={(e) => setNewFilter({...newFilter, zip_codes: e.target.value})}
                  style={inputStyle}
                  placeholder="90210, 10001"
                />
              </div>

              <div>
                <label style={labelStyle}>Search Radius (miles)</label>
                <input
                  type="number"
                  value={newFilter.radius_miles}
                  onChange={(e) => setNewFilter({...newFilter, radius_miles: parseInt(e.target.value)})}
                  style={inputStyle}
                  placeholder="50"
                />
              </div>
            </div>

            <div style={{ marginBottom: '20px' }}>
              <label style={{ ...labelStyle, marginBottom: '12px' }}>Marketplaces to Monitor</label>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
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
          </div>
        )}

        {/* Filters List */}
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
                  <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                    <span style={{
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