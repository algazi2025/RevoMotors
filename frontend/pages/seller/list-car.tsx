import React, { useState, useEffect } from 'react';

export default function ListCar() {
  const [form, setForm] = useState({year: '', make: '', model: '', trim: '', mileage: '', color: '', transmission: 'automatic', fuelType: 'gasoline', titleStatus: 'clean', accidentHistory: 'none', numOwners: '1', description: '', askingPrice: ''});
  const [trims, setTrims] = useState<string[]>([]);
  const [colors, setColors] = useState<string[]>([]);
  const [makes, setMakes] = useState<string[]>([]);
  const [models, setModels] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const API = 'https://revomotors.onrender.com';
  const YEARS = Array.from({length: 36}, (_, i) => (2025 - i).toString());

  useEffect(() => {
    fetch(`${API}/api/cars/makes`).then(r => r.json()).then(d => setMakes(d || [])).catch(() => {});
    fetch(`${API}/api/cars/colors`).then(r => r.json()).then(d => setColors(d || [])).catch(() => {});
  }, []);

  useEffect(() => {
    if (!form.make) {setModels([]); return;}
    fetch(`${API}/api/cars/models?make=${form.make}`).then(r => r.json()).then(d => setModels(d || [])).catch(() => {});
  }, [form.make]);

  useEffect(() => {
    if (!form.make || !form.model) {setTrims([]); return;}
    fetch(`${API}/api/cars/trims?make=${form.make}&model=${form.model}`).then(r => r.json()).then(d => setTrims(d || [])).catch(() => {});
  }, [form.make, form.model]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/leads/webhook/lead_received`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({vin: '', year: form.year, make: form.make, model: form.model, trim: form.trim, mileage: parseInt(form.mileage) || 0, color: form.color, transmission: form.transmission, fuelType: form.fuelType, titleStatus: form.titleStatus, accidentHistory: form.accidentHistory, numOwners: parseInt(form.numOwners) || 1, askingPrice: parseInt(form.askingPrice) || 0, description: form.description}),
      });
      const result = await res.json();
      if (result.success) {
        alert('✓ Success! ID: ' + result.listing_id);
        setForm({year: '', make: '', model: '', trim: '', mileage: '', color: '', transmission: 'automatic', fuelType: 'gasoline', titleStatus: 'clean', accidentHistory: 'none', numOwners: '1', description: '', askingPrice: ''});
      } else {
        alert('Error: ' + (result.error || 'Failed'));
      }
    } catch (e) {
      alert('Error submitting');
    } finally {
      setLoading(false);
    }
  };

  const st = {l: {display: 'block', marginBottom: '6px', fontWeight: '600', fontSize: '14px'}, i: {width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' as const, cursor: 'pointer'}};

  return (
    <div style={{maxWidth: '900px', margin: '0 auto', padding: '24px', fontFamily: 'Arial'}}>
      <h1 style={{fontSize: '32px', marginBottom: '32px'}}>🚗 Vehicle Information</h1>
      <form onSubmit={handleSubmit} style={{display: 'flex', flexDirection: 'column', gap: '20px'}}>
        
        {/* Year - First step */}
        <div>
          <label style={st.l}>Year *</label>
          <select style={st.i} value={form.year} onChange={(e) => setForm({...form, year: e.target.value, make: '', model: '', trim: ''})}>
            <option value="">Select year</option>
            {YEARS.map(y => <option key={y}>{y}</option>)}
          </select>
        </div>

        {/* Make - Only available if year selected */}
        <div>
          <label style={st.l}>Make *</label>
          <select style={st.i} value={form.make} onChange={(e) => setForm({...form, make: e.target.value, model: '', trim: ''})} disabled={!form.year}>
            <option value="">Select make</option>
            {makes.map(m => <option key={m}>{m}</option>)}
          </select>
        </div>

        {/* Model - Only available if make selected */}
        <div>
          <label style={st.l}>Model *</label>
          <select style={st.i} value={form.model} onChange={(e) => setForm({...form, model: e.target.value, trim: ''})} disabled={!form.make}>
            <option value="">Select model</option>
            {models.map(m => <option key={m}>{m}</option>)}
          </select>
        </div>

        {/* Trim - Only available if model selected */}
        <div>
          <label style={st.l}>Trim</label>
          <select style={st.i} value={form.trim} onChange={(e) => setForm({...form, trim: e.target.value})} disabled={!form.model}>
            <option value="">Select trim</option>
            {trims.map(t => <option key={t}>{t}</option>)}
          </select>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          {/* Mileage */}
          <div>
            <label style={st.l}>Mileage</label>
            <input style={{...st.i, cursor: 'text'}} type="number" value={form.mileage} onChange={(e) => setForm({...form, mileage: e.target.value})} />
          </div>

          {/* Color - Dropdown */}
          <div>
            <label style={st.l}>Color</label>
            <select style={st.i} value={form.color} onChange={(e) => setForm({...form, color: e.target.value})}>
              <option value="">Select color</option>
              {colors.map(c => <option key={c}>{c}</option>)}
            </select>
          </div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          {/* Transmission */}
          <div>
            <label style={st.l}>Transmission</label>
            <select style={st.i} value={form.transmission} onChange={(e) => setForm({...form, transmission: e.target.value})}>
              <option value="automatic">Automatic</option>
              <option value="manual">Manual</option>
              <option value="cvt">CVT</option>
            </select>
          </div>

          {/* Fuel Type - Dropdown */}
          <div>
            <label style={st.l}>Fuel Type</label>
            <select style={st.i} value={form.fuelType} onChange={(e) => setForm({...form, fuelType: e.target.value})}>
              <option value="gasoline">Gasoline</option>
              <option value="diesel">Diesel</option>
              <option value="hybrid">Hybrid</option>
              <option value="electric">Electric</option>
            </select>
          </div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          {/* Title Status */}
          <div>
            <label style={st.l}>Title Status</label>
            <select style={st.i} value={form.titleStatus} onChange={(e) => setForm({...form, titleStatus: e.target.value})}>
              <option value="clean">Clean</option>
              <option value="salvage">Salvage</option>
              <option value="branded">Branded</option>
            </select>
          </div>

          {/* Accident History */}
          <div>
            <label style={st.l}>Accident History</label>
            <select style={st.i} value={form.accidentHistory} onChange={(e) => setForm({...form, accidentHistory: e.target.value})}>
              <option value="none">None</option>
              <option value="minor">Minor</option>
              <option value="major">Major</option>
            </select>
          </div>
        </div>

        {/* Description */}
        <div>
          <label style={st.l}>Description</label>
          <textarea style={{...st.i, cursor: 'text', minHeight: '100px'}} value={form.description} onChange={(e) => setForm({...form, description: e.target.value})} />
        </div>

        {/* Asking Price */}
        <div>
          <label style={st.l}>Asking Price ($)</label>
          <input style={{...st.i, cursor: 'text'}} type="number" value={form.askingPrice} onChange={(e) => setForm({...form, askingPrice: e.target.value})} />
        </div>

        <button style={{padding: '12px', backgroundColor: '#2563eb', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold', fontSize: '16px'}} type="submit" disabled={loading || !form.year || !form.make || !form.model}>
          {loading ? 'Submitting...' : 'List My Car'}
        </button>
      </form>
    </div>
  );
}
