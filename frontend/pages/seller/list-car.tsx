import React, { useState, useEffect } from 'react';

export default function ListCar() {
  const [form, setForm] = useState({vin: '', year: '', make: '', model: '', trim: '', mileage: '', color: '', transmission: 'automatic', fuelType: 'gasoline', titleStatus: 'clean', accidentHistory: 'none', description: '', askingPrice: ''});
  const [trims, setTrims] = useState<string[]>([]);
  const [colors, setColors] = useState<string[]>([]);
  const [makes, setMakes] = useState<string[]>([]);
  const [models, setModels] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [vinDecoded, setVinDecoded] = useState(false);
  const [validationError, setValidationError] = useState('');

  const API = 'https://revomotors.onrender.com';
  const YEARS = Array.from({length: 36}, (_, i) => (2025 - i).toString());

  useEffect(() => {
    fetch(`${API}/api/cars/colors`).then(r => r.json()).then(d => setColors(d || [])).catch(() => setColors([]));
  }, []);

  useEffect(() => {
    if (!form.year) {setMakes([]); setForm(prev => ({...prev, make: '', model: '', trim: ''})); return;}
    fetch(`${API}/api/cars/makes?year=${form.year}`).then(r => r.json()).then(d => setMakes(d || [])).catch(() => setMakes([]));
  }, [form.year]);

  useEffect(() => {
    if (!form.make || !form.year) {setModels([]); setForm(prev => ({...prev, model: '', trim: ''})); return;}
    fetch(`${API}/api/cars/models?make=${form.make}&year=${form.year}`).then(r => r.json()).then(d => setModels(d || [])).catch(() => setModels([]));
  }, [form.make, form.year]);

  useEffect(() => {
    if (!form.make || !form.model || !form.year) {setTrims([]); return;}
    fetch(`${API}/api/cars/trims?make=${form.make}&model=${form.model}&year=${form.year}`).then(r => r.json()).then(d => setTrims(d || [])).catch(() => setTrims([]));
  }, [form.make, form.model, form.year]);

  const handleVINBlur = async (vin: string) => {
    if (vin.length !== 17) {setVinDecoded(false); return;}
    try {
      const res = await fetch(`${API}/api/cars/decode-vin?vin=${vin}`);
      const data = await res.json();
      if (data.Make && data.model && data.year) {
        setForm(prev => ({...prev, year: data.year, make: data.Make, model: data.model, fuelType: data.fuelType || 'gasoline'}));
        setVinDecoded(true);
      } else {
        setVinDecoded(false);
      }
    } catch (e) {
      setVinDecoded(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!form.year) {
      setValidationError('❌ Year is required');
      return;
    }
    if (!form.make) {
      setValidationError('❌ Make is required');
      return;
    }
    if (!form.model) {
      setValidationError('❌ Model is required - no models available for this Make/Year combination');
      return;
    }
    
    setValidationError('');
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/leads/webhook/lead_received`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({vin: form.vin, year: form.year, make: form.make, model: form.model, trim: form.trim, mileage: parseInt(form.mileage) || 0, color: form.color, transmission: form.transmission, fuelType: form.fuelType, titleStatus: form.titleStatus, accidentHistory: form.accidentHistory, askingPrice: parseInt(form.askingPrice) || 0, description: form.description}),
      });
      const result = await res.json();
      if (result.success) {
        alert('✓ Success! ID: ' + result.listing_id);
        setForm({vin: '', year: '', make: '', model: '', trim: '', mileage: '', color: '', transmission: 'automatic', fuelType: 'gasoline', titleStatus: 'clean', accidentHistory: 'none', description: '', askingPrice: ''});
        setVinDecoded(false);
        setValidationError('');
      } else {
        setValidationError('❌ ' + (result.error || 'Failed to submit'));
      }
    } catch (e) {
      setValidationError('❌ Error submitting form');
    } finally {
      setLoading(false);
    }
  };

  const st = {l: {display: 'block', marginBottom: '6px', fontWeight: '600', fontSize: '14px'}, i: {width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' as const}};

  return (
    <div style={{maxWidth: '900px', margin: '0 auto', padding: '24px', fontFamily: 'Arial'}}>
      <h1 style={{fontSize: '32px', marginBottom: '32px'}}>🚗 Vehicle Information</h1>
      
      {validationError && (
        <div style={{backgroundColor: '#ffe6e6', color: '#cc0000', padding: '12px', borderRadius: '4px', marginBottom: '20px', fontWeight: 'bold'}}>
          {validationError}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{display: 'flex', flexDirection: 'column', gap: '20px'}}>
        
        <div>
          <label style={st.l}>VIN Number</label>
          <input style={{...st.i, cursor: 'text'}} type="text" value={form.vin} onChange={(e) => {setForm({...form, vin: e.target.value}); setVinDecoded(false);}} onBlur={(e) => handleVINBlur(e.target.value)} />
          {vinDecoded && <p style={{color: 'green', fontSize: '12px', marginTop: '4px'}}>✓ VIN Decoded</p>}
        </div>

        <div>
          <label style={st.l}>Year *</label>
          {vinDecoded ? (
            <div style={{...st.i, backgroundColor: '#f0f0f0', display: 'flex', alignItems: 'center'}}>
              {form.year} <span style={{color: 'green', marginLeft: '8px', fontSize: '12px'}}>✓ Locked</span>
            </div>
          ) : (
            <select style={st.i} value={form.year} onChange={(e) => setForm({...form, year: e.target.value, make: '', model: '', trim: ''})}>
              <option value="">Select year</option>
              {YEARS.map(y => <option key={y}>{y}</option>)}
            </select>
          )}
        </div>

        <div>
          <label style={st.l}>Make * {makes.length > 0 && !vinDecoded && `(${makes.length} available)`}</label>
          {vinDecoded ? (
            <div style={{...st.i, backgroundColor: '#f0f0f0', display: 'flex', alignItems: 'center'}}>
              {form.make} <span style={{color: 'green', marginLeft: '8px', fontSize: '12px'}}>✓ Locked</span>
            </div>
          ) : (
            <select style={{...st.i, opacity: !form.year ? 0.5 : 1}} value={form.make} onChange={(e) => setForm({...form, make: e.target.value, model: '', trim: ''})} disabled={!form.year}>
              <option value="">Select make</option>
              {makes.map(m => <option key={m}>{m}</option>)}
            </select>
          )}
        </div>

        <div>
          <label style={st.l}>Model * {models.length > 0 && !vinDecoded && `(${models.length} available)`}</label>
          {vinDecoded ? (
            <div style={{...st.i, backgroundColor: '#f0f0f0', display: 'flex', alignItems: 'center'}}>
              {form.model} <span style={{color: 'green', marginLeft: '8px', fontSize: '12px'}}>✓ Locked</span>
            </div>
          ) : models.length === 0 && form.make ? (
            <div style={{...st.i, backgroundColor: '#f5f5f5', color: '#999', display: 'flex', alignItems: 'center'}}>
              No models available for {form.make} in {form.year}
            </div>
          ) : (
            <select style={{...st.i, opacity: !form.make ? 0.5 : 1}} value={form.model} onChange={(e) => setForm({...form, model: e.target.value, trim: ''})} disabled={!form.make}>
              <option value="">Select model</option>
              {models.map(m => <option key={m}>{m}</option>)}
            </select>
          )}
        </div>

        <div>
          <label style={st.l}>Trim</label>
          <select style={{...st.i, opacity: !form.model ? 0.5 : 1}} value={form.trim} onChange={(e) => setForm({...form, trim: e.target.value})} disabled={!form.model}>
            <option value="">Select trim (optional)</option>
            {trims.map(t => <option key={t}>{t}</option>)}
          </select>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          <div>
            <label style={st.l}>Mileage</label>
            <input style={{...st.i, cursor: 'text'}} type="number" value={form.mileage} onChange={(e) => setForm({...form, mileage: e.target.value})} />
          </div>
          <div>
            <label style={st.l}>Color</label>
            <select style={{...st.i, opacity: colors.length === 0 ? 0.5 : 1}} value={form.color} onChange={(e) => setForm({...form, color: e.target.value})}>
              <option value="">Select color</option>
              {colors.map(c => <option key={c}>{c}</option>)}
            </select>
          </div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          <div>
            <label style={st.l}>Transmission</label>
            <select style={st.i} value={form.transmission} onChange={(e) => setForm({...form, transmission: e.target.value})}>
              <option value="automatic">Automatic</option>
              <option value="manual">Manual</option>
              <option value="cvt">CVT</option>
            </select>
          </div>
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
          <div>
            <label style={st.l}>Title Status</label>
            <select style={st.i} value={form.titleStatus} onChange={(e) => setForm({...form, titleStatus: e.target.value})}>
              <option value="clean">Clean</option>
              <option value="salvage">Salvage</option>
              <option value="branded">Branded</option>
            </select>
          </div>
          <div>
            <label style={st.l}>Accident History</label>
            <select style={st.i} value={form.accidentHistory} onChange={(e) => setForm({...form, accidentHistory: e.target.value})}>
              <option value="none">None</option>
              <option value="minor">Minor</option>
              <option value="major">Major</option>
            </select>
          </div>
        </div>

        <div>
          <label style={st.l}>Description</label>
          <textarea style={{...st.i, cursor: 'text', minHeight: '100px'}} value={form.description} onChange={(e) => setForm({...form, description: e.target.value})} />
        </div>

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
