const BASE_URL = "http://127.0.0.1:8001";

const dashboardType = document.getElementById("dashboardType");
const entityDropdown = document.getElementById("entityDropdown");
const entityDropdownGroup = document.getElementById("entityDropdownGroup");
const loadBtn = document.getElementById("loadBtn");
const chartsContainer = document.getElementById("chartsContainer");
const todayBanner = document.getElementById("todayBanner");
const kpiContainer = document.getElementById("kpiContainer");

let charts = [];

// Custom Searchable Dropdown state and DOM references
const searchInput = document.getElementById("searchableSelectSearch");
const selectTrigger = document.getElementById("searchableSelectTrigger");
const selectContainer = document.getElementById("searchableSelect");
const selectedText = document.getElementById("selectedEntityText");
const optionsContainer = document.getElementById("searchableSelectOptions");

let currentDropdownOptions = [];

// Toggle dropdown active class and focus input
if (selectTrigger) {
    selectTrigger.addEventListener("click", (e) => {
        e.stopPropagation();
        selectContainer.classList.toggle("active");
        if (selectContainer.classList.contains("active")) {
            searchInput.value = "";
            filterDropdownOptions("");
            searchInput.focus();
        }
    });
}

// Close searchable dropdown on clicking outside
document.addEventListener("click", (e) => {
    if (selectContainer && !selectContainer.contains(e.target)) {
        selectContainer.classList.remove("active");
    }
});

// Filter items on input typing
if (searchInput) {
    searchInput.addEventListener("input", (e) => {
        filterDropdownOptions(e.target.value);
    });
}

// Populate options in searchable select
function populateSearchableOptions(items) {
    currentDropdownOptions = items;
    renderSearchableOptions(items);
    
    if (items.length > 0) {
        selectEntityItem(items[0]);
    } else {
        selectedText.textContent = "Select...";
        entityDropdown.value = "";
    }
}

// Render option items list
function renderSearchableOptions(items, filterText = "") {
    if (!optionsContainer) return;
    optionsContainer.innerHTML = "";
    
    const filtered = items.filter(item => 
        item.toLowerCase().includes(filterText.toLowerCase())
    );
    
    if (filtered.length === 0) {
        const noResults = document.createElement("div");
        noResults.className = "searchable-option no-results";
        noResults.textContent = "No matches found";
        optionsContainer.appendChild(noResults);
        return;
    }
    
    filtered.forEach(item => {
        const div = document.createElement("div");
        div.className = "searchable-option";
        if (entityDropdown.value === item) {
            div.classList.add("selected");
        }
        div.textContent = item;
        
        div.addEventListener("click", (e) => {
            e.stopPropagation();
            selectEntityItem(item);
            selectContainer.classList.remove("active");
        });
        
        optionsContainer.appendChild(div);
    });
}

// Select specific item and update native dropdown
function selectEntityItem(value) {
    entityDropdown.value = value;
    selectedText.textContent = value;
    
    const optionDivs = optionsContainer.querySelectorAll(".searchable-option");
    optionDivs.forEach(div => {
        if (div.textContent === value) {
            div.classList.add("selected");
        } else {
            div.classList.remove("selected");
        }
    });
}

// Filter the list of options
function filterDropdownOptions(query) {
    renderSearchableOptions(currentDropdownOptions, query);
}

// Global Chart.js configuration defaults for professional UI
if (window.Chart) {
    // Register the datalabels plugin globally
    if (window.ChartDataLabels) {
        Chart.register(window.ChartDataLabels);
        Chart.defaults.plugins.datalabels = {
            display: false // Disable by default for line charts and dense bar charts
        };
    }

    Chart.defaults.font.family = "'Plus Jakarta Sans', 'Inter', sans-serif";
    Chart.defaults.color = "#64748b"; // slate-500
    Chart.defaults.plugins.legend.labels.boxWidth = 12;
    Chart.defaults.plugins.legend.labels.boxHeight = 12;
    Chart.defaults.plugins.legend.labels.usePointStyle = true;
    Chart.defaults.plugins.legend.labels.padding = 16;

    // Nice tooltip styles
    Chart.defaults.plugins.tooltip.backgroundColor = "#0f172a"; // slate-900
    Chart.defaults.plugins.tooltip.titleFont = { size: 13, weight: '600' };
    Chart.defaults.plugins.tooltip.bodyFont = { size: 12 };
    Chart.defaults.plugins.tooltip.padding = 10;
    Chart.defaults.plugins.tooltip.cornerRadius = 8;
    Chart.defaults.plugins.tooltip.displayColors = true;
}

// Helper to convert hex to RGBA
function hexToRGBA(hex, alpha) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
}

// Chart theme colors (darker solid gradients to ensure white text visibility)
const THEME_COLORS = {
    indigo: {
        border: '#1e1b4b',
        gradientStart: '#4338ca',
        gradientEnd: '#2e2a87'
    },
    violet: {
        border: '#2e1065',
        gradientStart: '#6d28d9',
        gradientEnd: '#4c1d95'
    },
    emerald: {
        border: '#022c22',
        gradientStart: '#047857',
        gradientEnd: '#064e3b'
    },
    rose: {
        border: '#4c0519',
        gradientStart: '#be123c',
        gradientEnd: '#881337'
    },
    amber: {
        border: '#451a03',
        gradientStart: '#b45309',
        gradientEnd: '#78350f'
    },
    sky: {
        border: '#082f49',
        gradientStart: '#0369a1',
        gradientEnd: '#0c4a6e'
    }
};


// Helper to get linear gradient
function getCanvasGradient(canvasId, colorTheme) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return 'rgba(99, 102, 241, 0.85)';
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    const theme = THEME_COLORS[colorTheme] || THEME_COLORS.indigo;
    gradient.addColorStop(0, theme.gradientStart);
    gradient.addColorStop(1, theme.gradientEnd);
    return gradient;
}

// Helper to get line background gradient (more transparent)
function getLineFillGradient(canvasId, colorTheme) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return 'rgba(99, 102, 241, 0.1)';
    const ctx = canvas.getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 300);
    const theme = THEME_COLORS[colorTheme] || THEME_COLORS.indigo;
    gradient.addColorStop(0, hexToRGBA(theme.gradientStart, 0.25));
    gradient.addColorStop(1, hexToRGBA(theme.gradientEnd, 0.0));
    return gradient;
}

async function loadDropdown() {
    entityDropdown.innerHTML = "";
    const type = dashboardType.value;

    if (type === "main") {
        entityDropdownGroup.style.display = "none";
        return;
    }

    entityDropdownGroup.style.display = "flex";

    let endpoint = "";
    if (type === "unit") endpoint = "/unit/list";
    if (type === "department") endpoint = "/department/list";
    if (type === "checklist") endpoint = "/checklist/list";

    try {
        const response = await fetch(BASE_URL + endpoint);
        const data = await response.json();

        entityDropdown.innerHTML = "";
        data.forEach(item => {
            const option = document.createElement("option");
            option.value = item;
            option.textContent = item;
            entityDropdown.appendChild(option);
        });

        // Populate custom searchable select options
        populateSearchableOptions(data);
    } catch (err) {
        console.error("Error loading dropdown items:", err);
    }
}

dashboardType.addEventListener("change", loadDropdown);
loadDropdown();

function formatDate(dateStr) {
    if (!dateStr) return "";
    const date = new Date(dateStr);
    return date.toLocaleDateString("en-GB", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric"
    });
}

function destroyCharts() {
    charts.forEach(chart => chart.destroy());
    charts = [];
    
    // Reset all scroll containers to 100% width
    const scrollContainers = document.querySelectorAll('.chart-scroll-container');
    scrollContainers.forEach(container => {
        container.style.width = '100%';
    });
}

function adjustScrollContainer(id, itemCount, barGroupWidth = 35) {
    const canvas = document.getElementById(id);
    if (!canvas) return;
    const scrollContainer = canvas.parentNode;
    if (!scrollContainer || !scrollContainer.classList.contains('chart-scroll-container')) return;
    
    const minWidth = itemCount * barGroupWidth;
    const parentWidth = scrollContainer.parentNode.clientWidth || scrollContainer.parentNode.getBoundingClientRect().width;
    
    if (minWidth > parentWidth) {
        scrollContainer.style.width = minWidth + 'px';
    } else {
        scrollContainer.style.width = '100%';
    }
}

// Generate beautiful curved line chart
function createLineChart(id, labels, data, title, colorTheme = 'indigo') {
    const theme = THEME_COLORS[colorTheme] || THEME_COLORS.indigo;
    return new Chart(
        document.getElementById(id),
        {
            type: "line",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: title,
                        data: data,
                        borderColor: theme.border,
                        backgroundColor: getLineFillGradient(id, colorTheme),
                        borderWidth: 3,
                        fill: true,
                        tension: 0.35,
                        pointBackgroundColor: theme.border,
                        pointBorderColor: '#ffffff',
                        pointBorderWidth: 2,
                        pointRadius: 4,
                        pointHoverRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 0,
                            font: { size: 10 }
                        }
                    },
                    y: {
                        border: { dash: [5, 5] },
                        grid: { color: '#f1f5f9' },
                        beginAtZero: true
                    }
                }
            }
        }
    );
}

// Dynamic helper for chart datalabels configuration
function getDatalabelConfig(showLabels = true, forceVerticalInside = null) {
    if (!showLabels) return { display: false };
    
    return {
        display: true,
        anchor: function(context) {
            const itemCount = context.chart.data.labels.length;
            const autoVerticalLimit = 10;
            const useVerticalInside = forceVerticalInside !== null 
                ? forceVerticalInside 
                : (itemCount > autoVerticalLimit);
            
            if (!useVerticalInside) return 'end';
            const value = context.dataset.data[context.dataIndex];
            const maxVal = Math.max(...context.dataset.data.map(v => Number(v) || 0), 1);
            return (value / maxVal) < 0.20 ? 'end' : 'center';
        },
        align: function(context) {
            const itemCount = context.chart.data.labels.length;
            const autoVerticalLimit = 10;
            const useVerticalInside = forceVerticalInside !== null 
                ? forceVerticalInside 
                : (itemCount > autoVerticalLimit);
            
            if (!useVerticalInside) return 'top';
            const value = context.dataset.data[context.dataIndex];
            const maxVal = Math.max(...context.dataset.data.map(v => Number(v) || 0), 1);
            return (value / maxVal) < 0.20 ? 'top' : 'center';
        },
        rotation: function(context) {
            const itemCount = context.chart.data.labels.length;
            const autoVerticalLimit = 10;
            const useVerticalInside = forceVerticalInside !== null 
                ? forceVerticalInside 
                : (itemCount > autoVerticalLimit);
            
            if (!useVerticalInside) return 0;
            const value = context.dataset.data[context.dataIndex];
            const maxVal = Math.max(...context.dataset.data.map(v => Number(v) || 0), 1);
            return (value / maxVal) < 0.20 ? 0 : -90;
        },
        color: function(context) {
            const itemCount = context.chart.data.labels.length;
            const autoVerticalLimit = 10;
            const useVerticalInside = forceVerticalInside !== null 
                ? forceVerticalInside 
                : (itemCount > autoVerticalLimit);
            
            const value = context.dataset.data[context.dataIndex];
            const maxVal = Math.max(...context.dataset.data.map(v => Number(v) || 0), 1);
            return (!useVerticalInside || (value / maxVal) < 0.20) ? '#475569' : '#ffffff';
        },
        offset: function(context) {
            const itemCount = context.chart.data.labels.length;
            const autoVerticalLimit = 10;
            const useVerticalInside = forceVerticalInside !== null 
                ? forceVerticalInside 
                : (itemCount > autoVerticalLimit);
            
            if (!useVerticalInside) return 4;
            const value = context.dataset.data[context.dataIndex];
            const maxVal = Math.max(...context.dataset.data.map(v => Number(v) || 0), 1);
            return (value / maxVal) < 0.20 ? 4 : 0;
        },
        font: function(context) {
            const itemCount = context.chart.data.labels.length;
            const autoVerticalLimit = 10;
            const useVerticalInside = forceVerticalInside !== null 
                ? forceVerticalInside 
                : (itemCount > autoVerticalLimit);
            return {
                family: "'Plus Jakarta Sans', 'Inter', sans-serif",
                weight: '700',
                size: useVerticalInside ? 9 : 10
            };
        },
        formatter: (value, context) => {
            if (context.dataset.label && context.dataset.label.includes('%')) {
                return value + '%';
            }
            return value;
        }
    };
}

// Generate beautiful single dataset bar chart
function createBarChart(id, labels, data, datasetLabel, colorTheme = 'indigo', showLabels = true, verticalInsideLabels = null) {
    const theme = THEME_COLORS[colorTheme] || THEME_COLORS.indigo;
    
    // Dynamically adjust container width if there are many items
    adjustScrollContainer(id, labels.length);
    
    // Configure datalabels dynamically using helper
    const datalabelsConfig = getDatalabelConfig(showLabels, verticalInsideLabels);


    return new Chart(
        document.getElementById(id),
        {
            type: "bar",
            data: {
                labels: labels,
                datasets: [
                    {
                        label: datasetLabel,
                        data: data,
                        backgroundColor: getCanvasGradient(id, colorTheme),
                        borderColor: theme.border,
                        borderWidth: 1,
                        borderRadius: 6,
                        hoverBackgroundColor: theme.border
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    datalabels: datalabelsConfig
                },
                scales: {
                    x: {
                        grid: { display: false },
                        ticks: {
                            maxRotation: 45,
                            minRotation: 0,
                            font: { size: 10 }
                        }
                    },
                    y: {
                        border: { dash: [5, 5] },
                        grid: { color: '#f1f5f9' },
                        beginAtZero: true,
                        grace: '10%'
                    }
                }
            }
        }
    );
}

loadBtn.addEventListener("click", async () => {
    // Show loading state
    loadBtn.disabled = true;
    loadBtn.innerHTML = `<span>⏳</span> Loading...`;

    try {
        destroyCharts();
        const type = dashboardType.value;
        let endpoint = "";

        if (type === "main") {
            endpoint = "/dashboard/main";
            const res = await fetch(BASE_URL + endpoint);
            const data = await res.json();

            chartsContainer.style.display = "grid";

            // Update Dynamic Titles in the DOM for Main Dashboard
            document.getElementById("title-chart1").textContent = "Unit-wise Completion Rate (%)";
            document.getElementById("title-chart2").textContent = "Lapsed Submissions by Unit";
            document.getElementById("title-chart3").textContent = "Department-wise Completion Rate (%)";
            document.getElementById("title-chart4").textContent = "Lapsed Submissions by Department";
            document.getElementById("title-chart5").textContent = "Checklist-wise Completion Rate (%)";
            document.getElementById("title-chart6").textContent = "Lapsed Submissions by Checklist";

            // Main metadata date banner
            todayBanner.innerHTML = `
                <div class="meta-date-badge">
                    <span class="meta-icon">📅</span>
                    <span class="meta-text">Latest Reporting Date: <strong>${formatDate(data.today_summary.latest_date)}</strong></span>
                </div>
            `;

            // KPI Grid
            kpiContainer.innerHTML = `
                <div class="kpi-grid">
                    <div class="kpi-card">
                        <div class="kpi-card-header">
                            <span class="kpi-card-title">Daily Targets</span>
                            <div class="kpi-icon blue">🎯</div>
                        </div>
                        <div class="kpi-value-container">
                            <span class="kpi-card-value">${data.today_summary.targets}</span>
                            <span class="kpi-card-subtext">Expected checklists</span>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-card-header">
                            <span class="kpi-card-title">Daily Submissions</span>
                            <div class="kpi-icon green">📤</div>
                        </div>
                        <div class="kpi-value-container">
                            <span class="kpi-card-value">${data.today_summary.submissions}</span>
                            <span class="kpi-card-subtext positive">Received in full</span>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-card-header">
                            <span class="kpi-card-title">Lapsed Submissions</span>
                            <div class="kpi-icon red">⚠️</div>
                        </div>
                        <div class="kpi-value-container">
                            <span class="kpi-card-value">${data.today_summary.lapsed}</span>
                            <span class="kpi-card-subtext ${data.today_summary.lapsed > 0 ? 'negative' : 'positive'}">
                                ${data.today_summary.lapsed > 0 ? 'Action required' : 'All clear'}
                            </span>
                        </div>
                    </div>

                    <div class="kpi-card">
                        <div class="kpi-card-header">
                            <span class="kpi-card-title">Completion Rate</span>
                            <div class="kpi-icon indigo">📈</div>
                        </div>
                        <div class="kpi-value-container">
                            <span class="kpi-card-value">${data.today_summary.completion}%</span>
                            <div class="progress-bar-container">
                                <div class="progress-bar-fill" style="width: ${data.today_summary.completion}%"></div>
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Render Charts with dynamic gradients & styling
            // CHART 1: Unit Performance Completion %
            charts.push(
                createBarChart(
                    "chart1",
                    data.units.map(x => x.unit_name),
                    data.units.map(x => x.completion),
                    "Completion %",
                    "indigo"
                )
            );

            // CHART 2: Unit Lapsed
            charts.push(
                createBarChart(
                    "chart2",
                    data.units.map(x => x.unit_name),
                    data.units.map(x => x.lapsed),
                    "Lapsed Count",
                    "rose"
                )
            );

            // CHART 3: Department Performance Completion %
            charts.push(
                createBarChart(
                    "chart3",
                    data.departments.map(x => x.department_name),
                    data.departments.map(x => x.completion),
                    "Completion %",
                    "violet"
                )
            );

            // CHART 4: Department Lapsed
            charts.push(
                createBarChart(
                    "chart4",
                    data.departments.map(x => x.department_name),
                    data.departments.map(x => x.lapsed),
                    "Lapsed Count",
                    "amber"
                )
            );

            // CHART 5: Checklist Performance Completion %
            charts.push(
                createBarChart(
                    "chart5",
                    data.checklists.map(x => x.checklist_name),
                    data.checklists.map(x => x.completion),
                    "Completion %",
                    "sky",
                    true, // showLabels
                    true  // verticalInsideLabels
                )
            );

            // CHART 6: Checklist Lapsed
            charts.push(
                createBarChart(
                    "chart6",
                    data.checklists.map(x => x.checklist_name),
                    data.checklists.map(x => x.lapsed),
                    "Lapsed Count",
                    "rose",
                    true, // showLabels
                    true  // verticalInsideLabels
                )
            );

            return; // Exit Main Dashboard flow
        }

        // Specific Entity Dashboards Flow
        const name = entityDropdown.value;
        if (!name || name === "Select") {
            alert("Please select an entity first.");
            return;
        }

        if (type === "unit") endpoint = `/unit/dashboard/${name}`;
        if (type === "department") endpoint = `/department/dashboard/${name}`;
        if (type === "checklist") endpoint = `/checklist/dashboard/${name}`;

        const response = await fetch(BASE_URL + endpoint);
        const data = await response.json();

        chartsContainer.style.display = "grid";

        // Update Dynamic Titles in the DOM for Specific Dashboards
        document.getElementById("title-chart1").textContent = "7-Day Completion Trend";
        document.getElementById("title-chart2").textContent = "30-Day Completion Trend";
        document.getElementById("title-chart3").textContent = "Submissions vs Targets (Last 30 Days)";
        document.getElementById("title-chart4").textContent = "Daily Lapsed Submissions";
        document.getElementById("title-chart5").textContent = "Highest Performing Days (Best %)";
        document.getElementById("title-chart6").textContent = "Today's Performance Comparison";

        const kpis = data.kpis;
        const comparison = data.daily_comparison;
        const todayStats = comparison.today_stats;

        const latestDate = data.trend_7_days.length > 0
            ? data.trend_7_days[data.trend_7_days.length - 1].report_date
            : new Date();

        // Update meta date
        todayBanner.innerHTML = `
            <div class="meta-date-badge">
                <span class="meta-icon">📅</span>
                <span class="meta-text">Latest Reporting Date: <strong>${formatDate(latestDate)}</strong></span>
            </div>
        `;

        // Render KPI grids for Comparison & Summary metrics
        kpiContainer.innerHTML = `
            <div class="kpi-grid entity-kpis">
                <!-- Target Comparison -->
                <div class="kpi-card comparison-card-v2">
                    <div class="comparison-header">
                        <span class="comparison-card-title">Target Comparison</span>
                        <span class="comparison-icon blue">🎯</span>
                    </div>
                    <div class="comparison-metrics">
                        <div class="metric-block">
                            <span class="metric-label">TOTAL EXPECTED</span>
                            <span class="metric-val">${kpis.total_targets}</span>
                        </div>
                        <div class="metric-block border-left">
                            <span class="metric-label">TODAY'S TARGET</span>
                            <span class="metric-val">${todayStats.target}</span>
                        </div>
                    </div>
                </div>

                <!-- Submission Comparison -->
                <div class="kpi-card comparison-card-v2">
                    <div class="comparison-header">
                        <span class="comparison-card-title">Submissions Comparison</span>
                        <span class="comparison-icon green">📤</span>
                    </div>
                    <div class="comparison-metrics">
                        <div class="metric-block">
                            <span class="metric-label">TOTAL SUBMITTED</span>
                            <span class="metric-val">${kpis.total_submissions}</span>
                        </div>
                        <div class="metric-block border-left">
                            <span class="metric-label">TODAY'S SUBMIT</span>
                            <span class="metric-val">${todayStats.submission}</span>
                        </div>
                    </div>
                </div>

                <!-- Lapsed Comparison -->
                <div class="kpi-card comparison-card-v2">
                    <div class="comparison-header">
                        <span class="comparison-card-title">Lapsed Comparison</span>
                        <span class="comparison-icon red">⚠️</span>
                    </div>
                    <div class="comparison-metrics">
                        <div class="metric-block">
                            <span class="metric-label">TOTAL LAPSED</span>
                            <span class="metric-val">${kpis.total_lapsed}</span>
                        </div>
                        <div class="metric-block border-left">
                            <span class="metric-label">TODAY'S LAPSED</span>
                            <span class="metric-val">${todayStats.lapsed}</span>
                        </div>
                    </div>
                </div>

                <!-- Completion Rate Comparison -->
                <div class="kpi-card comparison-card-v2">
                    <div class="comparison-header">
                        <span class="comparison-card-title">Completion Rate</span>
                        <span class="comparison-icon indigo">📈</span>
                    </div>
                    <div class="comparison-metrics">
                        <div class="metric-block">
                            <span class="metric-label">OVERALL AVG</span>
                            <span class="metric-val">${kpis.completion_percentage}%</span>
                        </div>
                        <div class="metric-block border-left">
                            <span class="metric-label">TODAY</span>
                            <span class="metric-val">${comparison.today_completion}%</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Trends Comparison Row -->
            <div class="comparison-sub-grid">
                <!-- Compared to Yesterday -->
                <div class="kpi-card mini-comparison-card">
                    <div class="mini-title">Compared to Yesterday</div>
                    <div class="mini-metrics">
                        <div>
                            <span class="mini-label">Yesterday</span>
                            <span class="mini-value">${comparison.yesterday_completion}%</span>
                        </div>
                        <div class="mini-change-wrapper">
                            <span class="mini-label">Change</span>
                            <span class="trend-badge ${comparison.vs_yesterday >= 0 ? 'positive-badge' : 'negative-badge'}">
                                ${comparison.vs_yesterday >= 0 ? '▲' : '▼'} ${Math.abs(comparison.vs_yesterday)}%
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Compared to 7d Avg -->
                <div class="kpi-card mini-comparison-card">
                    <div class="mini-title">Compared to 7-Day Average</div>
                    <div class="mini-metrics">
                        <div>
                            <span class="mini-label">7-Day Avg</span>
                            <span class="mini-value">${comparison.avg_7_days}%</span>
                        </div>
                        <div class="mini-change-wrapper">
                            <span class="mini-label">Change</span>
                            <span class="trend-badge ${comparison.vs_7_days >= 0 ? 'positive-badge' : 'negative-badge'}">
                                ${comparison.vs_7_days >= 0 ? '▲' : '▼'} ${Math.abs(comparison.vs_7_days)}%
                            </span>
                        </div>
                    </div>
                </div>

                <!-- Compared to 30d Avg -->
                <div class="kpi-card mini-comparison-card">
                    <div class="mini-title">Compared to 30-Day Average</div>
                    <div class="mini-metrics">
                        <div>
                            <span class="mini-label">30-Day Avg</span>
                            <span class="mini-value">${comparison.avg_30_days}%</span>
                        </div>
                        <div class="mini-change-wrapper">
                            <span class="mini-label">Change</span>
                            <span class="trend-badge ${comparison.vs_30_days >= 0 ? 'positive-badge' : 'negative-badge'}">
                                ${comparison.vs_30_days >= 0 ? '▲' : '▼'} ${Math.abs(comparison.vs_30_days)}%
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Render charts for Entity Dashboard
        // CHART 1: 7 Day Trend line
        charts.push(
            createLineChart(
                "chart1",
                data.trend_7_days.map(x => formatDate(x.report_date)),
                data.trend_7_days.map(x => x.completion_percentage),
                "Completion %",
                "indigo"
            )
        );

        // CHART 2: 30 Day Trend line
        charts.push(
            createLineChart(
                "chart2",
                data.trend_30_days.map(x => formatDate(x.report_date)),
                data.trend_30_days.map(x => x.completion_percentage),
                "Completion %",
                "violet"
            )
        );

        // CHART 3: Target vs Submission
        adjustScrollContainer("chart3", data.submission_vs_target.length, 45);
        charts.push(
            new Chart(
                document.getElementById("chart3"),
                {
                    type: "bar",
                    data: {
                        labels: data.submission_vs_target.map(x => formatDate(x.report_date)),
                        datasets: [
                            {
                                label: "Targets",
                                data: data.submission_vs_target.map(x => x.no_of_targets),
                                backgroundColor: getCanvasGradient("chart3", "emerald"),
                                borderColor: THEME_COLORS.emerald.border,
                                borderWidth: 1,
                                borderRadius: 4
                            },
                            {
                                label: "Submissions",
                                data: data.submission_vs_target.map(x => x.no_of_submission),
                                backgroundColor: getCanvasGradient("chart3", "indigo"),
                                borderColor: THEME_COLORS.indigo.border,
                                borderWidth: 1,
                                borderRadius: 4
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: true, position: 'top' },
                            datalabels: getDatalabelConfig(true, true)
                        },
                        scales: {
                            x: {
                                grid: { display: false },
                                ticks: { maxRotation: 45, minRotation: 0, font: { size: 9 } }
                            },
                            y: { border: { dash: [5, 5] }, grid: { color: '#f1f5f9' }, beginAtZero: true }
                        }
                    }
                }
            )
        );

        // CHART 4: Daily Lapsed
        charts.push(
            createBarChart(
                "chart4",
                data.daily_lapsed.map(x => formatDate(x.report_date)),
                data.daily_lapsed.map(x => x.no_of_lapsed),
                "Lapsed",
                "rose"
            )
        );

        // CHART 5: Best Performing Days
        charts.push(
            createBarChart(
                "chart5",
                data.best_days.map(x => formatDate(x.report_date)),
                data.best_days.map(x => x.completion_percentage),
                "Completion %",
                "emerald"
            )
        );

        // CHART 6: Performance Comparison
        charts.push(
            new Chart(
                document.getElementById("chart6"),
                {
                    type: "bar",
                    data: {
                        labels: ["Today", "Yesterday", "7d Avg", "30d Avg"],
                        datasets: [
                            {
                                label: "Completion %",
                                data: [
                                    comparison.today_completion,
                                    comparison.yesterday_completion,
                                    comparison.avg_7_days,
                                    comparison.avg_30_days
                                ],
                                backgroundColor: [
                                    getCanvasGradient("chart6", "indigo"),
                                    getCanvasGradient("chart6", "sky"),
                                    getCanvasGradient("chart6", "violet"),
                                    getCanvasGradient("chart6", "emerald")
                                ],
                                borderColor: [
                                    THEME_COLORS.indigo.border,
                                    THEME_COLORS.sky.border,
                                    THEME_COLORS.violet.border,
                                    THEME_COLORS.emerald.border
                                ],
                                borderWidth: 1,
                                borderRadius: 6
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            datalabels: getDatalabelConfig(true, false)
                        },
                        scales: {
                            x: { grid: { display: false } },
                            y: { border: { dash: [5, 5] }, grid: { color: '#f1f5f9' }, beginAtZero: true, max: 100, grace: '10%' }
                        }
                    }
                }
            )
        );

    } catch (err) {
        console.error("Error loading dashboard data:", err);
        alert("Failed to load dashboard data. Make sure the backend server is running.");
    } finally {
        // Reset load button loading state
        loadBtn.disabled = false;
        loadBtn.innerHTML = `<span>🔄</span> Load Dashboard`;
    }
});