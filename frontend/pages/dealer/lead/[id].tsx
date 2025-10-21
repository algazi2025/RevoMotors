import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';

interface LeadDetail {
  lead_id: number;
  status: string;
  created_at: string;
  listing: any;
  ai_estimate: any;
  dealer_offer: number | null;
  messages: any[];
}

export default function LeadDetailPage() {
  const router = useRouter();
  const { id } = router.query;
  
  const [lead, setLead] = useState<LeadDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [generatingMessage, setGeneratingMessage] = useState(false);
  const [aiMessage, setAiMessage] = useState<any>(null);
  const [editedMessage, setEditedMessage] = useState('');
  const [customOffer, setCustomOffer] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (id) {
      const token = localStorage.getItem('dealer_token');
      if (!token) {
        window.location.href = '/dealer/login';
        return;
      }
      fetchLeadDetails(token, id as string);
    }
  }, [id]);

  const fetchLeadDetails = async (token: string, leadId: string) => {
    try {
      const response = await fetch(`https://revomotors.onrender.com/api/leads/${leadId}`, {
        headers: { 'Authorization': `Bearer ${token}` },
      });

      if (response.ok) {
        const data = await response.json();
        setLead(data);
        setCustomOffer(data.ai_estimate?.offer_fair?.toString() || '');
      }
    } catch (error) {
      console.error('Error fetching lead:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateMessage = async (messageType: string) => {
    const token = localStorage.getItem('dealer_token');
    setGeneratingMessage(true);

    try {
      const response = await fetch(
        `https://revomotors.onrender.com/api/leads/${id}/generate-message?message_type=${messageType}`,
        {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
        }
      );

      if (response.ok) {
        const data = await response.json();
        setAiMessage(data);
        setEditedMessage(data.body);
      } else {
        alert('Failed to generate message');
      }
    } catch (error) {
      console.error('Error generating message:', error);
      alert('Error generating message');
    } finally {
      setGeneratingMessage(false);
    }
  };

  const handleUpdateOffer = async () => {
    const token = localStorage.getItem('dealer_token');
    if (!customOffer) return;

    try {
      const response = await fetch(
        `https://revomotors.onrender.com/api/leads/${id}/update-offer?offer_amount=${parseFloat(customOffer)}`,
        {
          method: 'PUT',
          headers: { 'Authorization': `Bearer ${token}` },
        }
      );

      if (response.ok) {
        alert('✅ Offer updated!');
        fetchLeadDetails(token, id as string);
      }
    } catch (error) {
      console.error('Error updating offer:', error);
    }
  };

  const handleSendMessage = async () => {
    const token = localStorage.getItem('dealer_token');
    if (!aiMessage || !confirm('Send this message to the seller?')) return;

    setSending(true);
    try {
      const response = await fetch(
        `https://revomotors.onrender.com/api/leads/${id}/send-message?message_id=${aiMessage.message_id}${editedMessage !== aiMessage.body ? `&updated_body=${encodeURIComponent(editedMessage)}` : ''}`,
        {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
        }
      );

      if (response.ok) {
        alert('✅ Message sent successfully!');
        setAiMessage(null);
        setEditedMessage('');
        fetchLeadDetails(token, id as string);
      } else {
        alert('Failed to send message');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Error sending message');
    } finally {
      setSending(false);
    }
  };

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div>Loading lead details...</div>
      </div>
    );
  }

  if (!lead) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div>Lead not found</div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui' }}>
      {/* Header */}
      <header style={{ backgroundColor: 'white', borderBottom: '1px solid #e5e7eb', padding: '15px 0' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 20px' }}>
          <a href="/dealer/dashboard" style={{ color: '#2563eb', textDecoration: 'none', fontSize: '14px', fontWeight: '500' }}>
            ← Back to Dashboard
          </a>
        </div>
      </header>

      <main style={{ maxWidth: '1400px', margin: '0 auto', padding: '30px 20px' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '25px' }}>
          {/* Left Column - Vehicle Details & Messages */}
          <div>
            {/* Vehicle Card */}
            <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb', marginBottom: '25px' }}>
              <div style={{ display: 'flex', gap: '20px' }}>
                <div style={{ width: '300px', height: '200px', backgroundColor: '#e5e7eb', borderRadius: '8px', flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '64px' }}>
                  {lead.listing.photos && lead.listing.photos.length > 0 ? (
                    <img src={lead.listing.photos[0]} alt="Vehicle" style={{ width: '100%', height: '100%', objectFit: 'cover', borderRadius: '8px' }} />
                  ) : '🚗'}
                </div>
                
                <div style={{ flex: 1 }}>
                  <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '10px' }}>
                    {lead.listing.year} {lead.listing.make} {lead.listing.model} {lead.listing.trim}
                  </h1>
                  
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px', fontSize: '14px', marginBottom: '15px' }}>
                    <div><span style={{ color: '#6b7280' }}>Mileage:</span> <strong>{lead.listing.mileage?.toLocaleString()} miles</strong></div>
                    <div><span style={{ color: '#6b7280' }}>Condition:</span> <strong>{lead.listing.condition}</strong></div>
                    <div><span style={{ color: '#6b7280' }}>VIN:</span> <strong>{lead.listing.vin || 'N/A'}</strong></div>
                    <div><span style={{ color: '#6b7280' }}>Color:</span> <strong>{lead.listing.color || 'N/A'}</strong></div>
                    <div><span style={{ color: '#6b7280' }}>Transmission:</span> <strong>{lead.listing.transmission || 'N/A'}</strong></div>
                    <div><span style={{ color: '#6b7280' }}>Fuel:</span> <strong>{lead.listing.fuel_type || 'N/A'}</strong></div>
                  </div>

                  {lead.listing.description && (
                    <div style={{ marginTop: '15px', padding: '12px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
                      <div style={{ fontSize: '13px', color: '#6b7280', marginBottom: '5px' }}>Description:</div>
                      <div style={{ fontSize: '14px' }}>{lead.listing.description}</div>
                    </div>
                  )}
                </div>
              </div>

              {/* Seller Info */}
              <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f9fafb', borderRadius: '8px' }}>
                <div style={{ fontSize: '13px', fontWeight: '600', color: '#6b7280', marginBottom: '8px' }}>SELLER CONTACT</div>
                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px', fontSize: '14px' }}>
                  <div><strong>Name:</strong> {lead.listing.seller.name}</div>
                  <div><strong>Email:</strong> {lead.listing.seller.email}</div>
                  <div><strong>Phone:</strong> {lead.listing.seller.phone}</div>
                </div>
                {lead.listing.external_url && (
                  <div style={{ marginTop: '10px' }}>
                    <a href={lead.listing.external_url} target="_blank" style={{ color: '#2563eb', fontSize: '14px' }}>
                      View Original Listing →
                    </a>
                  </div>
                )}
              </div>
            </div>

            {/* AI Message Generator */}
            {!aiMessage ? (
              <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
                <h2 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '15px' }}>📩 Generate AI Message</h2>
                <p style={{ fontSize: '14px', color: '#6b7280', marginBottom: '20px' }}>
                  AI will create a professional message for you to review and send to the seller.
                </p>

                <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
                  <button
                    onClick={() => handleGenerateMessage('initial_contact')}
                    disabled={generatingMessage}
                    style={{
                      padding: '12px 20px',
                      backgroundColor: generatingMessage ? '#9ca3af' : '#2563eb',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: generatingMessage ? 'not-allowed' : 'pointer',
                      fontWeight: '600',
                      fontSize: '14px',
                    }}
                  >
                    {generatingMessage ? '🤖 Generating...' : '🤖 Generate Initial Contact'}
                  </button>

                  {lead.messages.length > 0 && (
                    <>
                      <button
                        onClick={() => handleGenerateMessage('follow_up_1')}
                        style={{
                          padding: '12px 20px',
                          backgroundColor: 'white',
                          color: '#2563eb',
                          border: '1px solid #2563eb',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          fontWeight: '600',
                          fontSize: '14px',
                        }}
                      >
                        Follow-up Day 1
                      </button>
                      <button
                        onClick={() => handleGenerateMessage('follow_up_2')}
                        style={{
                          padding: '12px 20px',
                          backgroundColor: 'white',
                          color: '#2563eb',
                          border: '1px solid #2563eb',
                          borderRadius: '6px',
                          cursor: 'pointer',
                          fontWeight: '600',
                          fontSize: '14px',
                        }}
                      >
                        Follow-up Day 3
                      </button>
                    </>
                  )}

                  <button
                    onClick={() => handleGenerateMessage('request_more_info')}
                    style={{
                      padding: '12px 20px',
                      backgroundColor: 'white',
                      color: '#6b7280',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      cursor: 'pointer',
                      fontSize: '14px',
                    }}
                  >
                    Request More Info
                  </button>
                </div>
              </div>
            ) : (
              <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '2px solid #2563eb' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
                  <h2 style={{ fontSize: '18px', fontWeight: 'bold' }}>✅ AI Message Ready to Send</h2>
                  <button
                    onClick={() => { setAiMessage(null); setEditedMessage(''); }}
                    style={{ background: 'none', border: 'none', fontSize: '20px', cursor: 'pointer', color: '#6b7280' }}
                  >
                    ✕
                  </button>
                </div>

                <div style={{ marginBottom: '15px' }}>
                  <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', fontSize: '14px' }}>
                    Subject:
                  </label>
                  <input
                    type="text"
                    value={aiMessage.subject}
                    readOnly
                    style={{
                      width: '100%',
                      padding: '10px',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      fontSize: '14px',
                      backgroundColor: '#f9fafb',
                    }}
                  />
                </div>

                <div style={{ marginBottom: '20px' }}>
                  <label style={{ display: 'block', fontWeight: '600', marginBottom: '8px', fontSize: '14px' }}>
                    Message Body: (You can edit this)
                  </label>
                  <textarea
                    value={editedMessage}
                    onChange={(e) => setEditedMessage(e.target.value)}
                    style={{
                      width: '100%',
                      minHeight: '250px',
                      padding: '12px',
                      border: '1px solid #d1d5db',
                      borderRadius: '6px',
                      fontSize: '14px',
                      fontFamily: 'inherit',
                      lineHeight: '1.6',
                    }}
                  />
                </div>

                <div style={{ display: 'flex', gap: '10px' }}>
                  <button
                    onClick={handleSendMessage}
                    disabled={sending}
                    style={{
                      padding: '14px 30px',
                      backgroundColor: sending ? '#9ca3af' : '#10b981',
                      color: 'white',
                      border: 'none',
                      borderRadius: '6px',
                      cursor: sending ? 'not-allowed' : 'pointer',
                      fontWeight: '700',
                      fontSize: '16px',
                    }}
                  >
                    {sending ? 'Sending...' : '✉️ SEND MESSAGE TO SELLER'}
                  </button>
                </div>
              </div>
            )}

            {/* Message History */}
            {lead.messages.length > 0 && (
              <div style={{ backgroundColor: 'white', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb', marginTop: '25px' }}>
                <h2 style={{ fontSize: '18px', fontWeight: 'bold', marginBottom: '15px' }}>📜 Communication History</h2>
                {lead.messages.map((msg, index) => (
                  <div key={index} style={{ padding: '15px', backgroundColor: '#f9fafb', borderRadius: '6px', marginBottom: '10px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span style={{ fontWeight: '600', fontSize: '14px' }}>{msg.subject}</span>
                      <span style={{
                        padding: '2px 8px',
                        backgroundColor: msg.sent ? '#d1fae5' : '#fef3c7',
                        color: msg.sent ? '#065f46' : '#92400e',
                        borderRadius: '10px',
                        fontSize: '11px',
                        fontWeight: '600',
                      }}>
                        {msg.sent ? '✓ Sent' : '⏳ Draft'}
                      </span>
                    </div>
                    <div style={{ fontSize: '13px', color: '#6b7280', whiteSpace: 'pre-wrap' }}>
                      {msg.body.substring(0, 150)}...
                    </div>
                    {msg.sent_at && (
                      <div style={{ fontSize: '12px', color: '#9ca3af', marginTop: '8px' }}>
                        Sent: {new Date(msg.sent_at).toLocaleString()}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Right Column - AI Estimate & Offer */}
          <div>
            {/* AI Estimate */}
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb', marginBottom: '20px' }}>
              <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '15px' }}>🤖 AI Market Estimate</h3>
              
              <div style={{ marginBottom: '15px' }}>
                <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '5px' }}>ESTIMATED VALUE</div>
                <div style={{ fontSize: '32px', fontWeight: 'bold', color: '#059669' }}>
                  ${lead.ai_estimate.estimated_value?.toLocaleString()}
                </div>
              </div>

              <div style={{ display: 'grid', gap: '10px', marginBottom: '15px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
                  <span style={{ fontSize: '13px', color: '#6b7280' }}>Low Offer:</span>
                  <span style={{ fontSize: '14px', fontWeight: '600' }}>${lead.ai_estimate.offer_low?.toLocaleString()}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#d1fae5', borderRadius: '6px' }}>
                  <span style={{ fontSize: '13px', color: '#065f46' }}>Fair Offer:</span>
                  <span style={{ fontSize: '14px', fontWeight: '700', color: '#065f46' }}>${lead.ai_estimate.offer_fair?.toLocaleString()}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px', backgroundColor: '#f9fafb', borderRadius: '6px' }}>
                  <span style={{ fontSize: '13px', color: '#6b7280' }}>High Offer:</span>
                  <span style={{ fontSize: '14px', fontWeight: '600' }}>${lead.ai_estimate.offer_high?.toLocaleString()}</span>
                </div>
              </div>

              {lead.ai_estimate.rationale && (
                <div style={{ padding: '12px', backgroundColor: '#eff6ff', borderRadius: '6px', fontSize: '13px', color: '#1e40af', lineHeight: '1.5' }}>
                  <strong>AI Analysis:</strong> {lead.ai_estimate.rationale}
                </div>
              )}
            </div>

            {/* Custom Offer */}
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb', marginBottom: '20px' }}>
              <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '15px' }}>💰 Your Offer</h3>
              
              <div style={{ marginBottom: '15px' }}>
                <label style={{ display: 'block', fontSize: '13px', fontWeight: '600', marginBottom: '8px', color: '#374151' }}>
                  Offer Amount ($)
                </label>
                <input
                  type="number"
                  value={customOffer}
                  onChange={(e) => setCustomOffer(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '12px',
                    border: '2px solid #d1d5db',
                    borderRadius: '6px',
                    fontSize: '18px',
                    fontWeight: 'bold',
                  }}
                  placeholder="Enter your offer"
                />
              </div>

              <button
                onClick={handleUpdateOffer}
                style={{
                  width: '100%',
                  padding: '12px',
                  backgroundColor: '#2563eb',
                  color: 'white',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '600',
                  fontSize: '14px',
                }}
              >
                Update Offer
              </button>

              {lead.dealer_offer && (
                <div style={{ marginTop: '15px', padding: '12px', backgroundColor: '#f9fafb', borderRadius: '6px', fontSize: '13px' }}>
                  <strong>Current Offer:</strong> ${lead.dealer_offer.toLocaleString()}
                </div>
              )}
            </div>

            {/* Lead Info */}
            <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
              <h3 style={{ fontSize: '16px', fontWeight: 'bold', marginBottom: '15px' }}>📊 Lead Info</h3>
              
              <div style={{ fontSize: '13px', marginBottom: '10px' }}>
                <span style={{ color: '#6b7280' }}>Status:</span>{' '}
                <span style={{
                  padding: '3px 10px',
                  backgroundColor: '#dbeafe',
                  color: '#1e40af',
                  borderRadius: '10px',
                  fontWeight: '600',
                  fontSize: '12px',
                }}>
                  {lead.status}
                </span>
              </div>

              <div style={{ fontSize: '13px', marginBottom: '10px' }}>
                <span style={{ color: '#6b7280' }}>Source:</span>{' '}
                <strong>{lead.listing.source}</strong>
              </div>

              <div style={{ fontSize: '13px', marginBottom: '10px' }}>
                <span style={{ color: '#6b7280' }}>Created:</span>{' '}
                <strong>{new Date(lead.created_at).toLocaleDateString()}</strong>
              </div>

              <div style={{ fontSize: '13px' }}>
                <span style={{ color: '#6b7280' }}>Location:</span>{' '}
                <strong>{lead.listing.location.city}, {lead.listing.location.state}</strong>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}