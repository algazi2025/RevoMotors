import React from 'react';

export default function Home() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#ffffff', fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif' }}>
      <div style={{ backgroundColor: 'white', borderBottom: '1px solid #f0f0f0', padding: '20px 0', position: 'sticky', top: 0, zIndex: 1000, backdropFilter: 'blur(10px)', backgroundColor: 'rgba(255,255,255,0.95)' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '0 40px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '20px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ width: '42px', height: '42px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '22px' }}>🚗</div>
            <h1 style={{ fontSize: '26px', fontWeight: '700', margin: 0, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>RevoMotors</h1>
          </div>
          <div style={{ display: 'flex', gap: '35px', fontSize: '15px', alignItems: 'center', flexWrap: 'wrap' }}>
            <a href="#features" style={{ color: '#4a5568', textDecoration: 'none', fontWeight: '500', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#4a5568'}>Features</a>
            <a href="#how-it-works" style={{ color: '#4a5568', textDecoration: 'none', fontWeight: '500', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#4a5568'}>How It Works</a>
            <div style={{ height: '24px', width: '1px', backgroundColor: '#e2e8f0' }}></div>
            <a href="/dealer/login" style={{ color: '#667eea', textDecoration: 'none', fontWeight: '600', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#764ba2'} onMouseOut={(e) => e.currentTarget.style.color = '#667eea'}>Login</a>
            <a href="/dealer/register" style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', padding: '10px 24px', borderRadius: '8px', textDecoration: 'none', fontWeight: '600', boxShadow: '0 4px 15px rgba(102, 126, 234, 0.3)', transition: 'all 0.3s' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-2px)'; e.currentTarget.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.4)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.3)'; }}>Register</a>
          </div>
        </div>
      </div>
      <div style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', padding: '100px 40px', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: '-100px', right: '-100px', width: '400px', height: '400px', background: 'rgba(255,255,255,0.1)', borderRadius: '50%', filter: 'blur(60px)' }}></div>
        <div style={{ position: 'absolute', bottom: '-150px', left: '-150px', width: '500px', height: '500px', background: 'rgba(255,255,255,0.08)', borderRadius: '50%', filter: 'blur(80px)' }}></div>
        <div style={{ maxWidth: '1400px', margin: '0 auto', position: 'relative', zIndex: 1 }}>
          <div style={{ textAlign: 'center', marginBottom: '60px' }}>
            <h2 style={{ fontSize: '64px', fontWeight: '800', marginBottom: '24px', lineHeight: '1.15', color: 'white', textShadow: '0 2px 20px rgba(0,0,0,0.1)' }}>Sell Your Car with<br /><span style={{ background: 'linear-gradient(90deg, #ffffff 0%, #f0f0f0 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text' }}>AI-Powered Precision</span></h2>
            <p style={{ fontSize: '22px', color: 'rgba(255,255,255,0.95)', marginBottom: '50px', maxWidth: '750px', margin: '0 auto 50px', lineHeight: '1.7', fontWeight: '400' }}>Connect with verified dealers instantly. Get fair offers powered by advanced AI market analysis in just minutes.</p>
            <div style={{ display: 'flex', gap: '20px', justifyContent: 'center', flexWrap: 'wrap' }}>
              <a href="/seller/list-car" style={{ display: 'inline-block', padding: '20px 50px', backgroundColor: 'white', color: '#667eea', fontSize: '18px', fontWeight: '700', borderRadius: '12px', textDecoration: 'none', cursor: 'pointer', boxShadow: '0 8px 30px rgba(0,0,0,0.2)', transition: 'all 0.3s' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-3px) scale(1.02)'; e.currentTarget.style.boxShadow = '0 12px 40px rgba(0,0,0,0.25)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0) scale(1)'; e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.2)'; }}>I'm a Seller →</a>
              <a href="/dealer/login" style={{ display: 'inline-block', padding: '20px 50px', backgroundColor: 'rgba(255,255,255,0.15)', color: 'white', fontSize: '18px', fontWeight: '700', borderRadius: '12px', border: '2px solid rgba(255,255,255,0.3)', textDecoration: 'none', cursor: 'pointer', backdropFilter: 'blur(10px)', transition: 'all 0.3s' }} onMouseOver={(e) => { e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.25)'; e.currentTarget.style.transform = 'translateY(-3px)'; e.currentTarget.style.borderColor = 'rgba(255,255,255,0.5)'; }} onMouseOut={(e) => { e.currentTarget.style.backgroundColor = 'rgba(255,255,255,0.15)'; e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.borderColor = 'rgba(255,255,255,0.3)'; }}>I'm a Dealer</a>
            </div>
          </div>
        </div>
      </div>
      <div style={{ maxWidth: '1400px', margin: '-80px auto 0', padding: '0 40px', position: 'relative', zIndex: 2 }}>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '30px' }}>
          <div style={{ backgroundColor: 'white', padding: '45px 35px', borderRadius: '20px', textAlign: 'center', boxShadow: '0 20px 60px rgba(0,0,0,0.08)', transition: 'all 0.3s', cursor: 'pointer' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-8px)'; e.currentTarget.style.boxShadow = '0 25px 70px rgba(0,0,0,0.12)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 20px 60px rgba(0,0,0,0.08)'; }}>
            <div style={{ fontSize: '56px', fontWeight: '800', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: '12px' }}>15k+</div>
            <div style={{ color: '#64748b', fontSize: '17px', fontWeight: '600', letterSpacing: '0.5px' }}>Cars Sold</div>
          </div>
          <div style={{ backgroundColor: 'white', padding: '45px 35px', borderRadius: '20px', textAlign: 'center', boxShadow: '0 20px 60px rgba(0,0,0,0.08)', transition: 'all 0.3s', cursor: 'pointer' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-8px)'; e.currentTarget.style.boxShadow = '0 25px 70px rgba(0,0,0,0.12)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 20px 60px rgba(0,0,0,0.08)'; }}>
            <div style={{ fontSize: '56px', fontWeight: '800', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: '12px' }}>500+</div>
            <div style={{ color: '#64748b', fontSize: '17px', fontWeight: '600', letterSpacing: '0.5px' }}>Verified Dealers</div>
          </div>
          <div style={{ backgroundColor: 'white', padding: '45px 35px', borderRadius: '20px', textAlign: 'center', boxShadow: '0 20px 60px rgba(0,0,0,0.08)', transition: 'all 0.3s', cursor: 'pointer' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-8px)'; e.currentTarget.style.boxShadow = '0 25px 70px rgba(0,0,0,0.12)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 20px 60px rgba(0,0,0,0.08)'; }}>
            <div style={{ fontSize: '56px', fontWeight: '800', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text', marginBottom: '12px' }}>98%</div>
            <div style={{ color: '#64748b', fontSize: '17px', fontWeight: '600', letterSpacing: '0.5px' }}>Satisfaction Rate</div>
          </div>
        </div>
      </div>
      <div id="features" style={{ backgroundColor: '#fafafa', padding: '120px 40px', marginTop: '100px' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '80px' }}>
            <h2 style={{ fontSize: '48px', fontWeight: '800', marginBottom: '20px', color: '#1a202c' }}>Why Choose RevoMotors?</h2>
            <p style={{ fontSize: '20px', color: '#64748b', maxWidth: '650px', margin: '0 auto' }}>Cutting-edge technology meets exceptional service</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: '40px' }}>
            <div style={{ backgroundColor: 'white', padding: '45px 40px', borderRadius: '20px', boxShadow: '0 10px 40px rgba(0,0,0,0.06)', transition: 'all 0.3s', cursor: 'pointer' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-8px)'; e.currentTarget.style.boxShadow = '0 20px 60px rgba(102,126,234,0.15)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 10px 40px rgba(0,0,0,0.06)'; }}>
              <div style={{ width: '70px', height: '70px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '25px', fontSize: '32px', boxShadow: '0 8px 20px rgba(102,126,234,0.3)' }}>📈</div>
              <h3 style={{ fontSize: '24px', fontWeight: '700', color: '#1a202c', marginBottom: '16px' }}>AI-Powered Pricing</h3>
              <p style={{ color: '#64748b', lineHeight: '1.8', fontSize: '16px', margin: 0 }}>Get instant, accurate market valuations using advanced AI algorithms and real-time market data.</p>
            </div>
            <div style={{ backgroundColor: 'white', padding: '45px 40px', borderRadius: '20px', boxShadow: '0 10px 40px rgba(0,0,0,0.06)', transition: 'all 0.3s', cursor: 'pointer' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-8px)'; e.currentTarget.style.boxShadow = '0 20px 60px rgba(102,126,234,0.15)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 10px 40px rgba(0,0,0,0.06)'; }}>
              <div style={{ width: '70px', height: '70px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '25px', fontSize: '32px', boxShadow: '0 8px 20px rgba(102,126,234,0.3)' }}>👥</div>
              <h3 style={{ fontSize: '24px', fontWeight: '700', color: '#1a202c', marginBottom: '16px' }}>Verified Dealers Only</h3>
              <p style={{ color: '#64748b', lineHeight: '1.8', fontSize: '16px', margin: 0 }}>Connect with pre-screened, trusted dealers who are ready to make competitive offers.</p>
            </div>
            <div style={{ backgroundColor: 'white', padding: '45px 40px', borderRadius: '20px', boxShadow: '0 10px 40px rgba(0,0,0,0.06)', transition: 'all 0.3s', cursor: 'pointer' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-8px)'; e.currentTarget.style.boxShadow = '0 20px 60px rgba(102,126,234,0.15)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0)'; e.currentTarget.style.boxShadow = '0 10px 40px rgba(0,0,0,0.06)'; }}>
              <div style={{ width: '70px', height: '70px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: '16px', display: 'flex', alignItems: 'center', justifyContent: 'center', marginBottom: '25px', fontSize: '32px', boxShadow: '0 8px 20px rgba(102,126,234,0.3)' }}>✅</div>
              <h3 style={{ fontSize: '24px', fontWeight: '700', color: '#1a202c', marginBottom: '16px' }}>Fast & Secure</h3>
              <p style={{ color: '#64748b', lineHeight: '1.8', fontSize: '16px', margin: 0 }}>Complete transactions quickly with full GDPR and CCPA compliance for your peace of mind.</p>
            </div>
          </div>
        </div>
      </div>
      <div id="how-it-works" style={{ padding: '120px 40px', background: 'white' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '80px' }}>
            <h2 style={{ fontSize: '48px', fontWeight: '800', marginBottom: '20px', color: '#1a202c' }}>How It Works</h2>
            <p style={{ fontSize: '20px', color: '#64748b', maxWidth: '650px', margin: '0 auto' }}>Three simple steps to sell your car</p>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '50px' }}>
            <div style={{ textAlign: 'center', position: 'relative' }}>
              <div style={{ width: '100px', height: '100px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '42px', fontWeight: '800', margin: '0 auto 30px', boxShadow: '0 15px 40px rgba(102,126,234,0.4)', position: 'relative', zIndex: 1 }}>1</div>
              <h3 style={{ fontSize: '26px', fontWeight: '700', color: '#1a202c', marginBottom: '16px' }}>List Your Car</h3>
              <p style={{ color: '#64748b', lineHeight: '1.8', fontSize: '17px', maxWidth: '300px', margin: '0 auto' }}>Provide basic details about your vehicle in less than 2 minutes.</p>
            </div>
            <div style={{ textAlign: 'center', position: 'relative' }}>
              <div style={{ width: '100px', height: '100px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '42px', fontWeight: '800', margin: '0 auto 30px', boxShadow: '0 15px 40px rgba(102,126,234,0.4)', position: 'relative', zIndex: 1 }}>2</div>
              <h3 style={{ fontSize: '26px', fontWeight: '700', color: '#1a202c', marginBottom: '16px' }}>Get AI Offers</h3>
              <p style={{ color: '#64748b', lineHeight: '1.8', fontSize: '17px', maxWidth: '300px', margin: '0 auto' }}>Receive instant offers from multiple verified dealers powered by AI.</p>
            </div>
            <div style={{ textAlign: 'center', position: 'relative' }}>
              <div style={{ width: '100px', height: '100px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '42px', fontWeight: '800', margin: '0 auto 30px', boxShadow: '0 15px 40px rgba(102,126,234,0.4)', position: 'relative', zIndex: 1 }}>3</div>
              <h3 style={{ fontSize: '26px', fontWeight: '700', color: '#1a202c', marginBottom: '16px' }}>Close the Deal</h3>
              <p style={{ color: '#64748b', lineHeight: '1.8', fontSize: '17px', maxWidth: '300px', margin: '0 auto' }}>Choose the best offer and complete your sale securely online.</p>
            </div>
          </div>
        </div>
      </div>
      <div style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', padding: '100px 40px', position: 'relative', overflow: 'hidden' }}>
        <div style={{ position: 'absolute', top: '-50px', right: '-50px', width: '300px', height: '300px', background: 'rgba(255,255,255,0.1)', borderRadius: '50%', filter: 'blur(60px)' }}></div>
        <div style={{ maxWidth: '900px', margin: '0 auto', textAlign: 'center', position: 'relative', zIndex: 1 }}>
          <h2 style={{ fontSize: '46px', fontWeight: '800', color: 'white', marginBottom: '24px', textShadow: '0 2px 20px rgba(0,0,0,0.1)' }}>Ready to Sell Your Car?</h2>
          <p style={{ fontSize: '22px', color: 'rgba(255,255,255,0.95)', marginBottom: '40px', lineHeight: '1.7' }}>Join thousands of satisfied sellers who got the best value for their cars</p>
          <a href="/seller/list-car" style={{ display: 'inline-block', padding: '20px 50px', backgroundColor: 'white', color: '#667eea', fontSize: '19px', fontWeight: '700', borderRadius: '12px', textDecoration: 'none', cursor: 'pointer', boxShadow: '0 8px 30px rgba(0,0,0,0.2)', transition: 'all 0.3s' }} onMouseOver={(e) => { e.currentTarget.style.transform = 'translateY(-3px) scale(1.05)'; e.currentTarget.style.boxShadow = '0 12px 40px rgba(0,0,0,0.25)'; }} onMouseOut={(e) => { e.currentTarget.style.transform = 'translateY(0) scale(1)'; e.currentTarget.style.boxShadow = '0 8px 30px rgba(0,0,0,0.2)'; }}>Get Started Now →</a>
        </div>
      </div>
      <footer style={{ backgroundColor: '#1a202c', color: 'white', padding: '80px 40px 40px' }}>
        <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '50px', marginBottom: '60px' }}>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', marginBottom: '20px', gap: '12px' }}>
                <div style={{ width: '40px', height: '40px', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '20px' }}>🚗</div>
                <span style={{ fontSize: '22px', fontWeight: '700' }}>RevoMotors</span>
              </div>
              <p style={{ color: '#a0aec0', fontSize: '15px', lineHeight: '1.7', margin: 0 }}>The future of used car sales, powered by AI.</p>
            </div>
            <div>
              <h4 style={{ fontSize: '17px', fontWeight: '700', marginBottom: '20px', color: 'white' }}>For Sellers</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '12px' }}><a href="/seller/list-car" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>List Your Car</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#how-it-works" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>How It Works</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>Pricing</a></li>
              </ul>
            </div>
            <div>
              <h4 style={{ fontSize: '17px', fontWeight: '700', marginBottom: '20px', color: 'white' }}>For Dealers</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '12px' }}><a href="/dealer/register" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>Join as Dealer</a></li>
                <li style={{ marginBottom: '12px' }}><a href="/dealer/dashboard" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>Dashboard</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>API Docs</a></li>
              </ul>
            </div>
            <div>
              <h4 style={{ fontSize: '17px', fontWeight: '700', marginBottom: '20px', color: 'white' }}>Company</h4>
              <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>About Us</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>Privacy Policy</a></li>
                <li style={{ marginBottom: '12px' }}><a href="#" style={{ color: '#a0aec0', textDecoration: 'none', fontSize: '15px', transition: 'color 0.3s' }} onMouseOver={(e) => e.currentTarget.style.color = '#667eea'} onMouseOut={(e) => e.currentTarget.style.color = '#a0aec0'}>Terms of Service</a></li>
              </ul>
            </div>
          </div>
          <div style={{ borderTop: '1px solid #2d3748', paddingTop: '40px', textAlign: 'center' }}>
            <p style={{ color: '#a0aec0', fontSize: '15px', margin: 0 }}>© 2025 RevoMotors. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}