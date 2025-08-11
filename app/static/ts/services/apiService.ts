export type RulesConfig = {
  min_length: number | null
  require_uppercase: boolean
  require_lowercase: boolean
  require_digit: boolean
  require_underscore: boolean
}

type DetailedRulesResponse = { rules: Record<string, boolean> }
type OverallValidityResponse = { valid: boolean }

export async function getRulesConfig(): Promise<RulesConfig> {
  const res = await fetch('/api/v1/rules')

  if (!res.ok) throw new Error('Failed to load rules')

  return res.json()
}

export async function getDetailedRules(password: string): Promise<Record<string, boolean>> {
  const res = await fetch('/api/v1/validate/rules', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  })

  if (!res.ok) throw new Error('Failed to fetch validation rules')

  const data: DetailedRulesResponse = await res.json()

  return data.rules
}

export async function getOverallValidity(password: string): Promise<boolean> {
  const res = await fetch('/api/v1/validate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ password }),
  })

  if (!res.ok) throw new Error('Failed to validate password')

  const data: OverallValidityResponse = await res.json()

  return data.valid
}