import React from 'react';

export default function DealerDashboard() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui' }}>
      <div style={{ backgroundColor: 'white', borderBottom: '1px solid #e5e7eb', padding: '20px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h1 style={{ fontSize: '20px', fontWeight: 'bold' }}>Dealer Dashboard</h1>
          <a href="/" style={{ color: '#2563eb', textDecoration: 'none' }}>Logout</a>
        </div>
      </div>

      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '20px' }}>Active Leads</h2>

        <div style={{ backgroundColor: 'white', padding: '40px', borderRadius: '8px', border: '1px solid #e5e7eb', textAlign: 'center', marginBottom: '30px' }}>
          <p style={{ color: '#6b7280' }}>No active leads yet. Check back soon!</p>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px' }}>
          <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#2563eb', marginBottom: '10px' }}>0</div>
            <div style={{ color: '#6b7280' }}>Active Leads</div>
          </div>

          <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#10b981', marginBottom: '10px' }}>0</div>
            <div style={{ color: '#6b7280' }}>Offers Made</div>
          </div>

          <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#8b5cf6', marginBottom: '10px' }}>0</div>
            <div style={{ color: '#6b7280' }}>Deals Closed</div>
          </div>
        </div>
      </div>
    </div>
  );
}