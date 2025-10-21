import React, { useEffect, useState } from 'react';
import Link from 'next/link';

interface Lead {
  id: number;
  listing: {
    year: number;
    make: string;
    model: string;
    mileage: number;
    condition: string;
    vin: string;
  };
  seller_contact: {
    name: string;
    email: string;
    phone: string;
  };
  ai_offer: {
    fair: number;
    low: number;
    max: number;
  };
  status: string;
  created_at: string;
}

export default function DealerDashboard() {
  const [leads, setLeads] = useState<Lead[]>([]);
  const [loading, setLoading] = useState(true);
  const [dealerEmail, setDealerEmail] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('dealer_token');
    const email = localStorage.getItem('dealer_email');
    
    if (!token) {
      window.location.href = '/dealer/login';
      return;
    }

    setDealerEmail(email || '');
    fetchLeads(token);
  }, []);

  const fetchLeads = async (token: string) => {
    try {
      const response = await fetch('https://revomotors.onrender.com/api/leads', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setLeads(data);
      } else if (response.status === 401) {
        localStorage.removeItem('dealer_token');
        window.location.href = '/dealer/login';
      } else {
        console.error('Failed to fetch leads');
      }
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('dealer_token');
    localStorage.removeItem('dealer_email');
    window.location.href = '/';
  };

  const handleMakeOffer = (leadId: number) => {
    alert(`Make offer for lead #${leadId} - Feature coming soon!`);
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui' }}>
      <header style={{ backgroundColor: 'white', borderBottom: '1px solid #e5e7eb', padding: '20px' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ fontSize: '24px', fontWeight: 'bold', marginBottom: '5px' }}>Dealer Dashboard</h1>
            <p style={{ fontSize: '14px', color: '#6b7280' }}>{dealerEmail}</p>
          </div>
          <button 
            onClick={handleLogout}
            style={{ color: '#2563eb', textDecoration: 'none', fontSize: '14px', background: 'none', border: 'none', cursor: 'pointer', fontWeight: '500' }}
          >
            Logout →
          </button>
        </div>
      </header>

      <main style={{ maxWidth: '1400px', margin: '0 auto', padding: '40px 20px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '20px', marginBottom: '40px' }}>
          <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#2563eb', marginBottom: '10px' }}>
              {leads.length}
            </div>
            <div style={{ color: '#6b7280', fontSize: '14px' }}>Active Leads</div>
          </div>

          <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#10b981', marginBottom: '10px' }}>
              {leads.filter(l => l.status === 'offered').length}
            </div>
            <div style={{ color: '#6b7280', fontSize: '14px' }}>Offers Made</div>
          </div>

          <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
            <div style={{ fontSize: '36px', fontWeight: 'bold', color: '#8b5cf6', marginBottom: '10px' }}>
              {leads.filter(l => l.status === 'closed').length}
            </div>
            <div style={{ color: '#6b7280', fontSize: '14px' }}>Deals Closed</div>
          </div>
        </div>

        <div style={{ backgroundColor: 'white', borderRadius: '8px', border: '1px solid #e5e7eb', overflow: 'hidden' }}>
          <div style={{ padding: '20px', borderBottom: '1px solid #e5e7eb' }}>
            <h2 style={{ fontSize: '20px', fontWeight: '600' }}>Recent Leads</h2>
          </div>

          {loading ? (
            <div style={{ padding: '40px', textAlign: 'center', color: '#6b7280' }}>
              Loading leads...
            </div>
          ) : leads.length === 0 ? (
            <div style={{ padding: '40px', textAlign: 'center', color: '#6b7280' }}>
              No active leads yet. Check back soon!
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead style={{ backgroundColor: '#f9fafb' }}>
                  <tr>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase' }}>Vehicle</th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase' }}>VIN</th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase' }}>Mileage</th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase' }}>Condition</th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase' }}>AI Offer</th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase' }}>Seller</th>
                    <th style={{ padding: '12px', textAlign: 'left', fontSize: '12px', fontWeight: '600', color: '#6b7280', textTransform: 'uppercase' }}>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {leads.map((lead) => (
                    <tr key={lead.id} style={{ borderTop: '1px solid #e5e7eb' }}>
                      <td style={{ padding: '16px' }}>
                        <div style={{ fontWeight: '500' }}>
                          {lead.listing.year} {lead.listing.make} {lead.listing.model}
                        </div>
                      </td>
                      <td style={{ padding: '16px', fontSize: '14px', color: '#6b7280' }}>
                        {lead.listing.vin}
                      </td>
                      <td style={{ padding: '16px', fontSize: '14px' }}>
                        {lead.listing.mileage.toLocaleString()} mi
                      </td>
                      <td style={{ padding: '16px' }}>
                        <span style={{ padding: '4px 12px', backgroundColor: '#dbeafe', color: '#1e40af', borderRadius: '12px', fontSize: '12px', fontWeight: '500' }}>
                          {lead.listing.condition}
                        </span>
                      </td>
                      <td style={{ padding: '16px', fontWeight: '600', color: '#059669' }}>
                        ${lead.ai_offer.fair.toLocaleString()}
                      </td>
                      <td style={{ padding: '16px', fontSize: '14px' }}>
                        <div>{lead.seller_contact.name}</div>
                        <div style={{ fontSize: '12px', color: '#6b7280' }}>{lead.seller_contact.phone}</div>
                      </td>
                      <td style={{ padding: '16px' }}>
                        <button
                          onClick={() => handleMakeOffer(lead.id)}
                          style={{
                            padding: '8px 16px',
                            backgroundColor: '#2563eb',
                            color: 'white',
                            fontSize: '14px',
                            fontWeight: '500',
                            borderRadius: '6px',
                            border: 'none',
                            cursor: 'pointer',
                          }}
                        >
                          Make Offer
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}