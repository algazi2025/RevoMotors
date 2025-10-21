import React, { useEffect, useState } from 'react';
import Link from 'next/link';

interface DealerProfile {
  company_name: string;
  dealership_name: string;
  license_number: string;
  phone: string;
  address: string;
  city: string;
  state: string;
  zip_code: string;
  website: string;
  verification_status: string;
  communication_preferences: {
    auto_followup_enabled: boolean;
    followup_day_1: boolean;
    followup_day_3: boolean;
    followup_day_7: boolean;
  };
}

export default function DealerSettings() {
  const [profile, setProfile] = useState<DealerProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeSection, setActiveSection] = useState<'profile' | 'communication' | 'documents'>('profile');

  useEffect(() => {
    const token = localStorage.getItem('dealer_token');
    if (!token) {
      window.location.href = '/dealer/login';
      return;
    }
    fetchProfile(token);
  }, []);

  const fetchProfile = async (token: string) => {
    try {
      const response = await fetch('https://revomotors.onrender.com/api/dealers/profile', {
        headers: { 'Authorization': `Bearer ${token}` },
      });
      if (response.ok) {
        const data = await response.json();
        setProfile(data);
      }
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSaveProfile = async () => {
    const token = localStorage.getItem('dealer_token');
    if (!profile) return;

    setSaving(true);
    try {
      const response = await fetch('https://revomotors.onrender.com/api/dealers/profile', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          company_name: profile.company_name,
          dealership_name: profile.dealership_name,
          license_number: profile.license_number,
          phone: profile.phone,
          address: profile.address,
          city: profile.city,
          state: profile.state,
          zip_code: profile.zip_code,
          website: profile.website,
        }),
      });

      if (response.ok) {
        alert('✅ Profile updated successfully!');
      } else {
        alert('Failed to update profile');
      }
    } catch (error) {
      console.error('Error saving profile:', error);
      alert('Error saving profile');
    } finally {
      setSaving(false);
    }
  };

  const handleSaveCommunicationPrefs = async () => {
    const token = localStorage.getItem('dealer_token');
    if (!profile) return;

    setSaving(true);
    try {
      const response = await fetch('https://revomotors.onrender.com/api/dealers/communication-preferences', {
        method: 'PUT',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          auto_followup_enabled: profile.communication_preferences.auto_followup_enabled,
          followup_day_1: profile.communication_preferences.followup_day_1,
          followup_day_3: profile.communication_preferences.followup_day_3,
          followup_day_7: profile.communication_preferences.followup_day_7,
        }),
      });

      if (response.ok) {
        alert('✅ Communication preferences updated!');
      }
    } catch (error) {
      console.error('Error saving preferences:', error);
    } finally {
      setSaving(false);
    }
  };

  const inputStyle = {
    width: '100%',
    padding: '12px',
    border: '1px solid #d1d5db',
    borderRadius: '6px',
    fontSize: '15px',
  };

  const labelStyle = {
    display: 'block',
    fontWeight: '600',
    marginBottom: '8px',
    fontSize: '14px',
    color: '#374151',
  };

  if (loading) {
    return (
      <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div>Loading...</div>
      </div>
    );
  }

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#f9fafb', fontFamily: 'system-ui' }}>
      {/* Header */}
      <header style={{ backgroundColor: 'white', borderBottom: '1px solid #e5e7eb', padding: '15px 0' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
          <a href="/dealer/dashboard" style={{ color: '#2563eb', textDecoration: 'none', fontSize: '14px', fontWeight: '500' }}>
            ← Back to Dashboard
          </a>
        </div>
      </header>

      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '30px 20px' }}>
        <h1 style={{ fontSize: '28px', fontWeight: 'bold', marginBottom: '30px' }}>Account Settings</h1>

        <div style={{ display: 'grid', gridTemplateColumns: '250px 1fr', gap: '30px' }}>
          {/* Sidebar */}
          <div style={{ backgroundColor: 'white', padding: '20px', borderRadius: '8px', border: '1px solid #e5e7eb', height: 'fit-content' }}>
            <div style={{ marginBottom: '10px' }}>
              <button
                onClick={() => setActiveSection('profile')}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '12px',
                  backgroundColor: activeSection === 'profile' ? '#eff6ff' : 'transparent',
                  color: activeSection === 'profile' ? '#2563eb' : '#6b7280',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '500',
                  fontSize: '14px',
                }}
              >
                🏢 Dealership Profile
              </button>
            </div>
            <div style={{ marginBottom: '10px' }}>
              <button
                onClick={() => setActiveSection('communication')}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '12px',
                  backgroundColor: activeSection === 'communication' ? '#eff6ff' : 'transparent',
                  color: activeSection === 'communication' ? '#2563eb' : '#6b7280',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '500',
                  fontSize: '14px',
                }}
              >
                💬 Communication
              </button>
            </div>
            <div>
              <button
                onClick={() => setActiveSection('documents')}
                style={{
                  width: '100%',
                  textAlign: 'left',
                  padding: '12px',
                  backgroundColor: activeSection === 'documents' ? '#eff6ff' : 'transparent',
                  color: activeSection === 'documents' ? '#2563eb' : '#6b7280',
                  border: 'none',
                  borderRadius: '6px',
                  cursor: 'pointer',
                  fontWeight: '500',
                  fontSize: '14px',
                }}
              >
                📄 Documents & Licenses
              </button>
            </div>
          </div>

          {/* Content */}
          <div style={{ backgroundColor: 'white', padding: '30px', borderRadius: '8px', border: '1px solid #e5e7eb' }}>
            {activeSection === 'profile' && profile && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '20px' }}>Dealership Profile</h2>
                
                <div style={{ marginBottom: '20px' }}>
                  <div style={{ padding: '12px', backgroundColor: profile.verification_status === 'verified' ? '#d1fae5' : '#fef3c7', borderRadius: '6px', marginBottom: '20px' }}>
                    <strong>Status:</strong> {profile.verification_status === 'verified' ? '✅ Verified' : '⏳ Pending Verification'}
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '20px' }}>
                  <div>
                    <label style={labelStyle}>Company Name *</label>
                    <input
                      type="text"
                      value={profile.company_name}
                      onChange={(e) => setProfile({...profile, company_name: e.target.value})}
                      style={inputStyle}
                    />
                  </div>

                  <div>
                    <label style={labelStyle}>Dealership Name</label>
                    <input
                      type="text"
                      value={profile.dealership_name || ''}
                      onChange={(e) => setProfile({...profile, dealership_name: e.target.value})}
                      style={inputStyle}
                    />
                  </div>

                  <div>
                    <label style={labelStyle}>Dealer License Number *</label>
                    <input
                      type="text"
                      value={profile.license_number || ''}
                      onChange={(e) => setProfile({...profile, license_number: e.target.value})}
                      style={inputStyle}
                    />
                  </div>

                  <div>
                    <label style={labelStyle}>Phone Number *</label>
                    <input
                      type="tel"
                      value={profile.phone || ''}
                      onChange={(e) => setProfile({...profile, phone: e.target.value})}
                      style={inputStyle}
                    />
                  </div>

                  <div style={{ gridColumn: 'span 2' }}>
                    <label style={labelStyle}>Address</label>
                    <input
                      type="text"
                      value={profile.address || ''}
                      onChange={(e) => setProfile({...profile, address: e.target.value})}
                      style={inputStyle}
                    />
                  </div>

                  <div>
                    <label style={labelStyle}>City</label>
                    <input
                      type="text"
                      value={profile.city || ''}
                      onChange={(e) => setProfile({...profile, city: e.target.value})}
                      style={inputStyle}
                    />
                  </div>

                  <div>
                    <label style={labelStyle}>State</label>
                    <input
                      type="text"
                      value={profile.state || ''}
                      onChange={(e) => setProfile({...profile, state: e.target.value})}
                      style={inputStyle}
                      maxLength={2}
                    />
                  </div>

                  <div>
                    <label style={labelStyle}>ZIP Code</label>
                    <input
                      type="text"
                      value={profile.zip_code || ''}
                      onChange={(e) => setProfile({...profile, zip_code: e.target.value})}
                      style={inputStyle}
                    />
                  </div>

                  <div>
                    <label style={labelStyle}>Website</label>
                    <input
                      type="url"
                      value={profile.website || ''}
                      onChange={(e) => setProfile({...profile, website: e.target.value})}
                      style={inputStyle}
                      placeholder="https://"
                    />
                  </div>
                </div>

                <button
                  onClick={handleSaveProfile}
                  disabled={saving}
                  style={{
                    marginTop: '20px',
                    padding: '12px 30px',
                    backgroundColor: saving ? '#9ca3af' : '#2563eb',
                    color: 'white',
                    fontSize: '15px',
                    fontWeight: '600',
                    borderRadius: '6px',
                    border: 'none',
                    cursor: saving ? 'not-allowed' : 'pointer',
                  }}
                >
                  {saving ? 'Saving...' : 'Save Profile'}
                </button>
              </div>
            )}

            {activeSection === 'communication' && profile && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '10px' }}>Communication Preferences</h2>
                <p style={{ color: '#6b7280', marginBottom: '25px', fontSize: '14px' }}>
                  Configure AI-powered follow-up messages. Messages are generated automatically but you must review and click "Send" for each one.
                </p>

                <div style={{ marginBottom: '20px' }}>
                  <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer', padding: '15px', backgroundColor: '#f9fafb', borderRadius: '8px' }}>
                    <input
                      type="checkbox"
                      checked={profile.communication_preferences.auto_followup_enabled}
                      onChange={(e) => setProfile({
                        ...profile,
                        communication_preferences: {
                          ...profile.communication_preferences,
                          auto_followup_enabled: e.target.checked
                        }
                      })}
                      style={{ marginRight: '12px', width: '18px', height: '18px' }}
                    />
                    <div>
                      <div style={{ fontWeight: '600', fontSize: '15px' }}>Enable Auto-Generated Follow-ups</div>
                      <div style={{ fontSize: '13px', color: '#6b7280', marginTop: '4px' }}>AI will generate follow-up messages for you to review and send</div>
                    </div>
                  </label>
                </div>

                {profile.communication_preferences.auto_followup_enabled && (
                  <div style={{ marginLeft: '20px', paddingLeft: '20px', borderLeft: '3px solid #e5e7eb' }}>
                    <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '15px' }}>Follow-up Schedule</h3>
                    
                    <div style={{ marginBottom: '15px' }}>
                      <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                        <input
                          type="checkbox"
                          checked={profile.communication_preferences.followup_day_1}
                          onChange={(e) => setProfile({
                            ...profile,
                            communication_preferences: {
                              ...profile.communication_preferences,
                              followup_day_1: e.target.checked
                            }
                          })}
                          style={{ marginRight: '10px' }}
                        />
                        <span style={{ fontSize: '14px' }}><strong>Day 1:</strong> First follow-up (24 hours after initial contact)</span>
                      </label>
                    </div>

                    <div style={{ marginBottom: '15px' }}>
                      <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                        <input
                          type="checkbox"
                          checked={profile.communication_preferences.followup_day_3}
                          onChange={(e) => setProfile({
                            ...profile,
                            communication_preferences: {
                              ...profile.communication_preferences,
                              followup_day_3: e.target.checked
                            }
                          })}
                          style={{ marginRight: '10px' }}
                        />
                        <span style={{ fontSize: '14px' }}><strong>Day 3:</strong> Second follow-up (3 days after initial contact)</span>
                      </label>
                    </div>

                    <div style={{ marginBottom: '15px' }}>
                      <label style={{ display: 'flex', alignItems: 'center', cursor: 'pointer' }}>
                        <input
                          type="checkbox"
                          checked={profile.communication_preferences.followup_day_7}
                          onChange={(e) => setProfile({
                            ...profile,
                            communication_preferences: {
                              ...profile.communication_preferences,
                              followup_day_7: e.target.checked
                            }
                          })}
                          style={{ marginRight: '10px' }}
                        />
                        <span style={{ fontSize: '14px' }}><strong>Day 7:</strong> Final follow-up (1 week after initial contact)</span>
                      </label>
                    </div>
                  </div>
                )}

                <div style={{ marginTop: '25px', padding: '15px', backgroundColor: '#eff6ff', borderRadius: '8px', fontSize: '13px', color: '#1e40af' }}>
                  <strong>📋 Note:</strong> All AI-generated messages require your review and approval before being sent. You'll always have the opportunity to edit or decline sending any message.
                </div>

                <button
                  onClick={handleSaveCommunicationPrefs}
                  disabled={saving}
                  style={{
                    marginTop: '20px',
                    padding: '12px 30px',
                    backgroundColor: saving ? '#9ca3af' : '#2563eb',
                    color: 'white',
                    fontSize: '15px',
                    fontWeight: '600',
                    borderRadius: '6px',
                    border: 'none',
                    cursor: saving ? 'not-allowed' : 'pointer',
                  }}
                >
                  {saving ? 'Saving...' : 'Save Preferences'}
                </button>
              </div>
            )}

            {activeSection === 'documents' && (
              <div>
                <h2 style={{ fontSize: '20px', fontWeight: 'bold', marginBottom: '10px' }}>Documents & Licenses</h2>
                <p style={{ color: '#6b7280', marginBottom: '25px', fontSize: '14px' }}>
                  Upload your dealer license, insurance, and other required documents for verification.
                </p>

                <div style={{ padding: '40px', textAlign: 'center', backgroundColor: '#f9fafb', borderRadius: '8px', border: '2px dashed #d1d5db' }}>
                  <div style={{ fontSize: '48px', marginBottom: '10px' }}>📄</div>
                  <p style={{ color: '#6b7280', marginBottom: '15px' }}>Document upload feature coming soon</p>
                  <p style={{ fontSize: '13px', color: '#9ca3af' }}>For now, please email your documents to verification@revomotors.com</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}