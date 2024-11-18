import { fetchValidationRules, validatePassword } from './services/apiService.js'

// DOM Elements
const rulesList = document.getElementById('rules')!
const responseDiv = document.getElementById('response')!
const passwordInput = document.getElementById('password') as HTMLInputElement
const submitButton = document.querySelector<HTMLButtonElement>('button[type="submit"]')!
const form = document.getElementById('passwordForm') as HTMLFormElement

let debounceTimer: ReturnType<typeof setTimeout> | undefined

async function updateRules(password: string): Promise<void> {
  try {
    rulesList.innerHTML = '<li>Loading...</li>'
    submitButton.disabled = true

    const rules = await fetchValidationRules(password)

    rulesList.innerHTML = ''
    let allRulesPassed = true

    for (const [rule, passed] of Object.entries(rules)) {
      const li = document.createElement('li')
      li.textContent = `${rule.replace('_', ' ')}: ${passed ? '✅' : '❌'}`
      li.style.color = passed ? 'green' : 'red'
      rulesList.appendChild(li)

      if (!passed) {
        allRulesPassed = false
      }
    }

    submitButton.disabled = !allRulesPassed
  } catch (error) {
    console.error('Error updating rules:', error)
    rulesList.innerHTML = '<li>Error loading rules.</li>'
    responseDiv.textContent = 'Error fetching validation rules.'
    responseDiv.style.color = 'red'
    submitButton.disabled = true
  }
}

async function handleFormSubmit(event: Event): Promise<void> {
  event.preventDefault()

  try {
    const password = passwordInput.value.trim()
    const isValid = await validatePassword(password)

    responseDiv.textContent = isValid
      ? '✅ Your password is valid!'
      : '❌ Your password is invalid!'
    responseDiv.style.color = isValid ? 'green' : 'red'
  } catch (error) {
    console.error('Error validating password:', error)
    responseDiv.textContent = 'Error validating password.'
    responseDiv.style.color = 'red'
  }
}

function debounce(func: (...args: any[]) => void, delay: number): (...args: any[]) => void {
  return (...args: any[]) => {
    if (debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => func(...args), delay)
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const debouncedUpdateRules = debounce(async (event: Event) => {
    const password = (event.target as HTMLInputElement).value
    await updateRules(password)
  }, 300)

  passwordInput.addEventListener('input', debouncedUpdateRules)

  form?.addEventListener('submit', handleFormSubmit)
})
