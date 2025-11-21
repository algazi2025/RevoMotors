import React, { useEffect, useState } from 'react';
import Link from 'next/link';

interface Lead {
  lead_id: number;
  status: string;
  created_at: string;
  listing: {
    id: number;
    title: string;
    year: number;
    make: string;
    model: string;
    mileage: number;
    condition: string;
    asking_price: number;
    source: string;
    location: {
      city: string;
      state: string;
    };
    seller: {
      name: string;
      phone: string;
    };
    photos: string[];
  };
  ai_estimate: {
    offer_fair: number;
    offer_low: number;
    offer_high: number;
  };
  communication: {
    first_contact_sent: boolean;
    latest_message: {
      subject: string;
      body: string;
      sent: boolean;
    } | null;
  };
}

interface Stats {
  total_leads: number;
  hot_leads: number;
  marketplace_leads: number;
  new_leads: number;
  contacted_leads: number;
  won_deals: number;
}

export default function DealerDashboard() {
  const [activeTab, setActiveTab] = useState<'hot' | 'marketplace'>('hot');
  const [leads, setLeads] = useState<Lead[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [dealerEmail, setDealerEmail] = useState('');
  const [selectedLead, setSelectedLead] = useState<Lead | null>(null);

  useEffect(() => {
    const token = localStorage.getItem('dealer_token');
    const email = localStorage.getItem('dealer_email');
    
    if (!token) {
      window.location.href = '/dealer/login';
      return;
    }

    setDealerEmail(email || '');
    fetchStats(token);
    fetchLeads(token, activeTab === 'hot' ? 'hot_lead' : 'marketplace');
  }, [activeTab]);

  const fetchStats = async (token: string) => {
    try {
     // const response = await fetch('https://revomotors.onrender.com/api/dealers/stats', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setStats(data);
      }
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const fetchLeads = async (token: string, source: string) => {
    try {
      setLoading(true);
     // const response = await fetch(`https://revomotors.onrender.com/api/leads?source=${source}`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (response.ok) {
        const data = await response.json();
        setLeads(data.leads || []);
      }
    } catch (error) {
      console.error('Error fetching leads:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateMessage = async (leadId: number) => {
    const token = localStorage.getItem('dealer_token');
    try {
      const response = await fetch(`https://revomotors.onrender.com/api/leads/${leadId}/generate-message?message_type=initial_contact`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (response.ok) {
        const data = await response.json();
        alert(`AI Message Generated!\n\nSubject: ${data.subject}\n\n${data.body.substring(0, 200)}...`);
        // Refresh leads
        fetchLeads(token!, activeTab === 'hot' ? 'hot_lead' : 'marketplace');
      }
    } catch (error) {
      console.error('Error generating message:', error);
    }
  };

  const handleSendMessage = async (leadId: number, messageId: number) => {
    const token = localStorage.getItem('dealer_token');
    if (!confirm('Send this message to the seller?')) return;

    try {
      const response = await fetch(`https://revomotors.onrender.com/api/leads/${leadId}/send-message?message_id=${messageId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (response.ok) {
        alert('✅ Message sent successfully!');
        fetchLeads(token!, activeTab === 'hot' ? 'hot_lead' : 'marketplace');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Error sending message');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('dealer_token');
    localStorage.removeItem('dealer_email');
    window.location.href = '/';
  };

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui' }}>
      {/* Header */}
      <header style={{ backgroundColor: 'white', borderBottom: '1px solid #e5e7eb', padding: '15px 0' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h1 style={{ fontSize: '22px', fontWeight: 'bold', marginBottom: '5px' }}>RevoMotors CRM</h1>
            <p style={{ fontSize: '13px', color: '#6b7280' }}>{dealerEmail}</p>
          </div>
          <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
            <a href="/dealer/settings" style={{ color: '#2563eb', textDecoration: 'none', fontSize: '14px', fontWeight: '500' }}>
             ⚙️ Settings
            </a>
            <a href="/dealer/filters" style={{ color: '#2563eb', textDecoration: 'none', fontSize: '14px', fontWeight: '500' }}>
              🔍 Filters
            </a>
            <button 
              onClick={handleLogout}
              style={{ color: '#6b7280', fontSize: '14px', background: 'none', border: 'none', cursor: 'pointer', fontWeight: '500' }}
            >
              Logout →
            </button>
          </div>
        </div>
      </header>

      <main style={{ maxWidth: '1400px', margin: '0 auto', padding: '30px 20px' }}>
        {/* Stats Cards */}
        {stats && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '15px', marginBottom: '30px' }}>
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#2563eb', marginBottom: '5px' }}>{stats.new_leads}</div>
              <div style={{ color: '#6b7280', fontSize: '13px' }}>New Leads</div>
            </div>
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#10b981', marginBottom: '5px' }}>{stats.hot_leads}</div>
              <div style={{ color: '#6b7280', fontSize: '13px' }}>Hot Leads</div>
            </div>
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#8b5cf6', marginBottom: '5px' }}>{stats.marketplace_leads}</div>
              <div style={{ color: '#6b7280', fontSize: '13px' }}>Marketplace</div>
            </div>
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
              <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#f59e0b', marginBottom: '5px' }}>{stats.won_deals}</div>
              <div style={{ color: '#6b7280', fontSize: '13px' }}>Deals Won</div>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div style={{ backgroundColor: 'white', borderRadius: '8px', border: '1px solid #e5e7eb', overflow: 'hidden' }}>
          <div style={{ display: 'flex', borderBottom: '1px solid #e5e7eb' }}>
            <button
              onClick={() => setActiveTab('hot')}
              style={{
                flex: 1,
                padding: '15px',
                backgroundColor: activeTab === 'hot' ? '#2563eb' : 'white',
                color: activeTab === 'hot' ? 'white' : '#6b7280',
                border: 'none',
                cursor: 'pointer',
                fontWeight: '600',
                fontSize: '15px'
              }}
            >
              🔥 Hot Leads ({stats?.hot_leads || 0})
            </button>
            <button
              onClick={() => setActiveTab('marketplace')}
              style={{
                flex: 1,
                padding: '15px',
                backgroundColor: activeTab === 'marketplace' ? '#2563eb' : 'white',
                color: activeTab === 'marketplace' ? 'white' : '#6b7280',
                border: 'none',
                cursor: 'pointer',
                fontWeight: '600',
                fontSize: '15px'
              }}
            >
              🛒 Marketplace Leads ({stats?.marketplace_leads || 0})
            </button>
          </div>

          {/* Leads List */}
          <div style={{ padding: '20px' }}>
            {loading ? (
              <div style={{ textAlign: 'center', padding: '40px', color: '#6b7280' }}>
                Loading leads...
              </div>
            ) : leads.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '40px', color: '#6b7280' }}>
                <div style={{ fontSize: '48px', marginBottom: '10px' }}>📭</div>
                <p>No {activeTab === 'hot' ? 'hot' : 'marketplace'} leads yet.</p>
                {activeTab === 'marketplace' && (
                  <a href="/dealer/filters" style={{ color: '#2563eb', textDecoration: 'none', fontSize: '14px' }}>
                    Set up marketplace filters →
                  </a>
                )}
              </div>
            ) : (
              <div style={{ display: 'grid', gap: '20px' }}>
                {leads.map((lead) => (
                  <div
                    key={lead.lead_id}
                    style={{
                      backgroundColor: '#f9fafb',
                      padding: '20px',
                      borderRadius: '8px',
                      border: '1px solid #e5e7eb'
                    }}
                  >
                    <div style={{ display: 'flex', gap: '20px' }}>
                      {/* Vehicle Image */}
                      <div style={{ width: '200px', height: '150px', backgroundColor: '#e5e7eb', borderRadius: '8px', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '48px' }}>
                        {lead.listing.photos && lead.listing.photos.length > 0 ? (
                          <img src={lead.listing.photos[0]} alt="Vehicle" style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px' }} />
                        ) : '🚗'}
                      </div>

                      {/* Vehicle Details */}
                      <div style={{ flex: 1 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '10px' }}>
                          <div>
                            <h3 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '5px' }}>
                              {lead.listing.year} {lead.listing.make} {lead.listing.model}
                            </h3>
                            <div style={{ fontSize: '14px', color: '#6b7280' }}>
                              {lead.listing.mileage.toLocaleString()} miles • {lead.listing.condition} • {lead.listing.location.city}, {lead.listing.location.state}
                            </div>
                          </div>
                          <span style={{
                            padding: '4px 12px',
                            backgroundColor: lead.listing.source === 'hot_lead' ? '#fef3c7' : '#dbeafe',
                            color: lead.listing.source === 'hot_lead' ? '#92400e' : '#1e40af',
                            borderRadius: '12px',
                            fontSize: '12px',
                            fontWeight: '600'
                          }}>
                            {lead.listing.source === 'hot_lead' ? '🔥 Hot Lead' : '🛒 ' + lead.listing.source}
                          </span>
                        </div>

                        {/* AI Estimate */}
                        <div style={{ backgroundColor: 'white', padding: '12px', borderRadius: '6px', marginBottom: '12px' }}>
                          <div style={{ fontSize: '13px', color: '#6b7280', marginBottom: '5px' }}>AI Market Estimate</div>
                          <div style={{ display: 'flex', gap: '15px', fontSize: '14px' }}>
                            <div>
                              <span style={{ color: '#6b7280' }}>Low:</span>{' '}
                              <span style={{ fontWeight: '600' }}>${lead.ai_estimate.offer_low?.toLocaleString()}</span>
                            </div>
                            <div>
                              <span style={{ color: '#6b7280' }}>Fair:</span>{' '}
                              <span style={{ fontWeight: '600', color: '#059669' }}>${lead.ai_estimate.offer_fair?.toLocaleString()}</span>
                            </div>
                            <div>
                              <span style={{ color: '#6b7280' }}>High:</span>{' '}
                              <span style={{ fontWeight: '600' }}>${lead.ai_estimate.offer_high?.toLocaleString()}</span>
                            </div>
                          </div>
                        </div>

                        {/* Seller Info */}
                        <div style={{ fontSize: '13px', color: '#6b7280', marginBottom: '12px' }}>
                          <strong>Seller:</strong> {lead.listing.seller.name} • {lead.listing.seller.phone}
                        </div>

                        {/* Actions */}
                        <div style={{ display: 'flex', gap: '10px' }}>
                          <a
                            href={`/dealer/lead/${lead.lead_id}`}
                            style={{
                              padding: '10px 20px',
                              backgroundColor: '#2563eb',
                              color: 'white',
                              fontSize: '14px',
                              fontWeight: '600',
                              borderRadius: '6px',
                              textDecoration: 'none',
                              display: 'inline-block'
                            }}
                          >
                            View Details & Send Message
                          </a>
                          {!lead.communication.first_contact_sent && (
                            <button
                              onClick={() => handleGenerateMessage(lead.lead_id)}
                              style={{
                                padding: '10px 20px',
                                backgroundColor: 'white',
                                color: '#2563eb',
                                fontSize: '14px',
                                fontWeight: '600',
                                borderRadius: '6px',
                                border: '1px solid #2563eb',
                                cursor: 'pointer'
                              }}
                            >
                              🤖 Generate AI Message
                            </button>
                          )}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}