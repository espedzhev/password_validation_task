const form = document.querySelector<HTMLFormElement>("#passwordForm");
const responseDiv = document.querySelector<HTMLDivElement>("#response");

form?.addEventListener("submit", async (event) => {
    event.preventDefault();

    // Get the entered password
    const passwordInput = document.querySelector<HTMLInputElement>("#password");
    const password = passwordInput?.value || "";

    // Send the password to the server for validation
    const response = await fetch("/validate", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ password }),
    });

    const result = await response.json();

    // Display the validation result
    responseDiv!.textContent = result.valid
        ? "✅ Your password is valid!"
        : "❌ Your password is invalid!";
});
