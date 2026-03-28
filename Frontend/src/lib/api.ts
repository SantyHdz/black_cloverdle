const BASE_URL = '/api';

export async function getDaily() {
  const res = await fetch(`${BASE_URL}/daily`);
  return res.json();
}

export async function sendGuess(nombre: string) {
  const res = await fetch(`${BASE_URL}/guess`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ nombre })
  });
  return res.json();
}

export async function searchCharacters(query: string) {
  const res = await fetch(`${BASE_URL}/characters/search?q=${encodeURIComponent(query)}`);
  return res.json();
}