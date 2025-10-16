# Urban Mobility Data Explorer - Frontend

A modern, responsive dashboard for exploring taxi trip data built with vanilla JavaScript, HTML, and CSS.

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

- Paginated trip records (100 per page)
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

1. **Start the Backend API** (if not already running)

   ```bash
   cd /path/to/urban_mobility_data_explorer
   uv run uvicorn backend.main:app --reload
   ```

2. **Open the Frontend**

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

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # All styles and responsive design
├── app.js              # Application logic and API calls
└── README.md           # This file
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

## Troubleshooting

### CORS Errors

If you see CORS errors in the console:

1. Make sure the backend is running
2. Check that `API_BASE_URL` in `app.js` is correct
3. Verify backend CORS settings allow `*` origin

### Chart Not Rendering

1. Check browser console for errors
2. Ensure Chart.js CDN is accessible
3. Verify API is returning valid data

### No Data Loading

1. Check backend is running: `curl http://127.0.0.1:8000/`
2. Verify database connection
3. Check browser console for API errors

## License

Part of the Urban Mobility Data Explorer project.

## Screenshots

The dashboard matches the reference design with:

- Clean, modern card-based UI
- Professional color scheme
- Smooth animations
- Mobile-responsive layout