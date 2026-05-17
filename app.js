// ==========================================================================
// 🚀 APP.JS: CLIENT-SIDE REACTION, ANCHOR LOGIC, INTERACTIVE GRAPHICS
// ==========================================================================

const TOTAL_ALLOCATED_SUPPLY = 100923053.37; // Total allocated $BILL rewards supply

// Global state variables
let state = {
    filteredData: [],
    currentPage: 1,
    pageSize: 25,
    sortField: 'amount', // default sorted by amount descending
    sortDirection: 'desc',
    searchTerm: '',
    selectedBracket: 'all'
};

// Elements DOM hooks
const elements = {
    statWallets: document.getElementById('stat-total-wallets'),
    statTokens: document.getElementById('stat-total-tokens'),
    statMax: document.getElementById('stat-max-claim'),
    statMaxHolder: document.getElementById('stat-max-holder'),
    statAllocatedSupply: document.getElementById('stat-allocated-supply'),
    statProgressPct: document.getElementById('stat-progress-pct'),
    statProgressBar: document.getElementById('stat-progress-bar'),
    countdownTimer: document.getElementById('countdown-timer'),
    
    searchInput: document.getElementById('search-input'),
    clearSearchBtn: document.getElementById('clear-search-btn'),
    bracketFilter: document.getElementById('bracket-filter'),
    pageSizeSelector: document.getElementById('page-size-selector'),
    
    tableBody: document.getElementById('table-body'),
    noResults: document.getElementById('no-results'),
    headers: document.querySelectorAll('#claims-table th.sortable'),
    
    pagStart: document.getElementById('pag-start'),
    pagEnd: document.getElementById('pag-end'),
    pagTotal: document.getElementById('pag-total'),
    paginationButtons: document.getElementById('pagination-buttons'),
    toast: document.getElementById('toast')
};

// ==========================================================================
// 📊 METRICS & CHART COMPUTATIONS (100% Dynamic)
// ==========================================================================

function initAnalytics() {
    // 1. Calculate Core Statistics
    const totalClaims = claimsData.length;
    let totalTokens = 0;
    const amounts = [];
    
    claimsData.forEach(c => {
        totalTokens += c.amount;
        amounts.push(c.amount);
    });
    
    // Sort amounts for median calculation
    amounts.sort((a, b) => a - b);
    const median = totalClaims > 0 ? amounts[Math.floor(totalClaims / 2)] : 0;
    const average = totalClaims > 0 ? totalTokens / totalClaims : 0;
    const maxVal = amounts.length > 0 ? amounts[amounts.length - 1] : 0;
    
    // Find whale holding maximum
    const maxClaimant = claimsData.find(c => c.amount === maxVal);
    
    // Calculate Claim Progress percentage
    const progressPct = (totalTokens / TOTAL_ALLOCATED_SUPPLY) * 100;
    
    // Render Stats
    elements.statWallets.innerText = totalClaims.toLocaleString();
    elements.statTokens.innerText = `${totalTokens.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} BILL`;
    elements.statMax.innerText = `${maxVal.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} BILL`;
    
    if (elements.statAllocatedSupply) {
        elements.statAllocatedSupply.innerText = `${TOTAL_ALLOCATED_SUPPLY.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})} BILL`;
    }
    if (elements.statProgressPct) {
        elements.statProgressPct.innerText = `${progressPct.toFixed(2)}%`;
    }
    if (elements.statProgressBar) {
        // Smooth delayed transition to trigger CSS transition animation on page load
        setTimeout(() => {
            elements.statProgressBar.style.width = `${progressPct.toFixed(2)}%`;
        }, 150);
    }
    
    if (maxClaimant) {
        elements.statMaxHolder.innerText = `${maxClaimant.address.substring(0, 6)}...${maxClaimant.address.substring(maxClaimant.address.length - 4)}`;
        elements.statMaxHolder.title = maxClaimant.address;
    }
    
    // 2. Compute Distribution Brackets
    let bracketCounts = {
        whale: 0,
        high: 0,
        medium: 0,
        supporter: 0,
        retail: 0,
        test: 0
    };
    
    claimsData.forEach(c => {
        const amt = c.amount;
        if (amt >= 1000000) bracketCounts.whale++;
        else if (amt >= 100000) bracketCounts.high++;
        else if (amt >= 10000) bracketCounts.medium++;
        else if (amt >= 1000) bracketCounts.supporter++;
        else if (amt >= 500) bracketCounts.retail++;
        else bracketCounts.test++;
    });
    
    // Render Charts
    renderDistributionChart(bracketCounts);
    renderVelocityChart();
}

// Render Doughnut distribution chart
function renderDistributionChart(counts) {
    const ctx = document.getElementById('distributionChart').getContext('2d');
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: [
                'Whales (>= 1M BILL)',
                'High Tier (100k - 999k)',
                'Medium Tier (10k - 99k)',
                'Supporters (1k - 9.9k)',
                'Retail (500 - 999 BILL)',
                'Testing (< 100 BILL)'
            ],
            datasets: [{
                data: [counts.whale, counts.high, counts.medium, counts.supporter, counts.retail, counts.test],
                backgroundColor: [
                    '#ff007f', // Accent Pink
                    '#00f2fe', // Cyan
                    '#7f00ff', // Violet
                    '#3d5afe', // Light blue
                    '#00e676', // Green
                    '#5c647a'  // Muted gray
                ],
                borderColor: '#0b0d19',
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#8d96b0',
                        font: {
                            family: 'Outfit',
                            size: 11
                        },
                        boxWidth: 12
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const pct = ((value / claimsData.length) * 100).toFixed(2);
                            return ` ${label}: ${value.toLocaleString()} (${pct}%)`;
                        }
                    }
                }
            },
            cutout: '65%'
        }
    });
}

// Render line velocity chart
function renderVelocityChart() {
    const ctx = document.getElementById('velocityChart').getContext('2d');
    
    // Process timeline
    const timeline = {};
    claimsData.forEach(c => {
        const day = c.timestamp.split(' ')[0]; // YYYY-MM-DD
        timeline[day] = (timeline[day] || 0) + 1;
    });
    
    const sortedDays = Object.keys(timeline).sort();
    const labels = sortedDays.map(d => {
        const parts = d.split('-');
        return `${parts[1]}-${parts[2]}`; // MM-DD
    });
    const values = sortedDays.map(d => timeline[d]);
    
    // Create gradient
    const gradient = ctx.createLinearGradient(0, 0, 0, 240);
    gradient.addColorStop(0, 'rgba(0, 242, 254, 0.4)');
    gradient.addColorStop(1, 'rgba(127, 0, 255, 0.0)');
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Claims Velocity',
                data: values,
                borderColor: '#00f2fe',
                borderWidth: 2,
                pointBackgroundColor: '#7f00ff',
                pointBorderColor: '#00f2fe',
                pointHoverRadius: 6,
                fill: true,
                backgroundColor: gradient,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#8d96b0', font: { family: 'Outfit', size: 10 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#8d96b0', font: { family: 'Outfit', size: 10 } }
                }
            }
        }
    });
}

// ==========================================================================
// ⚡ CORE TABLE OPERATIONS (Fuzzy Search, Sort, Filter, Render)
// ==========================================================================

function updateDataGrid() {
    // 1. Fuzzy Filter
    state.filteredData = claimsData.filter(claim => {
        // Search Term Check
        let matchesSearch = true;
        if (state.searchTerm) {
            const term = state.searchTerm.toLowerCase();
            const addr = claim.address.toLowerCase();
            const amt = claim.amount.toString();
            matchesSearch = addr.includes(term) || amt.includes(term);
        }
        
        // Bracket Filter Check
        let matchesBracket = true;
        if (state.selectedBracket !== 'all') {
            const amt = claim.amount;
            if (state.selectedBracket === 'whale') matchesBracket = amt >= 1000000;
            else if (state.selectedBracket === 'high') matchesBracket = amt >= 100000 && amt < 1000000;
            else if (state.selectedBracket === 'medium') matchesBracket = amt >= 10000 && amt < 100000;
            else if (state.selectedBracket === 'supporter') matchesBracket = amt >= 1000 && amt < 10000;
            else if (state.selectedBracket === 'retail') matchesBracket = amt >= 500 && amt < 1000;
            else if (state.selectedBracket === 'test') matchesBracket = amt < 100;
        }
        
        return matchesSearch && matchesBracket;
    });
    
    // 2. Apply Sorting
    state.filteredData.sort((a, b) => {
        let valA = a[state.sortField];
        let valB = b[state.sortField];
        
        if (typeof valA === 'string') {
            valA = valA.toLowerCase();
            valB = valB.toLowerCase();
        }
        
        if (valA < valB) return state.sortDirection === 'asc' ? -1 : 1;
        if (valA > valB) return state.sortDirection === 'asc' ? 1 : -1;
        return 0;
    });
    
    // 3. Keep current page bounded
    const totalRecords = state.filteredData.length;
    const maxPage = Math.max(1, Math.ceil(totalRecords / state.pageSize));
    if (state.currentPage > maxPage) {
        state.currentPage = maxPage;
    }
    
    // 4. Render Layout & Table Row items
    renderTable();
    renderPagination(totalRecords, maxPage);
}

// Render rows in HTML
function renderTable() {
    elements.tableBody.innerHTML = '';
    
    const totalRecords = state.filteredData.length;
    if (totalRecords === 0) {
        elements.noResults.style.display = 'block';
        elements.pagStart.innerText = '0';
        elements.pagEnd.innerText = '0';
        elements.pagTotal.innerText = '0';
        return;
    }
    
    elements.noResults.style.display = 'none';
    
    const startIndex = (state.currentPage - 1) * state.pageSize;
    const endIndex = Math.min(startIndex + state.pageSize, totalRecords);
    const paginatedItems = state.filteredData.slice(startIndex, endIndex);
    
    // Update pagination labels
    elements.pagStart.innerText = (startIndex + 1).toLocaleString();
    elements.pagEnd.innerText = endIndex.toLocaleString();
    elements.pagTotal.innerText = totalRecords.toLocaleString();
    
    paginatedItems.forEach(claim => {
        const row = document.createElement('tr');
        
        // Amount Badge Label
        let badgeHtml = '';
        if (claim.amount >= 1000000) {
            badgeHtml = `<span class="amount-badge badge-whale">Whale</span>`;
        } else if (claim.amount >= 100000) {
            badgeHtml = `<span class="amount-badge badge-high">High</span>`;
        } else if (claim.amount >= 1000) {
            badgeHtml = `<span class="amount-badge badge-supporter">Supporter</span>`;
        } else if (claim.amount >= 500) {
            badgeHtml = `<span class="amount-badge badge-retail">Retail</span>`;
        }
        
        const shortAddr = `${claim.address.substring(0, 8)}...${claim.address.substring(claim.address.length - 8)}`;
        
        row.innerHTML = `
            <td class="rank-col">#${claim.rank}</td>
            <td>
                <div class="address-cell" data-address="${claim.address}" title="Click to copy full address">
                    ${shortAddr} <i class="fa-regular fa-copy copy-icon"></i>
                </div>
            </td>
            <td class="amount-col" style="color: ${claim.amount >= 100000 ? 'var(--color-primary)' : 'var(--text-main)'}">
                ${claim.amount.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2})}
                ${badgeHtml}
            </td>
            <td class="date-col">${claim.timestamp}</td>
            <td>
                <a href="https://explorer.billions.network/tx/${claim.tx}" target="_blank" class="explorer-link">
                    Tx <i class="fa-solid fa-arrow-up-right-from-square"></i>
                </a>
            </td>
        `;
        
        elements.tableBody.appendChild(row);
    });
    
    // Rebind Click-To-Copy listeners to fresh cells
    document.querySelectorAll('.address-cell').forEach(cell => {
        cell.addEventListener('click', function() {
            const addr = this.getAttribute('data-address');
            navigator.clipboard.writeText(addr).then(() => {
                showToast(`Copied wallet address: ${addr.substring(0, 10)}...`);
            });
        });
    });
}

// Render dynamic pagination page buttons
function renderPagination(total, maxPage) {
    elements.paginationButtons.innerHTML = '';
    
    if (total === 0) return;
    
    // Create Previous Button
    const prevBtn = document.createElement('button');
    prevBtn.className = `pag-btn ${state.currentPage === 1 ? 'disabled' : ''}`;
    prevBtn.innerHTML = '<i class="fa-solid fa-angle-left"></i>';
    prevBtn.addEventListener('click', () => {
        if (state.currentPage > 1) {
            state.currentPage--;
            updateDataGrid();
            scrollToTableTop();
        }
    });
    elements.paginationButtons.appendChild(prevBtn);
    
    // Dynamic page ranges logic
    const delta = 2; // display 2 pages before and after current
    const range = [];
    for (let i = Math.max(2, state.currentPage - delta); i <= Math.min(maxPage - 1, state.currentPage + delta); i++) {
        range.push(i);
    }
    
    // Page 1
    const p1Btn = document.createElement('button');
    p1Btn.className = `pag-btn ${state.currentPage === 1 ? 'active' : ''}`;
    p1Btn.innerText = '1';
    p1Btn.addEventListener('click', () => {
        state.currentPage = 1;
        updateDataGrid();
        scrollToTableTop();
    });
    elements.paginationButtons.appendChild(p1Btn);
    
    // Elipses before range
    if (state.currentPage - delta > 2) {
        const span = document.createElement('span');
        span.className = 'pag-btn disabled';
        span.innerText = '...';
        elements.paginationButtons.appendChild(span);
    }
    
    // Range
    range.forEach(p => {
        const pBtn = document.createElement('button');
        pBtn.className = `pag-btn ${state.currentPage === p ? 'active' : ''}`;
        pBtn.innerText = p;
        pBtn.addEventListener('click', () => {
            state.currentPage = p;
            updateDataGrid();
            scrollToTableTop();
        });
        elements.paginationButtons.appendChild(pBtn);
    });
    
    // Elipses after range
    if (state.currentPage + delta < maxPage - 1) {
        const span = document.createElement('span');
        span.className = 'pag-btn disabled';
        span.innerText = '...';
        elements.paginationButtons.appendChild(span);
    }
    
    // Last Page (if maxPage > 1)
    if (maxPage > 1) {
        const pMaxBtn = document.createElement('button');
        pMaxBtn.className = `pag-btn ${state.currentPage === maxPage ? 'active' : ''}`;
        pMaxBtn.innerText = maxPage;
        pMaxBtn.addEventListener('click', () => {
            state.currentPage = maxPage;
            updateDataGrid();
            scrollToTableTop();
        });
        elements.paginationButtons.appendChild(pMaxBtn);
    }
    
    // Create Next Button
    const nextBtn = document.createElement('button');
    nextBtn.className = `pag-btn ${state.currentPage === maxPage ? 'disabled' : ''}`;
    nextBtn.innerHTML = '<i class="fa-solid fa-angle-right"></i>';
    nextBtn.addEventListener('click', () => {
        if (state.currentPage < maxPage) {
            state.currentPage++;
            updateDataGrid();
            scrollToTableTop();
        }
    });
    elements.paginationButtons.appendChild(nextBtn);
}

// Utility smooth scroll
function scrollToTableTop() {
    document.querySelector('.explorer-panel').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Show copying notification toast
let toastTimeout;
function showToast(message) {
    elements.toast.innerText = message;
    elements.toast.classList.add('show');
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => {
        elements.toast.classList.remove('show');
    }, 2000);
}

// ==========================================================================
// 🔔 ATTACH DOM LISTENERS & HANDLERS
// ==========================================================================

function setupEventListeners() {
    // 1. Search Bar listener
    elements.searchInput.addEventListener('input', (e) => {
        state.searchTerm = e.target.value;
        if (state.searchTerm) {
            elements.clearSearchBtn.style.display = 'block';
        } else {
            elements.clearSearchBtn.style.display = 'none';
        }
        state.currentPage = 1; // reset page
        updateDataGrid();
    });
    
    // Clear search button click
    elements.clearSearchBtn.addEventListener('click', () => {
        elements.searchInput.value = '';
        state.searchTerm = '';
        elements.clearSearchBtn.style.display = 'none';
        state.currentPage = 1;
        updateDataGrid();
    });
    
    // 2. Bracket Selection filter
    elements.bracketFilter.addEventListener('change', (e) => {
        state.selectedBracket = e.target.value;
        state.currentPage = 1;
        updateDataGrid();
    });
    
    // 3. Page Size selection
    elements.pageSizeSelector.addEventListener('change', (e) => {
        state.pageSize = parseInt(e.target.value);
        state.currentPage = 1;
        updateDataGrid();
    });
    
    // 4. Sort Headers click listeners
    elements.headers.forEach(header => {
        header.addEventListener('click', function() {
            const field = this.getAttribute('data-sort');
            
            // Toggle direction or switch fields
            if (state.sortField === field) {
                state.sortDirection = state.sortDirection === 'asc' ? 'desc' : 'asc';
            } else {
                state.sortField = field;
                state.sortDirection = 'desc'; // default sorting is desc
            }
            
            // Update active header visual classes
            elements.headers.forEach(h => {
                h.classList.remove('active-sort');
                const icon = h.querySelector('i');
                icon.className = 'fa-solid fa-sort';
            });
            
            this.classList.add('active-sort');
            const currentIcon = this.querySelector('i');
            currentIcon.className = state.sortDirection === 'asc' ? 'fa-solid fa-sort-up' : 'fa-solid fa-sort-down';
            
            state.currentPage = 1;
            updateDataGrid();
        });
    });
}

// ==========================================================================
// 🔄 REAL-TIME CLIENT-SIDE SYNCING (Blockscout API Integration)
// ==========================================================================

let countdownSeconds = 30;
let refreshInterval;

function startCountdown() {
    if (refreshInterval) clearInterval(refreshInterval);
    
    countdownSeconds = 30;
    updateCountdownUI();
    
    refreshInterval = setInterval(() => {
        countdownSeconds--;
        if (countdownSeconds <= 0) {
            clearInterval(refreshInterval);
            syncLatestClaims();
        } else {
            updateCountdownUI();
        }
    }, 1000);
}

function updateCountdownUI() {
    if (elements.countdownTimer) {
        elements.countdownTimer.innerText = `LIVE: ${countdownSeconds}s`;
    }
}

// Fire a premium live notification when a claim is registered in real-time
function showLiveNotification(claimant, amount) {
    const shortAddr = `${claimant.substring(0, 6)}...${claimant.substring(claimant.length - 4)}`;
    const formattedAmt = amount.toLocaleString(undefined, {minimumFractionDigits: 2, maximumFractionDigits: 2});
    showToast(`⚡ NEW CLAIM: ${shortAddr} claimed ${formattedAmt} $BILL!`);
}

async function syncLatestClaims() {
    if (elements.countdownTimer) {
        elements.countdownTimer.innerText = "Syncing...";
    }
    
    const distributorAddress = "0x4BB63E4E1AcC5750FD1a6aDF26520126D8c9d6C8";
    const url = `https://explorer.billions.network/api/v2/addresses/${distributorAddress}/transactions`;
    
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error("Network response was not ok");
        
        const data = await res.json();
        const txs = data.items || [];
        
        let newClaimsCount = 0;
        
        txs.forEach(tx => {
            // Check if transaction is a successful claim
            const isSuccess = tx.status === "ok" || tx.result === "success";
            
            if (isSuccess) {
                // Check if we already have this tx in our dataset (case-insensitive)
                const exists = claimsData.some(c => c.tx.toLowerCase() === tx.hash.toLowerCase());
                if (!exists) {
                    let claimant = null;
                    let amountTokens = 0;
                    
                    // Path A: Decoded inputs parameters
                    const decoded = tx.decoded_input || {};
                    const params = {};
                    (decoded.parameters || []).forEach(p => {
                        params[p.name] = p.value;
                    });
                    
                    if (params._onBehalfOf && params._amount) {
                        claimant = params._onBehalfOf;
                        amountTokens = parseFloat(params._amount) / 1e18;
                    } 
                    // Path B: Robust fallback to token transfers (incase ABI decoding is not yet performed by Blockscout)
                    else if (tx.token_transfers && tx.token_transfers.length > 0) {
                        const billTransfer = tx.token_transfers.find(t => 
                            t.token && 
                            t.token.address.toLowerCase() === "0xb060e40c3b053c33d458f7105f95da52741cab62".toLowerCase()
                        );
                        if (billTransfer) {
                            claimant = billTransfer.to ? billTransfer.to.hash : null;
                            if (billTransfer.total && billTransfer.total.value) {
                                amountTokens = parseFloat(billTransfer.total.value) / 1e18;
                            }
                        }
                    }
                    
                    // If a valid claimant and amount is resolved, register it!
                    if (claimant && amountTokens > 0) {
                        // Parse timestamp
                        let timestamp = tx.timestamp || new Date().toISOString();
                        timestamp = timestamp.replace('T', ' ').substring(0, 19);
                        
                        claimsData.push({
                            tx: tx.hash,
                            block: tx.block_number || tx.block || 0,
                            timestamp: timestamp,
                            address: claimant,
                            amount: amountTokens
                        });
                        
                        newClaimsCount++;
                        showLiveNotification(claimant, amountTokens);
                    }
                }
            }
        });
        
        if (newClaimsCount > 0) {
            // Re-sort claims descending by amount, then re-rank
            claimsData.sort((a, b) => b.amount - a.amount);
            claimsData.forEach((c, idx) => {
                c.rank = idx + 1;
            });
            
            // Re-render dashboard panels, graphs, and lists
            initAnalytics();
            updateDataGrid();
        } else {
            console.log("Sync complete: No new claims detected.");
        }
        
    } catch (e) {
        console.error("Error syncing claims:", e);
        showToast("Sync failed: Rate limited or network down.");
    } finally {
        // Reset countdown
        startCountdown();
    }
}

// ==========================================================================
// 🚀 INITIATE APP
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
    // 1. Run Dynamic Analytics Calculations & Render Charts
    initAnalytics();
    
    // 2. Bind DOM Action Listeners
    setupEventListeners();
    
    // 3. Initiate first ledger rendering
    updateDataGrid();
    
    // 4. Start Live Sync Countdown
    startCountdown();
});
