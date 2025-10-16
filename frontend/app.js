// API Configuration
const API_BASE_URL = "http://127.0.0.1:8000";

// State
let currentPage = 1;
let currentFilters = {
  min_passengers: null,
  min_duration: null,
  vendor_id: null,
};
let currentTimeRange = "3m";
let chart = null;

// Initialize app
document.addEventListener("DOMContentLoaded", () => {
  initializeEventListeners();
  Promise.all([
    loadStatistics(),
    loadTimeSeriesChart(currentTimeRange),
    loadTrips(),
  ]);
});

// Event Listeners
function initializeEventListeners() {
  // Time range buttons
  document.querySelectorAll(".time-btn").forEach((btn) => {
    btn.addEventListener("click", (e) => {
      document
        .querySelectorAll(".time-btn")
        .forEach((b) => b.classList.remove("active"));
      e.target.classList.add("active");
      currentTimeRange = e.target.dataset.range;
      loadTimeSeriesChart(currentTimeRange);
    });
  });

  // Filter buttons
  document
    .getElementById("apply-filters")
    .addEventListener("click", applyFilters);
  document
    .getElementById("reset-filters")
    .addEventListener("click", resetFilters);

  // Pagination
  document.getElementById("prev-page").addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      loadTrips();
    }
  });

  document.getElementById("next-page").addEventListener("click", () => {
    currentPage++;
    loadTrips();
  });

  // Enter key on filter inputs
  document.querySelectorAll(".table-filters input").forEach((input) => {
    input.addEventListener("keypress", (e) => {
      if (e.key === "Enter") applyFilters();
    });
  });
}

// API Calls
async function loadStatistics() {
  try {
    const response = await fetch(`${API_BASE_URL}/api/analytics/stats`);
    const data = await response.json();

    if (data.success) {
      const stats = data.data;

      // Update stat cards
      document.getElementById("total-trips").textContent =
        stats.total_trips.toLocaleString();
      document.getElementById("total-duration").textContent = formatDuration(
        stats.total_duration
      );
      document.getElementById("total-passengers").textContent =
        stats.total_passengers.toLocaleString();

      const avgDuration = stats.total_duration / stats.total_trips;
      document.getElementById("avg-duration").textContent =
        formatDuration(avgDuration);
    }
  } catch (error) {
    console.error("Error loading statistics:", error);
    showError("Failed to load statistics");
  }
}

async function loadTimeSeriesChart(timeRange) {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/analytics/time-series?time_range=${timeRange}`
    );
    const data = await response.json();

    if (data.success) {
      renderChart(data.data);
    }
  } catch (error) {
    console.error("Error loading time series:", error);
    showError("Failed to load chart data");
  }
}

async function loadTrips() {
  const tbody = document.getElementById("trips-tbody");
  tbody.innerHTML =
    '<tr><td colspan="8" class="loading">Loading trips...</td></tr>';

  try {
    const params = new URLSearchParams({
      skip: (currentPage - 1) * 20,
      limit: 20,
      sort_by: "pickup_datetime",
      sort_order: "desc",
    });

    // Apply filters
    if (currentFilters.min_passengers) {
      params.append("min_passengers", currentFilters.min_passengers);
    }
    if (currentFilters.min_duration) {
      params.append("min_duration", currentFilters.min_duration);
    }
    if (currentFilters.vendor_id) {
      params.append("vendor_id", currentFilters.vendor_id);
    }

    const response = await fetch(`${API_BASE_URL}/api/trips?${params}`);
    const data = await response.json();

    if (data.success && data.data.length > 0) {
      renderTripsTable(data.data);
      updatePagination(data.pagination);
    } else {
      tbody.innerHTML =
        '<tr><td colspan="8" class="loading">No trips found</td></tr>';
    }
  } catch (error) {
    console.error("Error loading trips:", error);
    tbody.innerHTML =
      '<tr><td colspan="8" class="loading">Error loading trips</td></tr>';
  }
}

// Rendering Functions
function renderChart(data) {
  const ctx = document.getElementById("timeSeriesChart").getContext("2d");

  // Destroy existing chart
  if (chart) {
    chart.destroy();
  }

  const labels = data.map((point) => {
    const date = new Date(point.timestamp);
    if (currentTimeRange === "7d") {
      return date.toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
        hour: "2-digit",
      });
    }
    return date.toLocaleDateString("en-US", { month: "short", day: "numeric" });
  });

  const tripCounts = data.map((point) => point.trip_count);

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [
        {
          label: "Trip Count",
          data: tripCounts,
          borderColor: "#3b82f6",
          backgroundColor: "rgba(59, 130, 246, 0.1)",
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointRadius: 2,
          pointHoverRadius: 5,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          display: false,
        },
        tooltip: {
          mode: "index",
          intersect: false,
          backgroundColor: "rgba(0, 0, 0, 0.8)",
          padding: 12,
          titleFont: {
            size: 14,
          },
          bodyFont: {
            size: 13,
          },
          callbacks: {
            label: function (context) {
              return `Trips: ${context.parsed.y.toLocaleString()}`;
            },
          },
        },
      },
      scales: {
        x: {
          grid: {
            display: false,
          },
          ticks: {
            maxRotation: 45,
            minRotation: 45,
            font: {
              size: 11,
            },
          },
        },
        y: {
          beginAtZero: true,
          grid: {
            color: "rgba(0, 0, 0, 0.05)",
          },
          ticks: {
            callback: function (value) {
              return value.toLocaleString();
            },
          },
        },
      },
      interaction: {
        mode: "nearest",
        axis: "x",
        intersect: false,
      },
    },
  });
}

function renderTripsTable(trips) {
  const tbody = document.getElementById("trips-tbody");
  tbody.innerHTML = "";

  trips.forEach((trip) => {
    const row = document.createElement("tr");
    row.innerHTML = `
            <td><code>${trip.id.substring(0, 8)}...</code></td>
            <td><span class="status-badge ${
              trip.vendor_id === 1 ? "success" : "warning"
            }">Vendor ${trip.vendor_id}</span></td>
            <td>${formatDateTime(trip.pickup_datetime)}</td>
            <td>${formatDateTime(trip.dropoff_datetime)}</td>
            <td>${formatDuration(trip.trip_duration)}</td>
            <td>${trip.passenger_count}</td>
            <td>${formatCoordinates(
              trip.pickup_latitude,
              trip.pickup_longitude
            )}</td>
            <td>${formatCoordinates(
              trip.dropoff_latitude,
              trip.dropoff_longitude
            )}</td>
        `;
    tbody.appendChild(row);
  });
}

// Filter Functions
function applyFilters() {
  currentFilters = {
    min_passengers: document.getElementById("filter-passengers").value || null,
    min_duration: document.getElementById("filter-duration").value || null,
    vendor_id: document.getElementById("filter-vendor").value || null,
  };
  currentPage = 1;
  loadTrips();
}

function resetFilters() {
  document.getElementById("filter-passengers").value = "";
  document.getElementById("filter-duration").value = "";
  document.getElementById("filter-vendor").value = "";
  currentFilters = {
    min_passengers: null,
    min_duration: null,
    vendor_id: null,
  };
  currentPage = 1;
  loadTrips();
}

// Pagination
function updatePagination(pagination) {
  // Update page info with comprehensive details
  const { page, total_pages, total, page_size, has_next, has_prev } =
    pagination;

  const startRecord = (page - 1) * page_size + 1;
  const endRecord = Math.min(page * page_size, total);

  document.getElementById("page-info").innerHTML = `
    Page <strong>${page}</strong> of <strong>${total_pages.toLocaleString()}</strong> 
    <span class="pagination-details">(${startRecord.toLocaleString()}-${endRecord.toLocaleString()} of ${total.toLocaleString()} trips)</span>
  `;

  // Update button states
  document.getElementById("prev-page").disabled = !has_prev;
  document.getElementById("next-page").disabled = !has_next;

  // Update current page for global state
  currentPage = page;
}

// Utility Functions
function formatDuration(seconds) {
  if (!seconds || isNaN(seconds)) return "0s";

  const years = Math.floor(seconds / (365 * 24 * 3600));
  seconds %= 365 * 24 * 3600;
  const months = Math.floor(seconds / (30 * 24 * 3600));
  seconds %= 30 * 24 * 3600;
  const days = Math.floor(seconds / (24 * 3600));
  seconds %= 24 * 3600;
  const hours = Math.floor(seconds / 3600);
  seconds %= 3600;
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);

  let parts = [];
  if (years > 0) parts.push(`${years}y`);
  if (months > 0) parts.push(`${months}mo`);
  if (days > 0) parts.push(`${days}d`);
  if (hours > 0) parts.push(`${hours}h`);
  if (minutes > 0) parts.push(`${minutes}m`);
  if (secs > 0 || parts.length === 0) parts.push(`${secs}s`);

  // Show only the first 2 non-zero categories
  const filtered = parts.filter((part) => !part.startsWith("0"));
  return filtered.slice(0, 2).join(" ") || "0s";
}

function formatDateTime(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatCoordinates(lat, lon) {
  return `${lat.toFixed(3)}, ${lon.toFixed(3)}`;
}

function showError(message) {
  console.error(message);
  // You could add a toast notification here
}
