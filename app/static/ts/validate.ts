import { getRulesConfig, getDetailedRules, getOverallValidity, RulesConfig } from './services/apiService.js'

const passwordInput = document.querySelector<HTMLInputElement>('#password-input')
const showPassword = document.querySelector<HTMLInputElement>('#show-password')
const showRulesToggle = document.querySelector<HTMLInputElement>('#show-rules')
const rulesList = document.querySelector<HTMLUListElement>('#rules-list')
const submitBtn = document.querySelector<HTMLButtonElement>('#submit-btn')
const responseBox = document.querySelector<HTMLDivElement>('#response')

let currentConfig: RulesConfig | null = null

function setInputColor(valid: boolean | null) {
  if (!passwordInput) return
  passwordInput.style.color = valid === null ? '' : valid ? 'green' : 'red'
}

function renderRulesConfig(config: RulesConfig) {
  if (!rulesList) return

  const items = [
    config.min_length !== null ? `Must be more than ${config.min_length} characters long` : null,
    config.require_uppercase ? 'Must contain at least one uppercase letter' : null,
    config.require_lowercase ? 'Must contain at least one lowercase letter' : null,
    config.require_digit ? 'Must contain at least one digit' : null,
    config.require_underscore ? 'Must contain at least one underscore (_)' : null,
  ].filter(Boolean) as string[]

  rulesList.innerHTML = items.length ? items.map((t) => `<li>${t}</li>`).join('') : '<li>No rules enabled.</li>'
}

function buildLabelMap(config: RulesConfig | null): Record<string, string> {
  if (!config) return {}
  return {
    ...(config.min_length !== null ? { min_length: `Must be more than ${config.min_length} characters long` } : {}),
    ...(config.require_uppercase ? { require_uppercase: 'Must contain at least one uppercase letter' } : {}),
    ...(config.require_lowercase ? { require_lowercase: 'Must contain at least one lowercase letter' } : {}),
    ...(config.require_digit ? { require_digit: 'Must contain at least one digit' } : {}),
    ...(config.require_underscore ? { require_underscore: 'Must contain at least one underscore (_)' } : {}),
  }
}

async function updateDetailed(password: string) {
  if (!rulesList || !submitBtn) return

  if (!showRulesToggle?.checked) {
    rulesList.classList.add('hidden')
    rulesList.innerHTML = ''
    try {
      const valid = password ? await getOverallValidity(password) : false
      // submitBtn.disabled = !valid;
      setInputColor(password ? valid : null)
    } catch {
      // submitBtn.disabled = true;
      setInputColor(null)
    }
    return
  }

  rulesList.classList.remove('hidden')
  rulesList.innerHTML = '<li>Checking...</li>'
  // submitBtn.disabled = true;

  try {
    const rules = await getDetailedRules(password)

    const labelMap = buildLabelMap(currentConfig)
    const order = [
      'min_length',
      'require_uppercase',
      'require_lowercase',
      'require_digit',
      'require_underscore',
    ] as const

    const filtered = order
      .map((key) =>
        key in rules && key in labelMap ? { key, passed: rules[key] as boolean, label: labelMap[key] } : null,
      )
      .filter(Boolean) as Array<{ key: string; passed: boolean; label: string }>

    const allPassed = filtered.length ? filtered.every((item) => item.passed) : false

    rulesList.innerHTML = filtered
      .map((item) => `<li style="color:${item.passed ? 'green' : 'red'}">${item.label}</li>`)
      .join('')

    // submitBtn.disabled = !allPassed;
    setInputColor(password ? allPassed : null)
  } catch {
    rulesList.innerHTML = '<li style="color:red">Error fetching validation rules.</li>'
    // submitBtn.disabled = true;
    setInputColor(null)
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  if (!passwordInput || !showPassword || !showRulesToggle || !rulesList || !submitBtn || !responseBox) return

  try {
    currentConfig = await getRulesConfig()
    renderRulesConfig(currentConfig)
  } catch {
    rulesList.innerHTML = '<li style="color:red">Failed to load current rules.</li>'
  }

  if (!showRulesToggle.checked) {
    rulesList.classList.add('hidden')
    rulesList.innerHTML = ''
  } else {
    rulesList.classList.remove('hidden')
  }

  if (passwordInput.value) {
    await updateDetailed(passwordInput.value)
  }

  passwordInput.addEventListener('input', async () => {
    const pwd = passwordInput.value
    await updateDetailed(pwd)
  })

  showPassword.addEventListener('change', () => {
    passwordInput.type = showPassword.checked ? 'text' : 'password'
  })

  showRulesToggle.addEventListener('change', async () => {
    if (showRulesToggle.checked) {
      rulesList.classList.remove('hidden')
      try {
        currentConfig = await getRulesConfig()
        renderRulesConfig(currentConfig)
      } catch {
        rulesList.innerHTML = '<li style="color:red">Failed to load current rules.</li>'
      }
    } else {
      rulesList.classList.add('hidden')
      rulesList.innerHTML = ''
    }
    await updateDetailed(passwordInput.value)
  })

  document.querySelector<HTMLFormElement>('#password-form')?.addEventListener('submit', async (e) => {
    e.preventDefault()
    responseBox.textContent = ''

    try {
      const valid = await getOverallValidity(passwordInput.value)
      responseBox.textContent = valid ? 'Your password is valid.' : 'Your password is invalid.'
      responseBox.style.color = valid ? 'green' : 'red'
    } catch {
      responseBox.textContent = 'Error validating password.'
      responseBox.style.color = 'red'
    }
  })
})
