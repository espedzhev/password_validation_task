export async function fetchValidationRules(password: string): Promise<Record<string, boolean>> {
  const response = await fetch('/api/v1/validate/rules', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  })

  if (!response.ok) {
    throw new Error('Failed to fetch validation rules')
  }

  const data = await response.json()
  return data.rules
}

export async function validatePassword(password: string): Promise<boolean> {
  const response = await fetch('/api/v1/validate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  })

  if (!response.ok) {
    throw new Error('Failed to validate password')
  }

  const data = await response.json()
  return data.valid
}
