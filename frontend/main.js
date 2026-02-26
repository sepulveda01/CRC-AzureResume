window.addEventListener("DOMContentLoaded", () => {
  getCount();
});

const functionApi =
  "https://rcfuncv2-g0c6dsb4exc4hcdm.westus-01.azurewebsites.net/api/counter";

async function getCount() {
  const el = document.getElementById("visit_count");
  if (!el) return;

  // Show placeholder while loading
  el.innerText = "—";

  try {
    const response = await fetch(functionApi, { method: "GET" });

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();

    if (data && typeof data.count === "number") {
      el.innerText = data.count;
    } else {
      el.innerText = "—";
    }

    console.log("Counter loaded successfully");
  } catch (error) {
    console.log("Counter fetch failed:", error);
    // Leave placeholder dash if API fails
  }
}
