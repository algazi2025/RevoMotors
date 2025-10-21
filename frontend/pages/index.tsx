import Link from 'next/link'
export default function Home() {
  return (
    <div style={{padding: '2rem', textAlign: 'center'}}>
      <h1>Used Car AI Platform</h1>
      <Link href="/seller/landing"><button>I'm a Seller</button></Link>
      <Link href="/dealer/landing"><button>I'm a Dealer</button></Link>
    </div>
  )
}
