// /api/geocode.js

export default async function handler(req, res) {
  if (req.method !== "GET" && req.method !== "POST") {
    return res.status(405).json({ error: "Method not allowed" });
  }

  // Adresi al (GET veya POST desteği)
  const address = req.method === "GET"
    ? req.query.text
    : req.body && req.body.text;

  if (!address) {
    return res.status(400).json({ error: "Missing address (text) parameter" });
  }

  const orsUrl = `https://api.openrouteservice.org/geocode/search?text=${encodeURIComponent(address)}`;

  try {
    const response = await fetch(orsUrl, {
      headers: {
        'Authorization': process.env.ORS_API_KEY
      }
    });
    const data = await response.json();
    console.log("ORS API response:", data); // <-- ekle

    console.log('ORS_API_KEY:', (process.env.ORS_API_KEY || '').slice(0,4) + '...' + (process.env.ORS_API_KEY || '').slice(-4));
    
    res.status(200).json(data);
  } catch (err) {
    res.status(500).json({ error: err.toString() });
  }
}
