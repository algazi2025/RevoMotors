import React from 'react';

export default function Home() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui, -apple-system, sans-serif' }}>
      {/* Header */}
      <div style={{ backgroundColor: 'white', borderBottom: '1px solid #e5e7eb', padding: '20px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <h1 style={{ fontSize: '24px', fontWeight: 'bold', margin: 0 }}>RevoMotors</h1>
        </div>
      </div>

      {/* Main Content */}
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '60px 20px' }}>
        <div style={{ textAlign: 'center', marginBottom: '60px' }}>
          <h2 style={{ fontSize: '48px', fontWeight: 'bold', marginBottom: '20px' }}>
            Used Car AI Platform
          </h2>
          <p style={{ fontSize: '20px', color: '#6b7280', marginBottom: '40px' }}>
            Connect sellers with verified dealers. Get AI-powered offers instantly.
          </p>

          {/* Buttons */}
          <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', flexWrap: 'wrap' }}>
            <a 
              href="/seller/list-car" 
              style={{ 
                display: 'inline-block',
                padding: '16px 32px', 
                backgroundColor: '#2563eb', 
                color: 'white', 
                fontSize: '18px', 
                fontWeight: '600',
                borderRadius: '8px',
                textDecoration: 'none',
                cursor: 'pointer'
              }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#1d4ed8'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#2563eb'}
            >
              I'm a Seller
            </a>
            
            <a 
              href="/dealer/dashboard" 
              style={{ 
                display: 'inline-block',
                padding: '16px 32px', 
                backgroundColor: 'white', 
                color: '#2563eb', 
                fontSize: '18px', 
                fontWeight: '600',
                borderRadius: '8px',
                border: '2px solid #2563eb',
                textDecoration: 'none',
                cursor: 'pointer'
              }}
              onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#eff6ff'}
              onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'white'}
            >
              I'm a Dealer
            </a>
          </div>
        </div>

        {/* Features */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '30px', marginTop: '60px' }}>
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '12px', textAlign: 'center', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '48px', marginBottom: '15px' }}>⚡</div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '10px' }}>Fast Process</h3>
            <p style={{ color: '#6b7280' }}>List your car in under 2 minutes</p>
          </div>

          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '12px', textAlign: 'center', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '48px', marginBottom: '15px' }}>🤖</div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '10px' }}>AI Powered</h3>
            <p style={{ color: '#6b7280' }}>Smart market pricing analysis</p>
          </div>

          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '12px', textAlign: 'center', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '48px', marginBottom: '15px' }}>✅</div>
            <h3 style={{ fontSize: '20px', fontWeight: '600', marginBottom: '10px' }}>Verified Dealers</h3>
            <p style={{ color: '#6b7280' }}>Trusted professionals only</p>
          </div>
        </div>
      </div>
    </div>
  );
}