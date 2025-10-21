import React, { useState } from 'react';
import Link from 'next/link';

export default function DealerRegister() {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    dealershipName: '',
    phone: '',
    licenseNumber: '',
    gdprConsent: false,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }

    if (!formData.gdprConsent) {
      setError('Please accept the terms and conditions');
      setLoading(false);
      return;
    }

    try {
      const response = await fetch('https://revomotors.onrender.com/api/auth/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: formData.email,
          password: formData.password,
          first_name: formData.firstName,
          last_name: formData.lastName,
          role: 'dealer',
          gdpr_consent: formData.gdprConsent,
          ccpa_consent: formData.gdprConsent,
          dealer_info: {
            dealership_name: formData.dealershipName,
            phone: formData.phone,
            license_number: formData.licenseNumber,
          },
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store token
        localStorage.setItem('dealer_token', data.access_token);
        localStorage.setItem('dealer_email', formData.email);
        
        alert('Registration successful! Redirecting to dashboard...');
        window.location.href = '/dealer/dashboard';
      } else {
        setError(data.detail || 'Registration failed. Email may already be in use.');
      }
    } catch (error) {
      console.error('Error:', error);
      setError('Connection error. Please try again.');
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

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui', padding: '40px 20px' }}>
      <div style={{ maxWidth: '600px', margin: '0 auto' }}>
        <div style={{ textAlign: 'center', marginBottom: '30px' }}>
          <h1 style={{ fontSize: '32px', fontWeight: 'bold', marginBottom: '10px' }}>
            Dealer Registration
          </h1>
          <p style={{ color: '#6b7280' }}>
            Join our network of verified dealers
          </p>
        </div>

        <form onSubmit={handleSubmit} style={{ backgroundColor: 'white', padding: '40px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
          {error && (
            <div style={{ padding: '12px', backgroundColor: '#fee2e2', color: '#991b1b', borderRadius: '6px', marginBottom: '20px', fontSize: '14px' }}>
              {error}
            </div>
          )}

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '20px' }}>
            <div>
              <label style={labelStyle}>First Name *</label>
              <input
                type="text"
                required
                value={formData.firstName}
                onChange={(e) => setFormData({...formData, firstName: e.target.value})}
                style={inputStyle}
                placeholder="John"
              />
            </div>

            <div>
              <label style={labelStyle}>Last Name *</label>
              <input
                type="text"
                required
                value={formData.lastName}
                onChange={(e) => setFormData({...formData, lastName: e.target.value})}
                style={inputStyle}
                placeholder="Doe"
              />
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={labelStyle}>Email *</label>
            <input
              type="email"
              required
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              style={inputStyle}
              placeholder="dealer@example.com"
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={labelStyle}>Dealership Name *</label>
            <input
              type="text"
              required
              value={formData.dealershipName}
              onChange={(e) => setFormData({...formData, dealershipName: e.target.value})}
              style={inputStyle}
              placeholder="ABC Motors"
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '20px' }}>
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
              <label style={labelStyle}>Dealer License # *</label>
              <input
                type="text"
                required
                value={formData.licenseNumber}
                onChange={(e) => setFormData({...formData, licenseNumber: e.target.value})}
                style={inputStyle}
                placeholder="DL123456"
              />
            </div>
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={labelStyle}>Password *</label>
            <input
              type="password"
              required
              minLength={8}
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              style={inputStyle}
              placeholder="••••••••"
            />
          </div>

          <div style={{ marginBottom: '20px' }}>
            <label style={labelStyle}>Confirm Password *</label>
            <input
              type="password"
              required
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
              style={inputStyle}
              placeholder="••••••••"
            />
          </div>

          <div style={{ marginBottom: '25px' }}>
            <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
              <input
                type="checkbox"
                required
                checked={formData.gdprConsent}
                onChange={(e) => setFormData({...formData, gdprConsent: e.target.checked})}
                style={{ marginRight: '10px' }}
              />
              <span style={{ fontSize: '14px', color: '#4b5563' }}>
                I agree to the Terms of Service and Privacy Policy
              </span>
            </label>
          </div>

          <button
            type="submit"
            disabled={loading}
            style={{
              width: '100%',
              padding: '14px',
              backgroundColor: loading ? '#9ca3af' : '#2563eb',
              color: 'white',
              fontSize: '16px',
              fontWeight: '600',
              borderRadius: '6px',
              border: 'none',
              cursor: loading ? 'not-allowed' : 'pointer',
              marginBottom: '15px',
            }}
          >
            {loading ? 'Creating Account...' : 'Create Dealer Account'}
          </button>

          <div style={{ textAlign: 'center', fontSize: '14px', color: '#6b7280' }}>
            Already have an account?{' '}
            <Link href="/dealer/login" style={{ color: '#2563eb', textDecoration: 'none', fontWeight: '500' }}>
              Sign in here
            </Link>
          </div>
        </form>

        <div style={{ textAlign: 'center', marginTop: '20px' }}>
          <Link href="/" style={{ color: '#6b7280', fontSize: '14px', textDecoration: 'none' }}>
            ← Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
}