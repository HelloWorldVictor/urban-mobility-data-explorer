# Urban Mobility Data Explorer - Frontend

A modern, responsive dashboard for exploring taxi trip data built with vanilla JavaScript, HTML, and CSS.

## Screenshots

![Screenshot 1](./docs/image-1.png)
![Screenshots 2](./docs/image-2.png)

## Features

### 📊 Statistics Dashboard

- **4 Key Metrics Cards**
  - Total Trips
  - Total Duration
  - Total Passengers
  - Average Trip Duration
- Real-time trend indicators (↗/↘)
- Clean, card-based layout

### 📈 Time Series Visualization

- Interactive line chart powered by Chart.js
- **Time Range Filters:**
  - Last 7 days (hourly granularity)
  - Last 30 days (daily granularity)
  - Last 3 months (daily granularity)
  - All time (full dataset)
- Smooth animations and hover tooltips
- Responsive design

### 📋 Data Table

- Paginated trip records (20 per page)
- **Easy Filters:**
  - Minimum passengers
  - Minimum duration
  - Vendor selection
- Clean, readable table design
- Sortable and filterable data

## Tech Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **Vanilla JavaScript** - No frameworks, just clean ES6+
- **Chart.js** - Beautiful, responsive charts
- **Fetch API** - RESTful API communication

## Getting Started

### Prerequisites

- Backend API running on `http://127.0.0.1:8000`
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Clone the Repository**

   ```bash
   git clone <https://github.com/HelloWorldVictor/urban-mobility-data-explorer.git>
   cd urban_mobility_data_explorer
    ```

2. **Copy Environment Configuration**

   If needed, copy `.env.example` to `.env` and adjust settings.

   ```bash
    cp .env.example .env
    ```

    then fill the `DB_URI` variable with a postgres connection string, e.g.:

    ```bash
    DB_URI=postgresql+psycopg2://username:password@localhost:5432/yourdatabase
    ```

3. **Start the Backend API** (if not already running)

   ```bash
   uv run fastapi dev backend/main.py
   ```

4. **Open the Frontend**

   **Option 1: Simple HTTP Server (Python)**

   ```bash
   cd frontend
   python3 -m http.server 8080
   ```

   Then open: <http://localhost:8080>

   **Option 2: VS Code Live Server**

- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

   **Option 3: Direct File Access**

- Open `frontend/index.html` directly in your browser
- Note: Some browsers may have CORS restrictions

## Project Structure

Top-level folders in this repository:

```bash
├── backend/ # Backend API code
├── data/ # Data cleaning and database seeding
└── frontend/ # This frontend dashboard
```

## API Integration

The frontend connects to these backend endpoints:

- `GET /api/analytics/stats` - Overall statistics
- `GET /api/analytics/time-series?time_range={range}` - Chart data
- `GET /api/trips?skip={n}&limit={m}&filters` - Trip records

## Customization

### Colors & Theme

Edit CSS variables in `styles.css`:

```css
:root {
    --primary-color: #3b82f6;      /* Blue */
    --success-color: #10b981;      /* Green */
    --danger-color: #ef4444;       /* Red */
    --background: #f8fafc;         /* Light gray */
    /* ... more variables */
}
```

### API URL

Change the API base URL in `app.js`:

```javascript
const API_BASE_URL = 'http://your-api-url:port';
```

### Chart Configuration

Modify chart settings in the `renderChart()` function in `app.js`:

```javascript
chart = new Chart(ctx, {
    type: 'line',  // or 'bar', 'area', etc.
    data: { /* ... */ },
    options: { /* customize here */ }
});
```

## Features in Detail

### Responsive Design

- **Desktop**: Multi-column layout with all features visible
- **Tablet**: Adaptive grid, stacked filters
- **Mobile**: Single column, touch-friendly controls

### Loading States

- Animated loading indicators
- Skeleton screens for stats cards
- Loading messages in table

### Error Handling

- Graceful API error handling
- User-friendly error messages
- Console logging for debugging

## Browser Support

- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ Opera 76+

## Performance

- **Initial Load**: ~500ms
- **Chart Update**: ~200ms
- **Table Load**: ~300ms (100 records)
- **Minimal Dependencies**: Only Chart.js (60KB gzipped)

## Future Enhancements

Potential improvements:

- [ ] Add geospatial map visualization
- [ ] Export data to CSV
- [ ] Advanced filtering (date ranges, location bounds)
- [ ] Real-time updates with WebSockets
- [ ] Dark mode toggle
- [ ] Custom chart types (bar, pie, heatmap)
- [ ] Mobile app version (PWA)
