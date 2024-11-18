import { fetchValidationRules, validatePassword } from './services/apiService.js'

const rulesList = document.getElementById('rules')!
const responseDiv = document.getElementById('response')!
const passwordInput = document.getElementById('passwordInput') as HTMLInputElement
const showPasswordCheckbox = document.getElementById('showPassword') as HTMLInputElement
const submitButton = document.querySelector<HTMLButtonElement>('button[type="submit"]')!
const form = document.getElementById('passwordForm') as HTMLFormElement

let debounceTimer: ReturnType<typeof setTimeout> | undefined

function togglePasswordVisibility(): void {
  passwordInput.type = showPasswordCheckbox.checked ? 'text' : 'password'
}

// Handle errors
function handleError(message: string): void {
  console.error(message)
  responseDiv.textContent = message
  responseDiv.style.color = 'red'
  submitButton.disabled = true
}

// Update rules dynamically
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
    handleError('Error fetching validation rules.')
  }
}

// Handle form submission
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
    handleError('Error validating password.')
  }
}

// Debounce function
function debounce<T extends (...args: any[]) => void>(func: T, delay: number): (...args: Parameters<T>) => void {
  return (...args: Parameters<T>) => {
    if (debounceTimer) clearTimeout(debounceTimer)
    debounceTimer = setTimeout(() => func(...args), delay)
  }
}

document.addEventListener('DOMContentLoaded', () => {
  showPasswordCheckbox.addEventListener('change', togglePasswordVisibility)

  const debouncedUpdateRules = debounce(async (event: Event) => {
    const password = (event.target as HTMLInputElement).value
    await updateRules(password)
  }, 300)

  passwordInput.addEventListener('input', debouncedUpdateRules)

  form?.addEventListener('submit', handleFormSubmit)
})
