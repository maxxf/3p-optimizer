import { useState } from "react"

export default function Landing() {
  const [email, setEmail] = useState("")
  const [resto, setResto] = useState("")
  const [urls, setUrls] = useState({ ub: "", dd: "" })

  const handleSubmit = async () => {
    const res = await fetch("/api/submit", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        email,
        restaurant_name: resto,
        doordash_url: urls.dd,
        ubereats_url: urls.ub
      })
    })
    const data = await res.json()
    window.location.href = data.report_url
  }

  return (
    <div className="p-8 max-w-xl mx-auto text-center">
      <h1 className="text-3xl font-bold mb-4">Is Your Delivery Menu Costing You Sales?</h1>
      <p className="mb-4">Get a free storefront audit of your Uber Eats & DoorDash pages.</p>
      <input className="mb-2 w-full p-2 border" placeholder="Restaurant Name" onChange={(e) => setResto(e.target.value)} />
      <input className="mb-2 w-full p-2 border" placeholder="Your Email" onChange={(e) => setEmail(e.target.value)} />
      <input className="mb-2 w-full p-2 border" placeholder="Uber Eats URL" onChange={(e) => setUrls({...urls, ub: e.target.value})} />
      <input className="mb-4 w-full p-2 border" placeholder="DoorDash URL" onChange={(e) => setUrls({...urls, dd: e.target.value})} />
      <button className="bg-black text-white py-2 px-4 rounded" onClick={handleSubmit}>Get My Report</button>
    </div>
  )
}
