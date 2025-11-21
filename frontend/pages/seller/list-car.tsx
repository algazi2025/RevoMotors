import React, { useState, useEffect } from 'react';

export default function ListCar() {
  const [formData, setFormData] = useState({
    year: '', make: '', model: '', trim: '', mileage: '',
    vin: '', color: '', transmission: 'automatic', fuelType: 'gasoline',
    titleStatus: 'clean', accidentHistory: 'none', numOwners: '1',
    description: '', askingPrice: '',
  });

  const [trims, setTrims] = useState<string[]>([]);
  const [colors, setColors] = useState<string[]>([]);
  const [makes, setMakes] = useState<string[]>([]);
  const [models, setModels] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  const API = 'https://revomotors.onrender.com';

  useEffect(() => {
    Promise.all([
      fetch(`${API}/api/cars/makes`).then(r => r.json()).catch(() => []),
      fetch(`${API}/api/cars/colors`).then(r => r.json()).catch(() => [])
    ]).then(([makesData, colorsData]) => {
      setMakes(makesData || []);
      setColors(colorsData || []);
    });
  }, []);

  useEffect(() => {
    if (!formData.make) return;
    fetch(`${API}/api/cars/models?make=${formData.make}`)
      .then(r => r.json())
      .then(data => setModels(data || []))
      .catch(() => setModels([]));
  }, [formData.make]);

  useEffect(() => {
    if (!formData.make || !formData.model) {
      setTrims([]);
      return;
    }
    fetch(`${API}/api/cars/trims?make=${formData.make}&model=${formData.model}`)
      .then(r => r.json())
      .then(data => setTrims(data || []))
      .catch(() => setTrims([]));
  }, [formData.make, formData.model]);

  const decodeVIN = async (vin: string) => {
    if (vin.length !== 17) return;
    try {
      const res = await fetch(`${API}/api/cars/decode-vin?vin=${vin}`);
      const data = await res.json();
      if (data.year && data.make && data.model) {
        setFormData(prev => ({
          ...prev,
          year: data.year,
          make: data.make,
          model: data.model,
          fuelType: data.fuelType || 'gasoline',
        }));
      }
    } catch (error) {
      console.error('VIN decode error:', error);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/leads/webhook/lead_received`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          vin: formData.vin, year: formData.year, make: formData.make, model: formData.model,
          trim: formData.trim, mileage: parseInt(formData.mileage) || 0, color: formData.color,
          transmission: formData.transmission, fuelType: formData.fuelType,
          titleStatus: formData.titleStatus, accidentHistory: formData.accidentHistory,
          numOwners: parseInt(formData.numOwners) || 1, askingPrice: parseInt(formData.askingPrice) || 0,
          description: formData.description,
        }),
      });
      const result = await res.json();
      if (result.success) {
        alert('✓ Listing submitted! ID: ' + result.listing_id);
        setFormData({year: '', make: '', model: '', trim: '', mileage: '', vin: '', color: '', transmission: 'automatic', fuelType: 'gasoline', titleStatus: 'clean', accidentHistory: 'none', numOwners: '1', description: '', askingPrice: ''});
      } else {
        alert('Error: ' + (result.error || 'Unknown error'));
      }
    } catch (error) {
      alert('Error submitting form');
    } finally {
      setLoading(false);
    }
  };

  const s = {l: {display: 'block', marginBottom: '6px', fontWeight: '600'}, i: {width: '100%', padding: '10px', border: '1px solid #ddd', borderRadius: '4px', fontSize: '14px', boxSizing: 'border-box' as const}};

  return (
    <div style={{maxWidth: '900px', margin: '0 auto', padding: '24px'}}>
      <h1 style={{fontSize: '32px', marginBottom: '32px'}}>🚗 Vehicle Information</h1>
      <form style={{display: 'flex', flexDirection: 'column', gap: '20px'}} onSubmit={handleSubmit}>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          <div><label style={s.l}>VIN</label><input style={s.i} type="text" placeholder="KNDMC5C16J6368353" value={formData.vin} onChange={(e) => setFormData({...formData, vin: e.target.value})} onBlur={(e) => decodeVIN(e.target.value)} />{formData.year && <p style={{color: '#22c55e', fontSize: '12px', marginTop: '4px'}}>✓ Decoded</p>}</div>
          <div><label style={s.l}>Year</label><input style={s.i} type="text" placeholder="2018" value={formData.year} onChange={(e) => setFormData({...formData, year: e.target.value})} /></div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px'}}>
          <div><label style={s.l}>Make</label><select style={s.i} value={formData.make} onChange={(e) => setFormData({...formData, make: e.target.value, model: '', trim: ''})}><option value="">Select</option>{makes.map(m => <option key={m} value={m}>{m}</option>)}</select></div>
          <div><label style={s.l}>Model</label><select style={s.i} value={formData.model} onChange={(e) => setFormData({...formData, model: e.target.value, trim: ''})} disabled={!formData.make}><option value="">Select</option>{models.map(m => <option key={m} value={m}>{m}</option>)}</select></div>
          <div><label style={s.l}>Trim</label><select style={s.i} value={formData.trim} onChange={(e) => setFormData({...formData, trim: e.target.value})} disabled={!formData.model}><option value="">Select</option>{trims.map(t => <option key={t} value={t}>{t}</option>)}</select></div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          <div><label style={s.l}>Mileage</label><input style={s.i} type="number" placeholder="45000" value={formData.mileage} onChange={(e) => setFormData({...formData, mileage: e.target.value})} /></div>
          <div><label style={s.l}>Color</label><select style={s.i} value={formData.color} onChange={(e) => setFormData({...formData, color: e.target.value})}><option value="">Select</option>{colors.map(c => <option key={c} value={c}>{c}</option>)}</select></div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          <div><label style={s.l}>Transmission</label><select style={s.i} value={formData.transmission} onChange={(e) => setFormData({...formData, transmission: e.target.value})}><option value="automatic">Automatic</option><option value="manual">Manual</option></select></div>
          <div><label style={s.l}>Fuel Type</label><select style={s.i} value={formData.fuelType} onChange={(e) => setFormData({...formData, fuelType: e.target.value})}><option value="gasoline">Gasoline</option><option value="diesel">Diesel</option><option value="hybrid">Hybrid</option></select></div>
        </div>

        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px'}}>
          <div><label style={s.l}>Title Status</label><select style={s.i} value={formData.titleStatus} onChange={(e) => setFormData({...formData, titleStatus: e.target.value})}><option value="clean">Clean</option><option value="salvage">Salvage</option></select></div>
          <div><label style={s.l}>Accident History</label><select style={s.i} value={formData.accidentHistory} onChange={(e) => setFormData({...formData, accidentHistory: e.target.value})}><option value="none">None</option><option value="minor">Minor</option></select></div>
        </div>

        <div><label style={s.l}>Description</label><textarea style={{...s.i, minHeight: '100px'}} placeholder="Describe..." value={formData.description} onChange={(e) => setFormData({...formData, description: e.target.value})} /></div>
        <div><label style={s.l}>Asking Price</label><input style={s.i} type="number" placeholder="25000" value={formData.askingPrice} onChange={(e) => setFormData({...formData, askingPrice: e.target.value})} /></div>

        <button style={{padding: '12px', backgroundColor: '#2563eb', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer', fontWeight: 'bold'}} type="submit" disabled={loading}>{loading ? 'Submitting...' : 'List My Car'}</button>
      </form>
    </div>
  );
}