import React, { useState, useEffect, useRef } from 'react';

export default function ListCar() {
  const [formData, setFormData] = useState({
    year: '', make: '', model: '', trim: '', mileage: '', condition: 'good',
    vin: '', color: '', transmission: 'automatic', fuelType: 'gasoline',
    titleStatus: 'clean', accidentHistory: 'none', numOwners: '1',
    sellerName: '', email: '', phone: '', zipCode: '', description: '', askingPrice: '',
  });

  const [trims, setTrims] = useState<string[]>([]);
  const [colors, setColors] = useState<string[]>([]);
  const [makes, setMakes] = useState<string[]>([]);
  const [models, setModels] = useState<string[]>([]);
  const [filteredMakes, setFilteredMakes] = useState<string[]>([]);
  const [filteredModels, setFilteredModels] = useState<string[]>([]);
  const [showMakeDropdown, setShowMakeDropdown] = useState(false);
  const [showModelDropdown, setShowModelDropdown] = useState(false);
  const [loading, setLoading] = useState(false);

  const API_URL = 'https://revomotors.onrender.com';

  useEffect(() => {
    fetch(`${API_URL}/api/cars/makes`).then(r => r.json()).then(setMakes).then(() => setFilteredMakes);
    fetch(`${API_URL}/api/cars/colors`).then(r => r.json()).then(setColors);
  }, []);

  useEffect(() => {
    if (formData.make) {
      fetch(`${API_URL}/api/cars/models?make=${formData.make}`).then(r => r.json()).then(data => {
        setModels(data);
        setFilteredModels(data);
      });
    }
  }, [formData.make]);

  useEffect(() => {
    if (formData.make && formData.model) {
      fetch(`${API_URL}/api/cars/trims?make=${formData.make}&model=${formData.model}`).then(r => r.json()).then(setTrims);
    }
  }, [formData.make, formData.model]);

  const handleVINDecode = async (vin: string) => {
    if (vin.length === 17) {
      const data = await fetch(`${API_URL}/api/cars/decode-vin?vin=${vin}`).then(r => r.json());
      if (data.year && data.make && data.model) {
        setFormData(prev => ({...prev, year: data.year, make: data.make, model: data.model, fuelType: data.fuelType || 'gasoline'}));
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/api/leads/webhook/lead_received`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({vin: formData.vin, year: formData.year, make: formData.make, model: formData.model, trim: formData.trim, mileage: parseInt(formData.mileage), color: formData.color, transmission: formData.transmission, fuelType: formData.fuelType, titleStatus: formData.titleStatus, accidentHistory: formData.accidentHistory, numOwners: parseInt(formData.numOwners), askingPrice: parseInt(formData.askingPrice), description: formData.description}),
      });
      if (res.ok) {
        alert('Success! Listing submitted.');
        setFormData({year: '', make: '', model: '', trim: '', mileage: '', condition: 'good', vin: '', color: '', transmission: 'automatic', fuelType: 'gasoline', titleStatus: 'clean', accidentHistory: 'none', numOwners: '1', sellerName: '', email: '', phone: '', zipCode: '', description: '', askingPrice: ''});
      }
    } catch (error) {
      alert('Error submitting. Try again.');
    } finally {
      setLoading(false);
    }
  };

  const labelStyle = {display: 'block', marginTop: '16px', marginBottom: '8px', fontWeight: '600'};
  const inputStyle = {width: '100%', padding: '12px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px'};

  return (
    <div style={{maxWidth: '900px', margin: '0 auto', padding: '24px'}}>
      <h1 style={{fontSize: '32px', fontWeight: 'bold', marginBottom: '32px'}}>🚗 Vehicle Information</h1>
      <form onSubmit={handleSubmit}>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px'}}>
          <div>
            <label style={labelStyle}>VIN</label>
            <input type="text" placeholder="KNDMC5C16J6368353" value={formData.vin} onChange={(e) => {setFormData({...formData, vin: e.target.value}); handleVINDecode(e.target.value);}} style={inputStyle} />
          </div>
          <div>
            <label style={labelStyle}>Year</label>
            <input type="text" placeholder="2018" value={formData.year} onChange={(e) => setFormData({...formData, year: e.target.value})} style={inputStyle} />
          </div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px', marginBottom: '20px'}}>
          <div>
            <label style={labelStyle}>Make</label>
            <input type="text" placeholder="Toyota" value={formData.make} onChange={(e) => {setFormData({...formData, make: e.target.value, model: '', trim: ''}); const filtered = makes.filter(m => m.toLowerCase().includes(e.target.value.toLowerCase())); setFilteredMakes(filtered); setShowMakeDropdown(true);}} style={inputStyle} autoComplete="off" />
            {showMakeDropdown && filteredMakes.length > 0 && <div style={{position: 'absolute', border: '1px solid #ddd', backgroundColor: '#fff', maxHeight: '200px', overflowY: 'auto', width: 'calc(33.33% - 14px)', zIndex: 10}}>
              {filteredMakes.map((make) => <div key={make} onClick={() => {setFormData({...formData, make, model: '', trim: ''}); setShowMakeDropdown(false);}} style={{padding: '10px', cursor: 'pointer', borderBottom: '1px solid #eee'}}>{make}</div>)}
            </div>}
          </div>
          <div>
            <label style={labelStyle}>Model</label>
            <input type="text" placeholder="Camry" value={formData.model} onChange={(e) => {setFormData({...formData, model: e.target.value, trim: ''}); const filtered = models.filter(m => m.toLowerCase().includes(e.target.value.toLowerCase())); setFilteredModels(filtered); setShowModelDropdown(true);}} disabled={!formData.make} style={inputStyle} autoComplete="off" />
            {showModelDropdown && filteredModels.length > 0 && <div style={{position: 'absolute', border: '1px solid #ddd', backgroundColor: '#fff', maxHeight: '200px', overflowY: 'auto', width: 'calc(33.33% - 14px)', zIndex: 10}}>
              {filteredModels.map((model) => <div key={model} onClick={() => {setFormData({...formData, model, trim: ''}); setShowModelDropdown(false);}} style={{padding: '10px', cursor: 'pointer', borderBottom: '1px solid #eee'}}>{model}</div>)}
            </div>}
          </div>
          <div>
            <label style={labelStyle}>Trim</label>
            <select value={formData.trim} onChange={(e) => setFormData({...formData, trim: e.target.value})} style={{...inputStyle, cursor: 'pointer'}} disabled={!formData.model || trims.length === 0}>
              <option value="">Select trim</option>
              {trims.map((trim) => <option key={trim} value={trim}>{trim}</option>)}
            </select>
          </div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px'}}>
          <div>
            <label style={labelStyle}>Mileage</label>
            <input type="number" placeholder="45000" value={formData.mileage} onChange={(e) => setFormData({...formData, mileage: e.target.value})} style={inputStyle} />
          </div>
          <div>
            <label style={labelStyle}>Color</label>
            <select value={formData.color} onChange={(e) => setFormData({...formData, color: e.target.value})} style={{...inputStyle, cursor: 'pointer'}}>
              <option value="">Select color</option>
              {colors.map((color) => <option key={color} value={color}>{color}</option>)}
            </select>
          </div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '20px'}}>
          <div>
            <label style={labelStyle}>Transmission</label>
            <select value={formData.transmission} onChange={(e) => setFormData({...formData, transmission: e.target.value})} style={{...inputStyle, cursor: 'pointer'}}>
              <option value="automatic">Automatic</option>
              <option value="manual">Manual</option>
            </select>
          </div>
          <div>
            <label style={labelStyle}>Fuel Type</label>
            <select value={formData.fuelType} onChange={(e) => setFormData({...formData, fuelType: e.target.value})} style={{...inputStyle, cursor: 'pointer'}}>
              <option value="gasoline">Gasoline</option>
              <option value="diesel">Diesel</option>
              <option value="hybrid">Hybrid</option>
              <option value="electric">Electric</option>
            </select>
          </div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr', gap: '20px', marginBottom: '20px'}}>
          <div>
            <label style={labelStyle}>Title Status</label>
            <select value={formData.titleStatus} onChange={(e) => setFormData({...formData, titleStatus: e.target.value})} style={{...inputStyle, cursor: 'pointer'}}>
              <option value="clean">Clean</option>
              <option value="salvage">Salvage</option>
            </select>
          </div>
          <div>
            <label style={labelStyle}>Accident History</label>
            <select value={formData.accidentHistory} onChange={(e) => setFormData({...formData, accidentHistory: e.target.value})} style={{...inputStyle, cursor: 'pointer'}}>
              <option value="none">None</option>
              <option value="minor">Minor</option>
              <option value="major">Major</option>
            </select>
          </div>
          <div>
            <label style={labelStyle}>Description</label>
            <textarea placeholder="Describe vehicle..." value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} style={{...inputStyle, minHeight: '120px'}} />
          </div>
          <div>
            <label style={labelStyle}>Asking Price</label>
            <input type="number" placeholder="25000" value={formData.askingPrice} onChange={(e) => setFormData({...formData, askingPrice: e.target.value})} style={inputStyle} />
          </div>
        </div>

        <button type="submit" disabled={loading} style={{width: '100%', padding: '16px', backgroundColor: '#2563eb', color: '#fff', border: 'none', borderRadius: '8px', cursor: 'pointer'}}>
          {loading ? 'Submitting...' : 'List My Car'}
        </button>
      </form>
    </div>
  );
}